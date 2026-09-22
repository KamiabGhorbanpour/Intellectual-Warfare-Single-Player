from __future__ import annotations

from pathlib import Path
from random import Random
from urllib.parse import quote
import os

# ============================================================
# CONFIG
# ============================================================
# A standard arcade run always contains the same number of cards so scores are comparable.
STANDARD_RUN_LENGTH = 10
POINTS_PER_SUCCESS = 1

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
AGENT_FOLDERS = {
    "Azadikhah": ASSET_DIR / "agents" / "azadikhah",
    "IRGC": ASSET_DIR / "agents" / "irgc",
}
EVENT_FOLDERS = {
    "Azadikhah": ASSET_DIR / "events" / "azadikhah",
    "IRGC": ASSET_DIR / "events" / "irgc",
}

APP_HOST = os.getenv("HOST", "0.0.0.0")
APP_PORT = int(os.getenv("PORT", "8080"))
STORAGE_SECRET = os.getenv("STORAGE_SECRET", "local-intellectual-warfare-arcade-secret")
RNG = Random()

STATIC_ROUTES = {
    "Azadikhah_agents": "/assets/agents/azadikhah",
    "IRGC_agents": "/assets/agents/irgc",
    "Azadikhah_events": "/assets/events/azadikhah",
    "IRGC_events": "/assets/events/irgc",
}


# ============================================================
# HELPERS
# ============================================================
def trait(value: str) -> str:
    """Normalize trait names so matching is reliable."""
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def pretty_trait(value: str) -> str:
    return value.replace("_", " ").title()


def image_url(route: str, filename: str) -> str:
    return f"{route}/{quote(filename)}"


def static_folders() -> list[tuple[str, Path]]:
    """Return the URL and local path for each supplied artwork folder."""
    return [
        (STATIC_ROUTES["Azadikhah_agents"], AGENT_FOLDERS["Azadikhah"]),
        (STATIC_ROUTES["IRGC_agents"], AGENT_FOLDERS["IRGC"]),
        (STATIC_ROUTES["Azadikhah_events"], EVENT_FOLDERS["Azadikhah"]),
        (STATIC_ROUTES["IRGC_events"], EVENT_FOLDERS["IRGC"]),
    ]


# ============================================================
# AGENTS
# ============================================================
IRGC_AGENTS = [
    {
        "id": "IRGC-AGENT-001",
        "name": "Agent Farhad",
        "image": "Agent Farhad.png",
        "traits": [trait("Thoroughness"), trait("Curiosity")],
    },
    {
        "id": "IRGC-AGENT-002",
        "name": "Ayatollah Fellahin",
        "image": "Ayatollah Fellahin.png",
        "traits": [trait("Epistemic Justice"), trait("Legitimacy Awareness")],
    },
    {
        "id": "IRGC-AGENT-003",
        "name": "Ayatollah Guguli",
        "image": "Ayatollah Guguli.png",
        "traits": [trait("Arrogance"), trait("Epistemic Cowardice")],
    },
    {
        "id": "IRGC-AGENT-004",
        "name": "Agent Khani",
        "image": "Agent Khani.png",
        "traits": [trait("Intellectual Humility"), trait("Confirmation Bias")],
    },
    {
        "id": "IRGC-AGENT-005",
        "name": "Agent Mojredi",
        "image": "Agent Mojredi.png",
        "traits": [trait("Open-mindedness"), trait("Binary Thinking")],
    },
    {
        "id": "IRGC-AGENT-006",
        "name": "Agent Moradi",
        "image": "Agent Moradi.png",
        "traits": [trait("Close-mindedness"), trait("Obstinacy")],
    },
    {
        "id": "IRGC-AGENT-007",
        "name": "Agent Iranshahi",
        "image": "Agent Iranshahi.png",
        "traits": [trait("Epistemic Authoritarianism"), trait("Arrogance")],
    },
]

AZADIKHAH_AGENTS = [
    {
        "id": "AZAD-AGENT-001",
        "name": "Agent 47",
        "image": "Agent 47.png",
        "traits": [trait("Thoroughness"), trait("Curiosity")],
    },
    {
        "id": "AZAD-AGENT-002",
        "name": "Agent Nazafarin",
        "image": "Agent Nazafarin.png",
        "traits": [trait("Epistemic Justice"), trait("Intellectual Courage")],
    },
    {
        "id": "AZAD-AGENT-003",
        "name": "Agent Pashinyan",
        "image": "Agent Pashinyan.png",
        "traits": [trait("Open-mindedness"), trait("Intellectual Humility")],
    },
    {
        "id": "AZAD-AGENT-004",
        "name": "Agent Musazad",
        "image": "Agent Musazad.png",
        "traits": [trait("Intellectual Integrity"), trait("Intellectual Empathy")],
    },
    {
        "id": "AZAD-AGENT-005",
        "name": "Agent Muabi",
        "image": "Agent Muabi.png",
        "traits": [trait("Intellectual Courage"), trait("Intellectual Humility")],
    },
    {
        "id": "AZAD-AGENT-006",
        "name": "Agent Kolahkaj",
        "image": "Agent Kolahkaj.png",
        "traits": [trait("Open-mindedness"), trait("Epistemic Justice")],
    },
]


# ============================================================
# EVENTS
# requirement = how many assigned agents must have at least one matching trait.
# longevity = how many End Turn clicks the event takes once it has agents assigned.
# ============================================================
AZADIKHAH_EVENTS = [
    {
        "id": "AZAD-EVENT-001",
        "name": "Viral Clip Verification",
        "image": "1.png",
        "text": "A viral clip appears to show the IRGC committing a shocking abuse. It is emotionally powerful and immediately useful for morale and recruitment. A junior analyst says the time stamps and audio feel wrong.",
        "traits": [trait("Intellectual Humility")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-002",
        "name": "Basij Center Investigation",
        "image": "2.png",
        "text": "A Basij center has been taken over by the Azadikhahs. We need to send someone to investigate the center for information that could be used for further operations.",
        "traits": [trait("Thoroughness")],
        "requirement": 1,
        "longevity": 2,
    },
    {
        "id": "AZAD-EVENT-003",
        "name": "The True Nationalists",
        "image": "3.png",
        "text": "Persian nationalism has always been a political tool for people to use and abuse. Many fight on the side of the regime because they feel it protects their homeland. We should show them that they need not feel threatened by us, and that we are the true nationalists.",
        "traits": [trait("Epistemic Justice"), trait("Intellectual Courage"), trait("Open-mindedness")],
        "requirement": 3,
        "longevity": 2,
    },
    {
        "id": "AZAD-EVENT-004",
        "name": "Morality Police Crackdown",
        "image": "4.png",
        "text": "The morality police have increased their subjugation of women. We should use this opportunity to encourage more disenfranchised women to join our cause.",
        "traits": [trait("Epistemic Justice")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-005",
        "name": "Spies Among Us",
        "image": "5.png",
        "text": "There are reports that the IRGC has planted spies among the Azadikhahs. We need someone who can weed them out quickly before they sabotage anything.",
        "traits": [trait("Thoroughness"), trait("Curiosity")],
        "requirement": 1,
        "longevity": 2,
    },
    {
        "id": "AZAD-EVENT-006",
        "name": "Post-Revolutionary Iran",
        "image": "6.png",
        "text": "People are concerned about the post-revolutionary Iran. What type of society will it be? We need someone to lay out a more precise plan on how the future Iran will look.",
        "traits": [trait("Curiosity"), trait("Open-mindedness"), trait("Intellectual Courage")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-007",
        "name": "Burning Mosques PR Crisis",
        "image": "7.png",
        "text": "The burning of mosques has become a serious issue for many Azadikhahs. While some argue that it is acceptable because many bases of oppression are stationed in mosques, others argue that it will not reflect well on the movement. We need people to handle the PR around this properly.",
        "traits": [trait("Epistemic Justice"), trait("Intellectual Courage")],
        "requirement": 3,
        "longevity": 2,
    },
    {
        "id": "AZAD-EVENT-008",
        "name": "Eye-Shooting Counterstrategy",
        "image": "8.png",
        "text": "A common tactic used by the IRGC is to shoot Azadikhahs in the eyes. This way, they do not need to kill them, but can still eliminate them as a threat. We need someone to come up with a counterstrategy to overcome this hurdle.",
        "traits": [trait("Intellectual Integrity"), trait("Intellectual Empathy")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-009",
        "name": "Reza Pahlavi Dispute",
        "image": "9.png",
        "text": "Reza Pahlavi is a very debated topic among Azadikhahs. Is he the trusted leader of the movement? Or is he tyrant in making? We need someone to reconcile the monarchists and non-monarchists to fight for a common cause.",
        "traits": [trait("Intellectual Humility")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-010",
        "name": "Information Under Shutdown",
        "image": "10.png",
        "text": "Distribution of information is of utmost importance. We need someone who could change the narrative while the internet is down using unusual means.",
        "traits": [trait("Curiosity"), trait("Open-mindedness")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-011",
        "name": "Corruption Graphic Verification",
        "image": "11.png",
        "text": "A graphic showing corruption among senior officials is spreading rapidly through activist channels. The figures are shocking, but nobody can identify where the numbers came from or who produced the graphic. We need someone to determine whether the claims are trustworthy before we amplify them.",
        "traits": [trait("Intellectual Humility"), trait("Intellectual Integrity")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-012",
        "name": "Nationalists And Socialists",
        "image": "12.png",
        "text": "There has always been diversity among the Azadikhahs. However, nationalists and socialists are growing more and more resentful of one another. We need someone who could calm everyone down.",
        "traits": [trait("Open-mindedness"), trait("Intellectual Humility"), trait("Intellectual Courage")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-013",
        "name": "Prison Video Leak Plan",
        "image": "13.png",
        "text": "A plan has been set in motion to hack the prison and release the brutal videos of torture to the public. We need agents who are to be trusted to do the deeds.",
        "traits": [trait("Intellectual Integrity"), trait("Intellectual Courage")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "AZAD-EVENT-014",
        "name": "Woman, Life, Freedom Slogan",
        "image": "14.png",
        "text": "While the Woman, Life, Freedom motto is widely used, some oppose this motto as it excludes men, and prefer other slogans. This might cause a division among Azadikhahs. We should find a way to stop this from happening using a trusted agent.",
        "traits": [trait("Epistemic Justice"), trait("Intellectual Courage")],
        "requirement": 1,
        "longevity": 1,
    },
]

IRGC_EVENTS = [
    {
        "id": "IRGC-EVENT-001",
        "name": "Park-e Daneshju Network",
        "image": "1.png",
        "text": "Sexually deviant youth is using Park-e Daneshju as a hub to grow and support one another against the government's anti-gay laws. We should send people to either convince them to stop or crack down on them hard.",
        "traits": [trait("Arrogance"), trait("Epistemic Justice")],
        "requirement": 3,
        "longevity": 2,
    },
    {
        "id": "IRGC-EVENT-002",
        "name": "Hijab Defiance Incident",
        "image": "2.png",
        "text": "A woman wearing improper clothing has appeared in public in defiance of the mandatory hijab law. Send someone who could handle the situation without causing unrest.",
        "traits": [trait("Open-mindedness"), trait("Epistemic Cowardice"), trait("Arrogance")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-003",
        "name": "Green Movement-Style Unrest",
        "image": "3.png",
        "text": "Social unrest in the center of Tehran has been reported. The rebels' socio-economic situation matches those from the Green Movement. Send someone to handle this by any means possible.",
        "traits": [trait("Intellectual Humility"), trait("Curiosity")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-004",
        "name": "Persian Gulf Strike Footage",
        "image": "4.png",
        "text": "A dramatic video appears showing an alleged military strike in the Persian Gulf. The footage spreads rapidly. We need confirmation.",
        "traits": [trait("Thoroughness"), trait("Curiosity")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-005",
        "name": "University Thesis Controversy",
        "image": "5.png",
        "text": "At Tehran University, a controversial thesis by Leila Husseinzadeh is widely condemned due to its take on Kurdish and Turkish nationalism. Most students loudly criticize it. You need spies to calm the situation.",
        "traits": [trait("Epistemic Cowardice"), trait("Arrogance")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-006",
        "name": "Esther And Mordechai Attack",
        "image": "6.png",
        "text": "There has been an antisemitic attack on the famous tomb of Esther and Mordechai. We could use this to amplify the anger into broader antisemitic/antizionist protests and perhaps recruit some new faces.",
        "traits": [trait("Obstinacy"), trait("Close-mindedness"), trait("Epistemic Cowardice")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-007",
        "name": "Cyrus Tomb Gathering",
        "image": "7.png",
        "text": "A mass of people have gathered around Cyrus' tomb and it has been flagged to start a nationalist anti-government protest. Someone needs to go to prevent this from happening.",
        "traits": [trait("Binary Thinking")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-008",
        "name": "Reformist Concessions Debate",
        "image": "8.png",
        "text": "The reformists are saying that we need to make some concessions to the people, but that's how the Shah fell, didn't he? We should send someone to figure out what is the best course of action.",
        "traits": [trait("Intellectual Humility"), trait("Legitimacy Awareness")],
        "requirement": 1,
        "longevity": 2,
    },
    {
        "id": "IRGC-EVENT-009",
        "name": "Anti-Government House",
        "image": "9.png",
        "text": "An anti-government house has been discovered and we need to send someone suitable to find clues in case they were coordinating with other anti-government folks.",
        "traits": [trait("Thoroughness")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-010",
        "name": "Bazaari Class Protests",
        "image": "10.png",
        "text": "The Bazaari class, the backbone of the Islamic Republic, is protesting against the economic crisis. To handle this, we need to persuade the Bazaari elites to put an end to the protests before things get ugly.",
        # This card requires three agents. The original single-trait solution
        # had only one eligible IRGC agent, so no legal selection could win.
        "traits": [
            trait("Epistemic Justice"),
            trait("Intellectual Humility"),
            trait("Open-mindedness"),
        ],
        "requirement": 3,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-011",
        "name": "Grand Ayatollah Household",
        "image": "11.png",
        "text": "Some protestors have been targeting a famous grand Ayatollah's household. We need agents who could defuse the situation by any means necessary. If we cannot protect our grand Ayatollahs, then what are we doing?",
        "traits": [trait("Legitimacy Awareness"), trait("Epistemic Justice"), trait("Arrogance")],
        "requirement": 2,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-012",
        "name": "Exploit Kurdish Nationalist Split",
        "image": "12.png",
        "text": "Divide and conquer is a classic strategy for overcoming your enemy. The Kurdish nationalist movement and much of the anti-government movement do not see eye to eye. It is time to exploit this by infiltrating the nationalist movement.",
        "traits": [trait("Confirmation Bias"), trait("Intellectual Humility"), trait("Binary Thinking")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-013",
        "name": "Climate And Energy Crisis",
        "image": "13.png",
        "text": "The climate problems and the energy crisis have devastated much of the population. We need to handle this before it turns into a political issue. But there are many aspects of the problem we are not yet fully aware of sadly.",
        # The original source used "Epistemic Humility", but no IRGC agent has
        # that trait. "Intellectual Humility" preserves the intended mechanic
        # and makes the card solvable by Agent Khani.
        "traits": [trait("Intellectual Humility")],
        "requirement": 1,
        "longevity": 3,
    },
    {
        "id": "IRGC-EVENT-014",
        "name": "Internet Situation",
        "image": "14.png",
        "text": "Knowledge is power, and at this moment, we need someone who can handle the internet situation. Depriving people of access to information is necessary when the regime is in danger.",
        "traits": [trait("Epistemic Authoritarianism"), trait("Epistemic Cowardice")],
        "requirement": 1,
        "longevity": 1,
    },
    {
        "id": "IRGC-EVENT-015",
        "name": "Narrative Manufacturing",
        "image": "15.png",
        "text": "Controlling the narrative is of utmost importance in times of turmoil. We need to manufacture a variety of narratives that make us look good and the enemy look bad. Perhaps they are Mossad agents, the CIA, or even funded by intergalactic mobsters?",
        "traits": [trait("Open-mindedness"), trait("Curiosity"), trait("Thoroughness")],
        "requirement": 1,
        "longevity": 1,
    },
]


# ============================================================
# GAME STATE
# ============================================================
LEGACY_MULTIPLAYER_REFERENCE = r'''
GROUPS: dict[str, dict[str, Any]] = {}
RESULTS: list[dict[str, Any]] = []
DECISION_HISTORY: list[dict[str, Any]] = []
PAGES: dict[str, Any] = {}
STATE_LOCK = RLock()


STYLE_HTML = """
<style>
body {
    background: #0f172a;
    color: white;
}
.card {
    background: #1e293b;
    border-radius: 16px;
    padding: 12px;
}
.event-card {
    width: 470px;
}
.agent-card {
    width: 270px;
}
.image-frame {
    background: #020617;
    border-radius: 12px;
}
.assignment-panel {
    background: #0f172a;
    border-radius: 12px;
    padding: 10px;
}
.small-muted {
    color: #cbd5e1;
}
.result-success {
    border-left: 6px solid #22c55e;
}
.result-failure {
    border-left: 6px solid #ef4444;
}
.in-progress {
    border-left: 6px solid #f59e0b;
}
.finished-banner {
    background: #14532d;
    border-radius: 16px;
    padding: 16px;
}
.warning-banner {
    background: #7c2d12;
    border-radius: 16px;
    padding: 16px;
}
</style>
"""


def add_style() -> None:
    ui.add_head_html(STYLE_HTML)


def side_agents(side: str) -> list[dict[str, Any]]:
    return IRGC_AGENTS if side == "IRGC" else AZADIKHAH_AGENTS


def side_events(side: str) -> list[dict[str, Any]]:
    return IRGC_EVENTS if side == "IRGC" else AZADIKHAH_EVENTS


def prepare_agent(agent: dict[str, Any]) -> dict[str, Any]:
    prepared = deepcopy(agent)
    prepared["status"] = "available"
    prepared["mission"] = None
    return prepared


def prepare_event(event: dict[str, Any]) -> dict[str, Any]:
    prepared = deepcopy(event)
    prepared["remaining"] = prepared["longevity"]
    prepared["agents"] = []
    prepared["drawn_round"] = None
    prepared["started_round"] = None
    return prepared


def draw_to_three(group: dict[str, Any]) -> None:
    while len(group["active_events"]) < ACTIVE_EVENTS_PER_TURN and group["deck"]:
        event = group["deck"].pop(0)
        event["drawn_round"] = group["round"]
        group["active_events"].append(event)
        DECISION_HISTORY.append(
            {
                "time": now_stamp(),
                "round": group["round"],
                "group": group["id"],
                "side": group["side"],
                "action": "draw_event",
                "event": event["name"],
            }
        )


def make_group(group_id: str, side: str) -> dict[str, Any]:
    deck = [prepare_event(event) for event in side_events(side)]
    if RANDOMIZE_DECKS:
        shuffle(deck)

    group = {
        "id": group_id,
        "side": side,
        "round": 1,
        "score": 0,
        "agents": [prepare_agent(agent) for agent in side_agents(side)],
        "deck": deck,
        "active_events": [],
        "finished": False,
    }
    draw_to_three(group)
    return group


def initialize_groups() -> None:
    GROUPS.clear()
    count_per_side = 3 if NUMBER_OF_GROUPS == 6 else 2

    for number in range(1, count_per_side + 1):
        GROUPS[f"irgc-{number}"] = make_group(f"irgc-{number}", "IRGC")
        GROUPS[f"azadikhah-{number}"] = make_group(f"azadikhah-{number}", "Azadikhah")


# ============================================================
# SQLITE PERSISTENCE
# ============================================================
def initialize_database() -> None:
    """Create the local SQLite table used for persistent online game state."""
    with sqlite3.connect(STATE_DB_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS game_state (
                id TEXT PRIMARY KEY,
                version INTEGER NOT NULL,
                saved_at TEXT NOT NULL,
                state_json TEXT NOT NULL
            )
            """
        )
        connection.commit()


def private_game_snapshot() -> dict[str, Any]:
    """Return the full server-side state, including hidden mechanics needed to resume."""
    return {
        "saved_at": now_stamp(),
        "version": GAME_STATE_VERSION,
        "config": {
            "number_of_groups": NUMBER_OF_GROUPS,
            "active_events_per_turn": ACTIVE_EVENTS_PER_TURN,
            "randomize_decks": RANDOMIZE_DECKS,
            "points_per_success": POINTS_PER_SUCCESS,
        },
        "groups": GROUPS,
        "results": RESULTS,
        "decision_history": DECISION_HISTORY,
    }


def save_private_state() -> None:
    """Save the live game to SQLite. This is called automatically after game actions."""
    snapshot = private_game_snapshot()
    state_json = json.dumps(snapshot, ensure_ascii=False)
    with sqlite3.connect(STATE_DB_FILE) as connection:
        connection.execute(
            """
            INSERT INTO game_state (id, version, saved_at, state_json)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                version = excluded.version,
                saved_at = excluded.saved_at,
                state_json = excluded.state_json
            """,
            (GAME_STATE_ID, GAME_STATE_VERSION, snapshot["saved_at"], state_json),
        )
        connection.commit()


def load_private_state() -> bool:
    """Load the saved game from SQLite. Return False when no saved game exists."""
    if not STATE_DB_FILE.exists():
        return False

    with sqlite3.connect(STATE_DB_FILE) as connection:
        row = connection.execute(
            "SELECT state_json FROM game_state WHERE id = ?",
            (GAME_STATE_ID,),
        ).fetchone()

    if not row:
        return False

    try:
        snapshot = json.loads(row[0])
        loaded_groups = snapshot.get("groups")
        if not isinstance(loaded_groups, dict):
            return False

        GROUPS.clear()
        GROUPS.update(loaded_groups)

        RESULTS.clear()
        RESULTS.extend(snapshot.get("results", []))

        DECISION_HISTORY.clear()
        DECISION_HISTORY.extend(snapshot.get("decision_history", []))
        return True
    except Exception as error:
        print(f"WARNING: could not load saved game state: {error}")
        return False


def save_all_state() -> None:
    """Save both the private SQLite state and the player-safe public JSON export."""
    with STATE_LOCK:
        save_private_state()
        save_history()


def start_or_load_game() -> None:
    """Start a new game only when no saved SQLite state exists."""
    initialize_database()
    if load_private_state():
        # Keep the public JSON export in sync after a server restart.
        save_history()
        print(f"Loaded saved game from {STATE_DB_FILE}")
    else:
        initialize_groups()
        save_all_state()
        print(f"Started new game and saved it to {STATE_DB_FILE}")


# ============================================================
# SAVE / RESET
# ============================================================
def public_group_snapshot(group: dict[str, Any]) -> dict[str, Any]:
    """Return only player-safe state for the saved history file."""
    event_name_by_id = {event["id"]: event["name"] for event in group["active_events"]}

    return {
        "id": group["id"],
        "side": group["side"],
        "round": group["round"],
        "score": group["score"],
        "finished": group["finished"],
        "deck_remaining": len(group["deck"]),
        "active_events": [
            {
                "id": event["id"],
                "name": event["name"],
                "image": event["image"],
                "drawn_round": event.get("drawn_round"),
                "started_round": event.get("started_round"),
                "assigned_agents": [agent["name"] for agent in assigned_agents_for_event(group, event)],
            }
            for event in group["active_events"]
        ],
        "agents": [
            {
                "id": agent["id"],
                "name": agent["name"],
                "image": agent["image"],
                "status": agent["status"],
                "assigned_event": event_name_by_id.get(agent.get("mission")),
            }
            for agent in group["agents"]
        ],
    }


def current_game_snapshot() -> dict[str, Any]:
    return {
        "saved_at": now_stamp(),
        "config": {
            "number_of_groups": NUMBER_OF_GROUPS,
            "active_events_per_turn": ACTIVE_EVENTS_PER_TURN,
            "randomize_decks": RANDOMIZE_DECKS,
            "points_per_success": POINTS_PER_SUCCESS,
        },
        "groups": {group_id: public_group_snapshot(group) for group_id, group in GROUPS.items()},
        "results": RESULTS,
        "decision_history": DECISION_HISTORY,
    }


def save_history() -> None:
    HISTORY_FILE.write_text(
        json.dumps(current_game_snapshot(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_history_with_notice() -> None:
    save_all_state()
    ui.notify(f"Game saved to SQLite and public history exported to {HISTORY_FILE}", type="positive", timeout=6000)


def reset_everything() -> None:
    RESULTS.clear()
    DECISION_HISTORY.clear()
    initialize_groups()
    save_all_state()
    refresh_all_pages()
    ui.notify("Whole game reset.", type="warning", timeout=4000)


def reset_group(group_id: str) -> None:
    side = GROUPS[group_id]["side"]
    GROUPS[group_id] = make_group(group_id, side)

    RESULTS[:] = [result for result in RESULTS if result["group"] != group_id]
    DECISION_HISTORY.append(
        {
            "time": now_stamp(),
            "round": 1,
            "group": group_id,
            "side": side,
            "action": "reset_group",
        }
    )
    save_all_state()
    refresh_group(group_id)
    ui.notify(f"{group_id} reset.", type="warning", timeout=4000)


# ============================================================
# LOOKUPS AND REFRESHING
# ============================================================
def get_agent(group: dict[str, Any], agent_id: str) -> dict[str, Any] | None:
    return next((agent for agent in group["agents"] if agent["id"] == agent_id), None)


def get_event(group: dict[str, Any], event_id: str) -> dict[str, Any] | None:
    return next((event for event in group["active_events"] if event["id"] == event_id), None)


def refresh_group(group_id: str) -> None:
    refresh = PAGES.get(group_id)
    if refresh:
        refresh()


def refresh_all_pages() -> None:
    for refresh in list(PAGES.values()):
        refresh()


def available_agents(group: dict[str, Any]) -> list[dict[str, Any]]:
    return [agent for agent in group["agents"] if agent["status"] == "available"]


def assigned_agents_for_event(group: dict[str, Any], event: dict[str, Any]) -> list[dict[str, Any]]:
    return [agent for agent in group["agents"] if agent["id"] in event["agents"]]


def event_is_in_progress(event: dict[str, Any]) -> bool:
    """An event is in progress after at least one End Turn has advanced it."""
    return bool(event["agents"]) and event["remaining"] < event["longevity"]


def event_assignment_limit(event: dict[str, Any]) -> int:
    """The card requirement is also the maximum number of assignable agents."""
    return int(event.get("requirement", 0))


def event_has_open_assignment_slot(event: dict[str, Any]) -> bool:
    return len(event["agents"]) < event_assignment_limit(event)


def event_can_accept_agent(event: dict[str, Any]) -> bool:
    # Once the event has started, its assigned agents are locked until resolution.
    return event_has_open_assignment_slot(event) and not event_is_in_progress(event)


def group_is_finished(group: dict[str, Any]) -> bool:
    return not group["deck"] and not group["active_events"]


# ============================================================
# CORE GAME ACTIONS
# ============================================================
def dispatch(group_id: str, agent_id: str, event_id: str) -> None:
    group = GROUPS[group_id]
    agent = get_agent(group, agent_id)
    event = get_event(group, event_id)

    if not agent or not event:
        return

    if agent["status"] != "available":
        ui.notify(f"{agent['name']} is already assigned.", type="warning", timeout=4000)
        return

    if event_is_in_progress(event):
        ui.notify("This card is already in progress. Assigned agents are locked until it resolves.", type="warning", timeout=5000)
        return

    if not event_has_open_assignment_slot(event):
        ui.notify("This card already has the maximum number of agents allowed by its requirement.", type="warning", timeout=5000)
        return

    agent["status"] = "assigned"
    agent["mission"] = event_id

    if agent_id not in event["agents"]:
        event["agents"].append(agent_id)

    DECISION_HISTORY.append(
        {
            "time": now_stamp(),
            "round": group["round"],
            "group": group_id,
            "side": group["side"],
            "action": "assign_agent",
            "agent": agent["name"],
            "event": event["name"],
        }
    )

    save_all_state()
    refresh_group(group_id)


def unassign_agent(group_id: str, agent_id: str) -> None:
    group = GROUPS[group_id]
    agent = get_agent(group, agent_id)

    if not agent or agent["status"] != "assigned":
        return

    event_id = agent.get("mission")
    event = get_event(group, event_id) if event_id else None
    event_name = event["name"] if event else "Unknown event"

    if event and event_is_in_progress(event):
        ui.notify("This card is already in progress. Assigned agents are locked until it resolves.", type="warning", timeout=5000)
        return

    if event and agent_id in event["agents"]:
        event["agents"].remove(agent_id)

    agent["status"] = "available"
    agent["mission"] = None

    DECISION_HISTORY.append(
        {
            "time": now_stamp(),
            "round": group["round"],
            "group": group_id,
            "side": group["side"],
            "action": "unassign_agent",
            "agent": agent["name"],
            "event": event_name,
        }
    )

    save_all_state()
    refresh_group(group_id)


def resolve_event(group_id: str, event: dict[str, Any]) -> None:
    group = GROUPS[group_id]
    assigned_agents = assigned_agents_for_event(group, event)
    required_traits = set(event["traits"])

    matching_agents = []
    non_matching_agents = []

    for agent in assigned_agents:
        matches = sorted(set(agent["traits"]) & required_traits)
        if matches:
            matching_agents.append({"agent": agent["name"], "traits": matches})
        else:
            non_matching_agents.append(agent["name"])

    success = len(matching_agents) >= event["requirement"]
    points = POINTS_PER_SUCCESS if success else 0
    group["score"] += points

    result = {
        "time": now_stamp(),
        "round": group["round"],
        "group": group_id,
        "side": group["side"],
        "event_id": event["id"],
        "event": event["name"],
        "success": success,
        "points": points,
        "assigned_agents": [agent["name"] for agent in assigned_agents],
        "drawn_round": event.get("drawn_round"),
        "started_round": event.get("started_round"),
        "resolved_round": group["round"],
    }
    RESULTS.append(result)
    DECISION_HISTORY.append({**result, "action": "resolve_event"})

    for agent in assigned_agents:
        agent["status"] = "available"
        agent["mission"] = None

    if event in group["active_events"]:
        group["active_events"].remove(event)

    ui.notify(
        f"{'SUCCESS' if success else 'FAILED'}: {event['name']}",
        type="positive" if success else "negative",
        timeout=6000,
    )


def advance_round(group_id: str) -> None:
    group = GROUPS[group_id]

    if group_is_finished(group):
        group["finished"] = True
        save_all_state()
        refresh_group(group_id)
        ui.notify("This group's deck is finished.", type="positive", timeout=5000)
        return

    progressed_events = []
    skipped_events = []

    for event in group["active_events"]:
        if event["agents"]:
            if event["started_round"] is None:
                event["started_round"] = group["round"]
            event["remaining"] -= 1
            progressed_events.append(event)
        else:
            skipped_events.append(event)

    DECISION_HISTORY.append(
        {
            "time": now_stamp(),
            "round": group["round"],
            "group": group_id,
            "side": group["side"],
            "action": "end_turn",
            "progressed_events": [event["name"] for event in progressed_events],
            "skipped_events": [event["name"] for event in skipped_events],
        }
    )

    events_to_resolve = [event for event in progressed_events if event["remaining"] <= 0]
    for event in events_to_resolve:
        resolve_event(group_id, event)

    group["round"] += 1
    draw_to_three(group)

    if group_is_finished(group):
        group["finished"] = True

    save_all_state()
    refresh_group(group_id)


# ============================================================
# UI COMPONENTS
# ============================================================
def render_agent_card(group_id: str, group: dict[str, Any], agent: dict[str, Any]) -> None:
    css = "card agent-card"
    if agent["status"] == "assigned":
        css += " in-progress"

    with ui.card().classes(css):
        ui.image(image_url(STATIC_ROUTES["agents"], agent["image"])).style(
            "width:245px; height:340px; object-fit:contain; border-radius:12px; background:#020617;"
        )
        if agent["status"] == "assigned":
            assigned_event = get_event(group, agent.get("mission")) if agent.get("mission") else None
            if assigned_event and event_is_in_progress(assigned_event):
                ui.label("Locked until card resolves").classes("text-sm small-muted")
            else:
                ui.button("Unassign", on_click=lambda aid=agent["id"]: unassign_agent(group_id, aid)).props("color=orange")


def render_event_card(group_id: str, group: dict[str, Any], event: dict[str, Any]) -> None:
    assigned_agents = assigned_agents_for_event(group, event)
    assigned_names = [agent["name"] for agent in assigned_agents]

    css = "card event-card"
    if event_is_in_progress(event):
        css += " in-progress"

    with ui.card().classes(css):
        # The card art contains the public event information. Hidden solution data stays in code only.
        ui.image(image_url(STATIC_ROUTES[group["side"]], event["image"])).style(
            "width:445px; height:620px; object-fit:contain; border-radius:12px; background:#020617;"
        )

        with ui.column().classes("assignment-panel w-full gap-2"):
            ui.label("Assigned: " + (", ".join(assigned_names) if assigned_names else "None")).classes("text-sm")

            if event_is_in_progress(event):
                ui.label("In progress - assigned agents are locked").classes("text-sm small-muted")
            elif not event_has_open_assignment_slot(event):
                ui.label("Maximum agents assigned.").classes("text-sm small-muted")
            elif not available_agents(group):
                ui.label("No available agents.").classes("text-sm small-muted")
            else:
                ui.label("Assign available agent:").classes("text-sm font-bold")
                with ui.row().classes("gap-2 flex-wrap"):
                    for agent in available_agents(group):
                        ui.button(
                            agent["name"],
                            on_click=lambda aid=agent["id"], eid=event["id"]: dispatch(group_id, aid, eid),
                        ).props("dense")


def render_group_status(group: dict[str, Any]) -> None:
    active = len(group["active_events"])
    deck = len(group["deck"])
    available = len(available_agents(group))
    total_agents = len(group["agents"])

    with ui.row().classes("gap-4 flex-wrap"):
        with ui.card().classes("card"):
            ui.label(f"Score: {group['score']}").classes("text-2xl font-bold")
        with ui.card().classes("card"):
            ui.label(f"Deck remaining: {deck}").classes("text-2xl font-bold")
        with ui.card().classes("card"):
            ui.label(f"Active cards: {active}/{ACTIVE_EVENTS_PER_TURN}").classes("text-2xl font-bold")
        with ui.card().classes("card"):
            ui.label(f"Available agents: {available}/{total_agents}").classes("text-2xl font-bold")


def render_recent_history(group_id: str) -> None:
    recent = [entry for entry in DECISION_HISTORY if entry.get("group") == group_id][-8:]
    ui.label("Recent Decisions").classes("text-2xl font-bold")
    if not recent:
        ui.label("No decisions logged yet.")
        return

    for entry in reversed(recent):
        action = entry.get("action", "unknown")
        with ui.card().classes("card"):
            ui.label(f"Round {entry.get('round', '-')}: {action.replace('_', ' ').title()}").classes("font-bold")
            if action == "assign_agent":
                ui.label(f"{entry['agent']} assigned to {entry['event']}")
            elif action == "unassign_agent":
                ui.label(f"{entry['agent']} unassigned from {entry['event']}")
            elif action == "resolve_event":
                ui.label(f"{entry['event']} -> {'SUCCESS' if entry['success'] else 'FAILED'}")
            elif action == "end_turn":
                ui.label("Progressed: " + (", ".join(entry.get("progressed_events", [])) or "None"))
                ui.label("Skipped: " + (", ".join(entry.get("skipped_events", [])) or "None"))
            elif action == "draw_event":
                ui.label(f"Drew event: {entry['event']}")
            elif action == "reset_group":
                ui.label("Group reset")
            ui.label(entry.get("time", "")).classes("text-xs small-muted")


def group_screen(group_id: str) -> None:
    add_style()
    main = ui.column().classes("w-full p-4")

    def refresh() -> None:
        group = GROUPS.get(group_id)
        main.clear()

        with main:
            if not group:
                ui.label(f"Unknown group: {group_id}").classes("text-3xl font-bold")
                ui.link("Home", "/").classes("text-lg")
                return

            with ui.row().classes("w-full justify-between items-center"):
                ui.label(f"{group['side']} GROUP {group_id.split('-')[-1]} - ROUND {group['round']}").classes("text-4xl font-bold")
                with ui.row().classes("gap-2"):
                    ui.button("END TURN", on_click=lambda: advance_round(group_id)).props("color=red")
                    ui.button("RESET THIS GROUP", on_click=lambda: reset_group(group_id)).props("color=grey")
                    ui.button("SAVE GAME", on_click=save_history_with_notice).props("color=green")
                    ui.link("RESULTS", "/results").classes("text-lg")
                    ui.link("HOME", "/").classes("text-lg")

            ui.separator()
            render_group_status(group)

            if group_is_finished(group):
                with ui.card().classes("finished-banner"):
                    ui.label("All event cards are over for this group.").classes("text-2xl font-bold")
                    ui.label("Go to Results for the final overview.")

            if not group["active_events"] and group["deck"]:
                with ui.card().classes("warning-banner"):
                    ui.label("No active cards, but the deck still has cards. Click End Turn to draw.").classes("font-bold")

            ui.separator()
            ui.label("ACTIVE EVENT CARDS").classes("text-2xl font-bold")
            ui.label("Each group keeps up to three active event cards. New cards are drawn after resolved cards leave play.").classes("small-muted")

            if not group["active_events"]:
                ui.label("No active event cards.").classes("text-xl")
            else:
                with ui.row().classes("gap-4 flex-wrap"):
                    for event in group["active_events"]:
                        render_event_card(group_id, group, event)

            ui.separator()
            ui.label("AGENTS").classes("text-2xl font-bold")
            with ui.row().classes("gap-4 flex-wrap"):
                for agent in group["agents"]:
                    render_agent_card(group_id, group, agent)

            ui.separator()
            render_recent_history(group_id)

    PAGES[group_id] = refresh
    refresh()


# ============================================================
# PAGES
# ============================================================
@ui.page("/")
def home() -> None:
    add_style()
    ui.label("Intellectual Warfare - Online Saved Game").classes("text-4xl font-bold")
    ui.label("Open each group page in a different browser window or device.").classes("text-xl")
    ui.label("This version saves the live game in SQLite, so a hosted game can resume after refreshes or server restarts.").classes("small-muted")
    ui.label(f"Saved game database: {STATE_DB_FILE}").classes("small-muted")
    ui.label(f"Player-safe public history export: {HISTORY_FILE}").classes("small-muted")
    ui.separator()

    missing_folders = []
    if not AGENT_IMAGE_FOLDER.exists():
        missing_folders.append(f"Agent images: {AGENT_IMAGE_FOLDER}")
    if not AZADIKHAH_CARD_FOLDER.exists():
        missing_folders.append(f"Azadikhah event cards: {AZADIKHAH_CARD_FOLDER}")
    if not IRGC_CARD_FOLDER.exists():
        missing_folders.append(f"IRGC event cards: {IRGC_CARD_FOLDER}")

    if missing_folders:
        with ui.card().classes("warning-banner"):
            ui.label("Some image folders were not found. The game will run, but some images may not display.").classes("font-bold")
            for item in missing_folders:
                ui.label(item).classes("text-sm")

    with ui.row().classes("gap-8 flex-wrap"):
        with ui.column().classes("gap-2"):
            ui.label("IRGC Groups").classes("text-2xl font-bold")
            for group_id, group in GROUPS.items():
                if group["side"] == "IRGC":
                    number = group_id.split("-")[-1]
                    ui.link(f"IRGC Group {number}", f"/irgc/{number}").classes("text-xl")

        with ui.column().classes("gap-2"):
            ui.label("Azadikhah Groups").classes("text-2xl font-bold")
            for group_id, group in GROUPS.items():
                if group["side"] == "Azadikhah":
                    number = group_id.split("-")[-1]
                    ui.link(f"Azadikhah Group {number}", f"/azadikhah/{number}").classes("text-xl")

        with ui.column().classes("gap-2"):
            ui.label("Overview").classes("text-2xl font-bold")
            ui.link("Final Results", "/results").classes("text-xl")
            ui.button("Save Game", on_click=save_history_with_notice).props("color=green")
            ui.button("Reset Whole Game", on_click=reset_everything).props("color=red")


@ui.page("/irgc/{number}")
def irgc_group(number: int) -> None:
    group_screen(f"irgc-{number}")


@ui.page("/azadikhah/{number}")
def azadikhah_group(number: int) -> None:
    group_screen(f"azadikhah-{number}")


@ui.page("/results")
def results_page() -> None:
    add_style()
    ui.label("FINAL RESULTS").classes("text-4xl font-bold")
    with ui.row().classes("gap-2"):
        ui.link("Home", "/").classes("text-lg")
        ui.button("Save Game", on_click=save_history_with_notice).props("color=green")
        ui.button("Reset Whole Game", on_click=reset_everything).props("color=red")
    ui.separator()

    irgc_score = sum(group["score"] for group in GROUPS.values() if group["side"] == "IRGC")
    azadikhah_score = sum(group["score"] for group in GROUPS.values() if group["side"] == "Azadikhah")
    irgc_resolved = sum(1 for result in RESULTS if result["side"] == "IRGC")
    azadikhah_resolved = sum(1 for result in RESULTS if result["side"] == "Azadikhah")
    irgc_successes = sum(1 for result in RESULTS if result["side"] == "IRGC" and result["success"])
    azadikhah_successes = sum(1 for result in RESULTS if result["side"] == "Azadikhah" and result["success"])

    with ui.row().classes("gap-4 flex-wrap"):
        with ui.card().classes("card"):
            ui.label(f"IRGC total score: {irgc_score}").classes("text-2xl font-bold")
            ui.label(f"Resolved: {irgc_resolved} | Successes: {irgc_successes}").classes("small-muted")
        with ui.card().classes("card"):
            ui.label(f"Azadikhah total score: {azadikhah_score}").classes("text-2xl font-bold")
            ui.label(f"Resolved: {azadikhah_resolved} | Successes: {azadikhah_successes}").classes("small-muted")

    if irgc_score > azadikhah_score:
        ui.label("Winner: IRGC").classes("text-3xl font-bold")
    elif azadikhah_score > irgc_score:
        ui.label("Winner: Azadikhah").classes("text-3xl font-bold")
    else:
        ui.label("Result: Draw").classes("text-3xl font-bold")

    ui.separator()
    ui.label("Group Status").classes("text-2xl font-bold")
    with ui.row().classes("gap-4 flex-wrap"):
        for group_id, group in GROUPS.items():
            with ui.card().classes("card"):
                ui.label(f"{group['side']} Group {group_id.split('-')[-1]}").classes("text-xl font-bold")
                ui.label(f"Round: {group['round']}")
                ui.label(f"Score: {group['score']}")
                ui.label(f"Deck remaining: {len(group['deck'])}")
                ui.label(f"Active events: {len(group['active_events'])}")
                ui.label("Finished: " + ("Yes" if group_is_finished(group) else "No"))

    ui.separator()
    ui.label("Exact Event Resolution History").classes("text-2xl font-bold")
    ui.label("Solution traits are hidden from the player-facing results screen.").classes("small-muted")

    if not RESULTS:
        ui.label("No events have been resolved yet.")
    else:
        for result in RESULTS:
            css_class = "result-success" if result["success"] else "result-failure"
            with ui.card().classes(f"card {css_class}"):
                ui.label(f"Round {result['round']} - {result['group']} - {result['event']}").classes("text-xl font-bold")
                ui.label(f"Side: {result['side']}")
                ui.label(f"Success: {result['success']}")
                ui.label(f"Points: {result['points']}")
                ui.label("Assigned agents: " + (", ".join(result["assigned_agents"]) if result["assigned_agents"] else "None"))

    ui.separator()
    ui.label("Full Decision Log").classes("text-2xl font-bold")
    if not DECISION_HISTORY:
        ui.label("No decisions logged yet.")
    else:
        for entry in DECISION_HISTORY[-100:]:
            with ui.card().classes("card"):
                ui.label(f"{entry.get('time', '')} | Round {entry.get('round', '-')} | {entry.get('group', '-')} | {entry.get('action', '').replace('_', ' ').title()}").classes("font-bold")
                if entry.get("agent") and entry.get("event"):
                    ui.label(f"{entry['agent']} -> {entry['event']}")
                elif entry.get("event"):
                    ui.label(str(entry["event"]))
                if entry.get("progressed_events") is not None:
                    ui.label("Progressed: " + (", ".join(entry.get("progressed_events", [])) or "None"))
                    ui.label("Skipped: " + (", ".join(entry.get("skipped_events", [])) or "None"))
                if entry.get("success") is not None:
                    ui.label("Result: " + ("SUCCESS" if entry["success"] else "FAILED"))


start_or_load_game()

ui.run(
    title="Intellectual Warfare - Online Saved Game",
    host=APP_HOST,
    port=APP_PORT,
    reload=False,
)
'''
