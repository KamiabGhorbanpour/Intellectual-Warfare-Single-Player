from __future__ import annotations

import unittest

from game_content import (
    AGENT_FOLDERS,
    AZADIKHAH_AGENTS,
    AZADIKHAH_EVENTS,
    EVENT_FOLDERS,
    IRGC_AGENTS,
    IRGC_EVENTS,
    STANDARD_RUN_LENGTH,
)
from game_engine import validate_content


class ContentTests(unittest.TestCase):
    def test_both_factions_have_enough_cards_for_a_standard_run(self) -> None:
        self.assertGreaterEqual(len(AZADIKHAH_EVENTS), STANDARD_RUN_LENGTH)
        self.assertGreaterEqual(len(IRGC_EVENTS), STANDARD_RUN_LENGTH)

    def test_every_event_is_solvable(self) -> None:
        self.assertEqual(validate_content(AZADIKHAH_AGENTS, AZADIKHAH_EVENTS), [])
        self.assertEqual(validate_content(IRGC_AGENTS, IRGC_EVENTS), [])

    def test_every_referenced_image_exists(self) -> None:
        missing: list[str] = []
        for side, agents, events in [
            ("Azadikhah", AZADIKHAH_AGENTS, AZADIKHAH_EVENTS),
            ("IRGC", IRGC_AGENTS, IRGC_EVENTS),
        ]:
            for agent in agents:
                path = AGENT_FOLDERS[side] / agent["image"]
                if not path.is_file():
                    missing.append(str(path))
            for event in events:
                path = EVENT_FOLDERS[side] / event["image"]
                if not path.is_file():
                    missing.append(str(path))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
