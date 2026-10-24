"""Checks documents against padroes/documentacao.md.

Usage:
  check_docs.py [--root DIR] [files...]   check given files, or every doc of the repository at DIR
  check_docs.py --hook                    Claude Code PostToolUse hook (reads the tool call JSON on stdin)

The standard and the templates live next to this script, in custodia-docs, and are the single
source of truth for statuses, sizes and required sections. The repository being checked can be
custodia-docs itself (area layout) or any project repository (docs/ layout).
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[1]
STANDARD = DOCS_ROOT / "padroes" / "documentacao.md"
TEMPLATES = DOCS_ROOT / "templates"

# Catalog names in the standard mapped to type keys (also the template file names).
CATALOG_TYPES = {
    "Visão da área": "visao",
    "Glossário": "glossario",
    "Regras de módulo": "regras-modulo",
    "Área vizinha": "area-vizinha",
    "ADR": "adr",
    "Spec de feature": "spec",
    "Task de feature": "task",
    "Runbook": "runbook",
    "Spike": "spike",
    "Registro de decisões": "registro-decisoes",
    "README": "readme",
}
# Headings (## or ###) of the standard whose "- Status:" line gives a type its own statuses.
STATUS_SECTIONS = {"spec.md": "spec", "Tasks": "task", "ADR": "adr", "Registro de decisões": "registro-decisoes"}
# The QA task has its own template but follows every other rule of a task.
SAME_RULES_AS = {"task-qa": "task"}
OPTIONAL_MARK = "só quando houver"
NUMBERED = {
    "adr": (re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md$"), "ADR deve seguir NNNN-titulo-curto.md"),
    "spike": (re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md$"), "spike deve seguir NNNN-pergunta-curta.md"),
    "registro-decisoes": (
        re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md$"),
        "registro de decisões deve seguir NNNN-titulo-curto.md",
    ),
    "task": (
        re.compile(r"^\d{2}-(back|front|infra)-[a-z0-9]+(-[a-z0-9]+)*\.md$"),
        "task deve seguir NN-camada-titulo-curto.md, camada back, front ou infra",
    ),
    "task-qa": (re.compile(r"^\d{2}-qa-[a-z0-9]+(-[a-z0-9]+)*\.md$"), "task de QA deve seguir NN-qa-titulo-curto.md"),
}
SPEC_FOLDER = re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DASHES = {"—": "travessão", "–": "meia-risca"}
NA = re.compile(r"(?<!\w)N/A(?!\w)")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# Generated or tooling folders of custodia-docs that are not documents.
AREA_SKIPPED = {"templates", "scripts", "projetos", ".github"}


@dataclass
class Finding:
    level: str
    path: str
    line: int
    message: str

    def __str__(self):
        return f"{self.level} {self.path}:{self.line}: {self.message}"


def is_area(root):
    return (root / "padroes" / "documentacao.md").exists()


def doc_type(path, root):
    """Returns the type key, 'generic' for other docs, or None when the file is not checked."""
    rel = path.resolve().relative_to(root.resolve())
    parts = rel.parts
    if rel.suffix != ".md":
        return None
    if rel == Path("README.md"):
        return "readme"
    if is_area(root):
        if parts[0] in AREA_SKIPPED:
            return None
        if rel == Path("produto/visao.md"):
            return "visao"
        if rel == Path("glossario.md"):
            return "glossario"
        return {"regras": "regras-modulo", "areas-vizinhas": "area-vizinha", "adr": "adr"}.get(
            parts[0] if len(parts) > 1 else "", "generic"
        )
    if parts[0] != "docs":
        return None
    if len(parts) > 2:
        folder = parts[1]
        if folder == "specs":
            if len(parts) == 4 and parts[3] == "spec.md":
                return "spec"
            if len(parts) == 5 and parts[3] == "tasks":
                return "task-qa" if re.match(r"^\d{2}-qa-", parts[4]) else "task"
        known = {"adr": "adr", "runbooks": "runbook", "spikes": "spike", "decisoes": "registro-decisoes"}
        if folder in known:
            return known[folder]
    return "generic"


def split_frontmatter(lines):
    """Returns (fields, index of first body line) or (None, 0) when absent."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fields = {}
            for raw in lines[1:i]:
                key, _, value = raw.partition(":")
                fields[key.strip()] = value.strip()
            return fields, i + 1
    return None, 0


def load_standard():
    lines = STANDARD.read_text(encoding="utf-8").splitlines()
    _, body_start = split_frontmatter(lines)
    general = section = None
    type_statuses = {}
    sizes = {}
    for line in lines[body_start:]:
        stripped = line.strip()
        heading = re.match(r"^#{2,3} (.+)$", line)
        if heading:
            section = STATUS_SECTIONS.get(heading.group(1).strip())
        elif stripped.startswith("status:") and general is None:
            general = {s.strip() for s in stripped[len("status:"):].split("|")}
        elif stripped.startswith("- Status:") and section:
            type_statuses[section] = set(re.findall(r"`([^`]+)`", stripped))
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if cells[0] in CATALOG_TYPES:
                number = re.match(r"\d+", cells[-1])
                sizes[CATALOG_TYPES[cells[0]]] = int(number.group()) if number else None
    return {"statuses": general, "type_statuses": type_statuses, "sizes": sizes}


def is_optional(heading, next_line):
    return OPTIONAL_MARK in heading.lower() or OPTIONAL_MARK in next_line.lower()


def required_sections(kind):
    template = TEMPLATES / f"{kind}.md"
    if not template.exists():
        return []
    lines = template.read_text(encoding="utf-8").splitlines()
    sections = []
    for i, line in enumerate(lines):
        # A heading in <angle brackets> is a placeholder the author replaces, not a fixed section.
        if not line.startswith("## ") or line[3:].lstrip().startswith("<"):
            continue
        following = next((l for l in lines[i + 1:] if l.strip()), "")
        if not is_optional(line, following):
            sections.append(line[3:].strip())
    return sections


def prose_lines(lines, start):
    """Yields (line number, text) outside code blocks, with inline code removed."""
    in_code = False
    for i in range(start, len(lines)):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            yield i + 1, INLINE_CODE.sub("", line)


def broken_link(target, path, root):
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return False
    relative = target.split("#", 1)[0]
    if not relative:
        return False
    base = root if relative.startswith("/") else path.parent
    resolved = (base / relative.lstrip("/")).resolve()
    # Project docs are copied into projetos/ only when the portal is built.
    if is_area(root) and resolved.is_relative_to((root / "projetos").resolve()):
        return False
    return not resolved.exists()


def check_file(path, root):
    kind = doc_type(path, root)
    if kind is None:
        return []
    rules = SAME_RULES_AS.get(kind, kind)
    rel = str(path.resolve().relative_to(root.resolve()))
    standard = load_standard()
    lines = path.read_text(encoding="utf-8").splitlines()
    findings = []

    def add(level, line, message):
        findings.append(Finding(level, rel, line, message))

    fields, body_start = split_frontmatter(lines)
    if kind != "readme":
        if fields is None:
            add("ERRO", 1, "frontmatter ausente (status, atualizado e descricao)")
        else:
            allowed = standard["type_statuses"].get(rules, standard["statuses"])
            if fields.get("status") not in allowed:
                add("ERRO", 2, f"status inválido; use: {', '.join(sorted(allowed))}")
            if not DATE.match(fields.get("atualizado", "")):
                add("ERRO", 3, "atualizado ausente ou fora do formato AAAA-MM-DD")
            if not fields.get("descricao"):
                add("ERRO", 4, "descricao ausente; escreva em uma frase o que o documento responde")
            for key, value in fields.items():
                # An unquoted ": " makes the frontmatter invalid YAML, and the portal build drops the page.
                if ": " in value and value[:1] not in "\"'":
                    add("ERRO", 1, f"{key} com dois-pontos seguido de espaço; reescreva ou ponha o valor entre aspas")

    if kind in NUMBERED:
        pattern, message = NUMBERED[kind]
        if not pattern.match(path.name):
            add("ERRO", 1, message)
    if kind in ("spec", "task", "task-qa"):
        folder = path.parent if kind == "spec" else path.parent.parent
        if not SPEC_FOLDER.match(folder.name):
            add("ERRO", 1, "pasta da spec deve seguir NNNN-titulo-curto")

    size = 0
    for number, text in prose_lines(lines, body_start):
        for char, name in DASHES.items():
            if char in text:
                add("ERRO", number, f"{name} não é permitido; use vírgula, dois-pontos ou parênteses")
        if NA.search(text):
            add("ERRO", number, "N/A não é permitido; apague a seção que não se aplica")
        for target in LINK.findall(text):
            if broken_link(target, path, root):
                add("ERRO", number, f"link quebrado: {target}")
        if text.strip():
            size += 1

    headings = {l[3:].strip() for l in lines if l.startswith("## ")}
    for section in required_sections(kind):
        if section not in headings:
            add("ERRO", 1, f"seção obrigatória ausente: ## {section}")

    limit = standard["sizes"].get(rules)
    if limit and size > limit:
        add("AVISO", 1, f"{size} linhas, referência {limit}; passar é permitido com motivo registrado")
    return findings


def all_docs(root):
    base = root if is_area(root) else root / "docs"
    docs = sorted(base.rglob("*.md")) if base.exists() else []
    readme = root / "README.md"
    if readme.exists() and readme not in docs:
        docs.append(readme)
    return [d for d in docs if doc_type(d, root) is not None]


def repository_root(path):
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def run_hook(stdin=None, stdout=None, stderr=None):
    stdin, stdout, stderr = stdin or sys.stdin, stdout or sys.stdout, stderr or sys.stderr
    payload = json.load(stdin)
    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return 0
    path = Path(file_path).resolve()
    root = repository_root(path.parent)
    if root is None or not path.exists():
        return 0
    findings = check_file(path, root)
    errors = [f for f in findings if f.level == "ERRO"]
    if errors:
        # Exit 2 makes Claude Code show stderr to Claude so it fixes the document.
        print("\n".join(str(f) for f in findings), file=stderr)
        return 2
    if findings:
        context = "\n".join(str(f) for f in findings)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}), file=stdout)
    return 0


def main(argv):
    if argv[:1] == ["--hook"]:
        return run_hook()
    root = Path.cwd()
    if argv[:1] == ["--root"]:
        root, argv = Path(argv[1]), argv[2:]
    root = root.resolve()
    paths = [Path(a).resolve() for a in argv] or all_docs(root)
    findings = [f for p in paths for f in check_file(p, root)]
    for finding in findings:
        print(finding)
    errors = sum(f.level == "ERRO" for f in findings)
    print(f"{len(paths)} arquivo(s), {errors} erro(s), {len(findings) - errors} aviso(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
