from __future__ import annotations

import re
import unittest
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


class LearningExploreGateTest(unittest.TestCase):
    def test_readme_learning_is_not_a_separate_active_skill(self) -> None:
        self.assertFalse(Path(".codex/skills/readme-learning-capture/SKILL.md").exists())

    def test_repo_readme_module_is_self_contained_under_learning_capture(self) -> None:
        text = read(".codex/skills/learning-capture/references/repo-readme.md")

        self.assertNotIn(".codex/skills/readme-learning-capture", text)
        self.assertIn("repo-readme-scorecard.md", text)
        self.assertIn("repo-readme-pressure-scenarios.md", text)
        self.assertTrue(Path(".codex/skills/learning-capture/references/repo-readme-scorecard.md").is_file())
        self.assertTrue(
            Path(".codex/skills/learning-capture/references/repo-readme-pressure-scenarios.md").is_file()
        )

    def test_agents_do_not_route_active_learning_to_retired_readme_skill(self) -> None:
        text = read("AGENTS.md")
        high_frequency = text.split("## Agent Intent Routing", 1)[0]

        self.assertNotIn("readme-learning-capture", high_frequency)

    def test_agents_declares_missing_local_skill_stop_gate(self) -> None:
        text = read("AGENTS.md").lower()

        self.assertIn("missing local skill", text)
        self.assertIn("do not continue as if the skill loaded", text)
        self.assertIn("historical skill name", text)

    def test_agents_skill_routes_reference_existing_local_skill_paths(self) -> None:
        text = read("AGENTS.md")
        paths = sorted(set(re.findall(r"`(\.codex/skills/[^`]+/SKILL\.md)`", text)))

        self.assertTrue(paths)
        self.assertEqual([path for path in paths if not Path(path).is_file()], [])

    def test_openspec_explore_defines_read_only_exit_boundary(self) -> None:
        text = read(".codex/skills/openspec-explore/SKILL.md").lower()

        self.assertIn("explicit `$openspec-explore`", text)
        self.assertIn("read-only exploration stance", text)
        self.assertIn("not implementation permission", text)
        self.assertIn("exit explore", text)
        self.assertIn("must not edit", text)


if __name__ == "__main__":
    unittest.main()
