from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESOLVE_OUTPUT = REPO_ROOT / "claude/bin/resolve-output"
SKILL_DIR = REPO_ROOT / "claude/skills/shortcuts-playground"
AGENTS = (
    REPO_ROOT / "claude/agents/shortcut-builder.md",
    REPO_ROOT / "claude/agents/shortcut-remixer.md",
)
ALWAYS_READ_BUDGET_BYTES = 25_000
FENCED_BLOCK = re.compile(r"```.*?```", re.S)


def run_resolve(home: Path, *args: str, env: dict | None = None) -> dict[str, str]:
    base_env = {"HOME": str(home), "PATH": os.environ["PATH"]}
    base_env.update(env or {})
    result = subprocess.run(
        [str(RESOLVE_OUTPUT), *args],
        capture_output=True,
        text=True,
        env=base_env,
        check=True,
    )
    return dict(line.split("=", 1) for line in result.stdout.splitlines())


class ResolveOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_unfilled_user_config_placeholders_fall_back_to_defaults(self) -> None:
        values = run_resolve(
            self.home,
            "--output-dir",
            "${user_config.output_dir}",
            "--mode",
            "${user_config.signing_mode}",
        )
        default_dir = self.home / "Documents/Shortcuts Playground"
        self.assertEqual(str(default_dir), values["OUTPUT_DIR"])
        self.assertEqual("anyone", values["SIGNING_MODE"])
        self.assertTrue((default_dir / "drafts").is_dir())

    def test_empty_values_fall_back_to_plugin_option_env_vars(self) -> None:
        custom = self.home / "from-env"
        values = run_resolve(
            self.home,
            "--output-dir",
            "",
            "--mode",
            "",
            env={
                "CLAUDE_PLUGIN_OPTION_OUTPUT_DIR": str(custom),
                "CLAUDE_PLUGIN_OPTION_SIGNING_MODE": "people-who-know-me",
            },
        )
        self.assertEqual(str(custom), values["OUTPUT_DIR"])
        self.assertEqual("people-who-know-me", values["SIGNING_MODE"])

    def test_tilde_and_home_prefixes_expand_to_the_home_directory(self) -> None:
        for raw in ("~/Shortcuts Out", "$HOME/Shortcuts Out"):
            with self.subTest(raw=raw):
                values = run_resolve(self.home, "--output-dir", raw)
                self.assertEqual(str(self.home / "Shortcuts Out"), values["OUTPUT_DIR"])

    def test_configured_values_are_used_as_given(self) -> None:
        target = self.home / "Configured"
        values = run_resolve(
            self.home, "--output-dir", str(target), "--mode", "people-who-know-me"
        )
        self.assertEqual(str(target), values["OUTPUT_DIR"])
        self.assertEqual("people-who-know-me", values["SIGNING_MODE"])
        self.assertTrue((target / "drafts").is_dir())


class AgentInstructionTests(unittest.TestCase):
    def test_user_config_placeholders_only_reach_the_shell_single_quoted(self) -> None:
        for path in AGENTS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(agent=path.name):
                self.assertIn("'${user_config.output_dir}'", text)
                self.assertIn("'${user_config.signing_mode}'", text)
                self.assertNotIn('"${user_config', text)

    def test_skill_signs_with_the_resolved_output_dir_and_mode(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("resolve-output", text)
        self.assertIn('--output-dir "$OUTPUT_DIR"', text)
        self.assertIn('--mode "$SIGNING_MODE"', text)

    def test_skill_routes_schema_gaps_to_the_grounding_helper(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for term in ("lookup_action_grounding.py", "bundled JSON only", "toolkit-parameter-summary"):
            self.assertIn(term, text)

    def test_a_schema_gap_goes_on_the_on_device_checklist_instead_of_stopping(self) -> None:
        texts = [(SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")]
        texts += [path.read_text(encoding="utf-8") for path in AGENTS]
        for text in texts:
            self.assertIn("on-device checklist", text)
        for path in AGENTS:
            self.assertNotIn("Wait for the user's answer", path.read_text(encoding="utf-8"))

    def test_always_read_instructions_fit_the_budget(self) -> None:
        always_read = [SKILL_DIR / "SKILL.md", AGENTS[0]]
        total = sum(path.stat().st_size for path in always_read)
        self.assertLessEqual(total, ALWAYS_READ_BUDGET_BYTES)

    def test_every_relative_link_in_the_skill_and_rules_resolves(self) -> None:
        docs = [SKILL_DIR / "SKILL.md", SKILL_DIR / "BEST_PRACTICES.md", *sorted((SKILL_DIR / "rules").glob("*.md"))]
        for doc in docs:
            body = FENCED_BLOCK.sub("", doc.read_text(encoding="utf-8"))
            for target in re.findall(r"\]\(([^)#:]+)(?:#[^)]*)?\)", body):
                with self.subTest(doc=doc.name, target=target):
                    self.assertTrue((doc.parent / target).exists())


class FormatDateGuidanceTests(unittest.TestCase):
    def test_no_doc_tells_the_agent_to_use_wfdateformatstring(self) -> None:
        for tree in ("claude", "codex"):
            root = REPO_ROOT / tree / "skills/shortcuts-playground"
            for doc in root.glob("*.md"):
                if doc.name == "CHANGELOG.md":
                    continue
                with self.subTest(doc=f"{tree}/{doc.name}"):
                    self.assertFalse("WFDateFormatString" in doc.read_text(encoding="utf-8"))

    def test_toolkit_pattern_shape_passes_the_validator(self) -> None:
        fixture = REPO_ROOT / "tests/fixtures/format-date-custom-pattern.xml"
        for target in ("26", "27"):
            with self.subTest(target_macos=target):
                result = subprocess.run(
                    [str(REPO_ROOT / "claude/bin/validate-shortcut"), str(fixture), "--target-macos", target],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
