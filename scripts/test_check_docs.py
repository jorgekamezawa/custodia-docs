import io
import json
import tempfile
import unittest
from pathlib import Path

import check_docs

VALID_FRONTMATTER = "---\nstatus: ativo\natualizado: 2026-10-24\ndescricao: Diz o que o documento responde.\n---\n"


def adr(status="aceito", body="**Decisão:** x.\n\n## Contexto\nc\n\n## Alternativas descartadas\n- a\n\n## Consequências\n- b\n"):
    return f"---\nstatus: {status}\natualizado: 2026-10-24\ndescricao: Pergunta e resposta.\n---\n# ADR-0001: X\n\n{body}"


class Repo:
    """A temporary project repository with a docs/ folder."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".git").mkdir()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def messages(self, rel, text):
        return [f.message for f in check_docs.check_file(self.write(rel, text), self.root)]


class ProjectLayoutTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.tmp.cleanup()

    def test_valid_generic_doc_has_no_findings(self):
        self.assertEqual(self.repo.messages("docs/index.md", VALID_FRONTMATTER + "# Projeto\n"), [])

    def test_missing_frontmatter_is_an_error(self):
        self.assertIn("frontmatter ausente (status, atualizado e descricao)", self.repo.messages("docs/a.md", "# A\n"))

    def test_missing_description_is_an_error(self):
        text = "---\nstatus: ativo\natualizado: 2026-10-24\n---\n# A\n"
        self.assertTrue(any(m.startswith("descricao ausente") for m in self.repo.messages("docs/a.md", text)))

    def test_unquoted_colon_in_frontmatter_is_an_error(self):
        text = "---\nstatus: ativo\natualizado: 2026-10-24\ndescricao: Regras: prazos\n---\n# A\n"
        quoted = "---\nstatus: ativo\natualizado: 2026-10-24\ndescricao: \"Regras: prazos\"\n---\n# A\n"
        self.assertIn("descricao com dois-pontos seguido de espaço; reescreva ou ponha o valor entre aspas", self.repo.messages("docs/a.md", text))
        self.assertEqual(self.repo.messages("docs/b.md", quoted), [])

    def test_adr_uses_its_own_statuses(self):
        self.assertEqual(self.repo.messages("docs/adr/0001-x.md", adr()), [])
        self.assertTrue(any(m.startswith("status inválido") for m in self.repo.messages("docs/adr/0001-x.md", adr("ativo"))))

    def test_adr_file_name_must_be_numbered(self):
        self.assertIn("ADR deve seguir NNNN-titulo-curto.md", self.repo.messages("docs/adr/x.md", adr()))

    def test_missing_required_section_is_an_error(self):
        body = "**Decisão:** x.\n\n## Contexto\nc\n\n## Consequências\n- b\n"
        self.assertIn("seção obrigatória ausente: ## Alternativas descartadas", self.repo.messages("docs/adr/0001-x.md", adr(body=body)))

    def test_optional_section_may_be_absent(self):
        messages = self.repo.messages("docs/adr/0001-x.md", adr())
        self.assertFalse(any("Substitui" in m for m in messages))

    def test_dash_and_na_are_errors_outside_code(self):
        text = VALID_FRONTMATTER + "# A\numa frase — outra\nvalor: N/A\n`N/A em código`\n```\n— em bloco\n```\n"
        messages = self.repo.messages("docs/a.md", text)
        self.assertEqual(sum(m.startswith("travessão") for m in messages), 1)
        self.assertEqual(sum(m.startswith("N/A") for m in messages), 1)

    def test_broken_relative_link_is_an_error(self):
        self.repo.write("docs/existe.md", VALID_FRONTMATTER + "# E\n")
        text = VALID_FRONTMATTER + "# A\n[ok](existe.md) [ok](existe.md#secao) [web](https://x.y) [quebrado](falta.md)\n"
        self.assertEqual([m for m in self.repo.messages("docs/a.md", text) if m.startswith("link")], ["link quebrado: falta.md"])

    def test_spec_and_tasks_are_recognized_with_their_names(self):
        root = self.repo.root
        self.assertEqual(check_docs.doc_type(root / "docs/specs/0001-x/spec.md", root), "spec")
        self.assertEqual(check_docs.doc_type(root / "docs/specs/0001-x/tasks/01-back-y.md", root), "task")
        self.assertEqual(check_docs.doc_type(root / "docs/specs/0001-x/tasks/03-qa-validacao.md", root), "task-qa")

    def test_task_with_two_layers_or_bad_name_is_an_error(self):
        text = "---\nstatus: rascunho\natualizado: 2026-10-24\ndescricao: d\n---\n# T\n"
        messages = self.repo.messages("docs/specs/0001-x/tasks/01-full-y.md", text)
        self.assertIn("task deve seguir NN-camada-titulo-curto.md, camada back, front ou infra", messages)

    def test_spec_folder_must_be_numbered(self):
        text = "---\nstatus: rascunho\natualizado: 2026-10-24\ndescricao: d\n---\n# S\n"
        self.assertIn("pasta da spec deve seguir NNNN-titulo-curto", self.repo.messages("docs/specs/x/spec.md", text))

    def test_spec_and_task_statuses_come_from_the_standard(self):
        spec = "---\nstatus: concluída\natualizado: 2026-10-24\ndescricao: d\n---\n# S\n"
        task = "---\nstatus: entregue\natualizado: 2026-10-24\ndescricao: d\n---\n# T\n"
        self.assertTrue(any(m.startswith("status inválido") for m in self.repo.messages("docs/specs/0001-x/spec.md", spec)))
        self.assertTrue(any(m.startswith("status inválido") for m in self.repo.messages("docs/specs/0001-x/tasks/01-back-y.md", task)))

    def test_size_above_reference_is_a_warning(self):
        lines = "\n".join(f"linha {i}" for i in range(80))
        findings = check_docs.check_file(self.repo.write("docs/adr/0001-x.md", adr() + lines), self.repo.root)
        self.assertEqual([f.level for f in findings if "referência" in f.message], ["AVISO"])

    def test_files_outside_docs_are_ignored(self):
        self.assertEqual(self.repo.messages("frontend/README.md", "sem nada"), [])


class AreaLayoutTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.repo.write("padroes/documentacao.md", VALID_FRONTMATTER + "# Padrão\n")

    def tearDown(self):
        self.repo.tmp.cleanup()

    def test_area_types_and_skipped_folders(self):
        root = self.repo.root
        self.assertEqual(check_docs.doc_type(root / "regras/garantias.md", root), "regras-modulo")
        self.assertEqual(check_docs.doc_type(root / "areas-vizinhas/simulacao.md", root), "area-vizinha")
        self.assertEqual(check_docs.doc_type(root / "glossario.md", root), "glossario")
        self.assertIsNone(check_docs.doc_type(root / "templates/adr.md", root))
        self.assertIsNone(check_docs.doc_type(root / "projetos/poc/index.md", root))

    def test_placeholder_heading_of_template_is_not_required(self):
        text = VALID_FRONTMATTER + "# Regras de garantias\n\n## Inclusão de gravame\n\n### GAR-01: X\nEnunciado.\n"
        messages = self.repo.messages("regras/garantias.md", text)
        self.assertFalse(any(m.startswith("seção obrigatória ausente") for m in messages))

    def test_links_into_generated_projects_folder_are_not_checked(self):
        messages = self.repo.messages("index.md", VALID_FRONTMATTER + "# I\n[poc](projetos/poc/)\n")
        self.assertEqual(messages, [])


class HookTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.tmp.cleanup()

    def run_hook(self, path):
        stdin = io.StringIO(json.dumps({"tool_input": {"file_path": str(path)}}))
        stdout, stderr = io.StringIO(), io.StringIO()
        return check_docs.run_hook(stdin, stdout, stderr), stdout.getvalue(), stderr.getvalue()

    def test_error_exits_2_with_findings_on_stderr(self):
        code, _, stderr = self.run_hook(self.repo.write("docs/a.md", "# sem frontmatter\n"))
        self.assertEqual(code, 2)
        self.assertIn("frontmatter ausente", stderr)

    def test_clean_doc_exits_0_silently(self):
        self.assertEqual(self.run_hook(self.repo.write("docs/a.md", VALID_FRONTMATTER + "# A\n")), (0, "", ""))

    def test_file_outside_a_repository_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.md"
            path.write_text("# sem frontmatter\n", encoding="utf-8")
            self.assertEqual(self.run_hook(path)[0], 0)


class StandardTest(unittest.TestCase):
    def test_standard_is_parsed(self):
        standard = check_docs.load_standard()
        self.assertEqual(standard["statuses"], {"rascunho", "ativo", "substituído", "obsoleto"})
        self.assertEqual(standard["type_statuses"]["spec"], {"rascunho", "aprovada", "entregue", "substituída"})
        self.assertEqual(standard["type_statuses"]["task"], {"rascunho", "aprovada", "concluída"})
        self.assertEqual(standard["sizes"]["spec"], 150)
        self.assertIsNone(standard["sizes"]["task"])


if __name__ == "__main__":
    unittest.main()
