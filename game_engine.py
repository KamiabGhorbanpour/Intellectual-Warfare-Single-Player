"""Pure game rules for the Intellectual Warfare solo arcade mode.

This module deliberately has no NiceGUI dependency, which keeps the scoring
rules easy to test and modify independently from the interface.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from random import Random, SystemRandom
from typing import Any


def evaluate_attempt(
    event: dict[str, Any],
    selected_agents: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate one irreversible, scored attempt.

    The player must assign the exact number of agents printed as the requirement.
    The mission passes when at least half of the assigned agents, rounded up,
    share at least one trait with the card's hidden solution traits.
    """

    required_count = int(event["requirement"])
    if len(selected_agents) != required_count:
        raise ValueError(f"Select exactly {required_count} agent(s).")

    required_traits = set(event["traits"])
    agent_results: list[dict[str, Any]] = []

    for agent in selected_agents:
        matching_traits = sorted(set(agent["traits"]) & required_traits)
        agent_results.append(
            {
                "id": agent["id"],
                "name": agent["name"],
                "matching_traits": matching_traits,
                "matched": bool(matching_traits),
            }
        )

    matched_count = sum(1 for result in agent_results if result["matched"])
    pass_threshold = (required_count + 1) // 2
    success = matched_count >= pass_threshold
    return {
        "event_id": event["id"],
        "event": event["name"],
        "success": success,
        "points": 1 if success else 0,
        "required_count": required_count,
        "matched_count": matched_count,
        "pass_threshold": pass_threshold,
        "required_traits": sorted(required_traits),
        "agents": agent_results,
    }


def shuffled_run(
    events: Sequence[dict[str, Any]],
    length: int,
    *,
    rng: Random | SystemRandom | None = None,
) -> list[dict[str, Any]]:
    """Return a shuffled run without mutating the source deck."""

    if length < 1:
        raise ValueError("Run length must be at least one card.")
    if length > len(events):
        raise ValueError("Run length cannot exceed the available deck.")

    randomizer = rng or SystemRandom()
    return randomizer.sample(list(events), length)


def run_rank(score: int, total: int) -> str:
    """Return a compact arcade rank for the final score."""

    if total < 1:
        return "Unranked"
    accuracy = score / total
    if accuracy == 1:
        return "Perfect Strategist"
    if accuracy >= 0.8:
        return "Master Analyst"
    if accuracy >= 0.6:
        return "Field Operative"
    if accuracy >= 0.4:
        return "Developing Analyst"
    return "Recruit"


def validate_content(
    agents: Iterable[dict[str, Any]],
    events: Iterable[dict[str, Any]],
) -> list[str]:
    """Report data problems that would make an arcade card unfair or invalid."""

    agent_list = list(agents)
    event_list = list(events)
    problems: list[str] = []

    agent_ids = [agent["id"] for agent in agent_list]
    event_ids = [event["id"] for event in event_list]
    if len(agent_ids) != len(set(agent_ids)):
        problems.append("Agent IDs must be unique.")
    if len(event_ids) != len(set(event_ids)):
        problems.append("Event IDs must be unique.")

    for event in event_list:
        requirement = int(event["requirement"])
        matching_agents = [
            agent
            for agent in agent_list
            if set(agent["traits"]) & set(event["traits"])
        ]
        pass_threshold = (requirement + 1) // 2
        if requirement < 1:
            problems.append(f"{event['id']} has an invalid requirement.")
        elif len(matching_agents) < pass_threshold:
            problems.append(
                f"{event['id']} needs at least {pass_threshold} matching agent(s) "
                f"to pass but only {len(matching_agents)} are available."
            )

    return problems
