from __future__ import annotations

import unittest
from random import Random

from game_engine import evaluate_attempt, run_rank, shuffled_run, validate_content


class GameEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agents = [
            {"id": "a", "name": "A", "traits": ["curiosity"]},
            {"id": "b", "name": "B", "traits": ["humility"]},
            {"id": "c", "name": "C", "traits": ["obstinacy"]},
        ]
        self.event = {
            "id": "event",
            "name": "Test Event",
            "traits": ["curiosity", "humility"],
            "requirement": 2,
        }

    def test_correct_attempt_scores_one(self) -> None:
        result = evaluate_attempt(self.event, self.agents[:2])
        self.assertTrue(result["success"])
        self.assertEqual(result["points"], 1)

    def test_one_wrong_agent_fails_entire_attempt(self) -> None:
        result = evaluate_attempt(self.event, [self.agents[0], self.agents[2]])
        self.assertFalse(result["success"])
        self.assertEqual(result["points"], 0)

    def test_exact_requirement_is_enforced(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_attempt(self.event, [self.agents[0]])

    def test_shuffled_run_does_not_mutate_source(self) -> None:
        events = [{"id": str(index)} for index in range(12)]
        original = list(events)
        run = shuffled_run(events, 10, rng=Random(42))
        self.assertEqual(len(run), 10)
        self.assertEqual(events, original)
        self.assertEqual(len({event["id"] for event in run}), 10)

    def test_rank_boundaries(self) -> None:
        self.assertEqual(run_rank(10, 10), "Perfect Strategist")
        self.assertEqual(run_rank(8, 10), "Master Analyst")
        self.assertEqual(run_rank(6, 10), "Field Operative")
        self.assertEqual(run_rank(4, 10), "Developing Analyst")
        self.assertEqual(run_rank(3, 10), "Recruit")

    def test_validation_catches_an_unsolvable_card(self) -> None:
        problems = validate_content(
            self.agents,
            [{"id": "bad", "name": "Bad", "traits": ["justice"], "requirement": 1}],
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("only 0 are available", problems[0])


if __name__ == "__main__":
    unittest.main()
