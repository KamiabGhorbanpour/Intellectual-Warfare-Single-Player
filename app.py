from __future__ import annotations

from functools import partial
from typing import Any

from nicegui import app, ui

from game_content import (
    APP_HOST,
    APP_PORT,
    AZADIKHAH_AGENTS,
    AZADIKHAH_EVENTS,
    IRGC_AGENTS,
    IRGC_EVENTS,
    RNG,
    STANDARD_RUN_LENGTH,
    STATIC_ROUTES,
    STORAGE_SECRET,
    image_url,
    pretty_trait,
    static_folders,
)
from game_engine import evaluate_attempt, run_rank, shuffled_run


for static_route, static_folder in static_folders():
    if static_folder.exists():
        app.add_static_files(static_route, str(static_folder))
    else:
        print(f"WARNING: image folder not found: {static_folder}")


STYLE_HTML = """
<style>
:root {
    --ink: #15283b;
    --muted: #617386;
    --line: #dbe4ec;
    --paper: #f6f8fb;
    --blue: #155eef;
    --blue-dark: #0d3faa;
    --red: #c9342f;
    --green: #16865a;
}
body {
    margin: 0;
    color: var(--ink);
    background:
        radial-gradient(circle at 12% 8%, rgba(21, 94, 239, .10), transparent 28rem),
        linear-gradient(180deg, #ffffff 0%, var(--paper) 100%);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.game-shell { max-width: 1480px; margin: 0 auto; padding: 28px; }
.eyebrow { color: var(--blue); font-size: .78rem; font-weight: 850; letter-spacing: .18em; text-transform: uppercase; }
.display-title { font-size: clamp(2.4rem, 6vw, 5.8rem); font-weight: 950; line-height: .88; letter-spacing: -.065em; }
.section-title { font-size: clamp(1.55rem, 3vw, 2.5rem); font-weight: 900; letter-spacing: -.035em; }
.muted { color: var(--muted); }
.paper-card {
    border: 1px solid var(--line);
    border-radius: 20px;
    background: rgba(255, 255, 255, .94);
    box-shadow: 0 18px 50px rgba(27, 50, 73, .08);
}
.faction-card { min-width: min(100%, 360px); flex: 1 1 360px; padding: 24px; }
.faction-card.irgc { border-top: 5px solid var(--red); }
.faction-card.azadikhah { border-top: 5px solid var(--blue); }
.stat-card { min-width: 150px; padding: 14px 18px; }
.stat-value { font-size: 1.75rem; font-weight: 950; letter-spacing: -.04em; }
.event-panel { flex: 1 1 520px; min-width: min(100%, 340px); padding: 18px; }
.event-art { width: 100%; max-height: 690px; object-fit: contain; border-radius: 14px; background: #edf2f7; }
.roster-panel { flex: 1.35 1 680px; min-width: min(100%, 340px); }
.agent-tile {
    width: 218px;
    max-width: 46vw;
    padding: 10px;
    cursor: pointer;
    border: 2px solid transparent;
    transition: transform .14s ease, border-color .14s ease, box-shadow .14s ease;
}
.agent-tile:hover { transform: translateY(-3px); box-shadow: 0 14px 36px rgba(27, 50, 73, .13); }
.agent-tile.selected { border-color: var(--blue); box-shadow: 0 0 0 4px rgba(21, 94, 239, .13); }
.agent-art { width: 100%; aspect-ratio: 591 / 1004; object-fit: contain; border-radius: 12px; background: #edf2f7; }
.requirement-pill {
    display: inline-flex; align-items: center; gap: 8px; padding: 8px 13px;
    border-radius: 999px; background: #e9f0ff; color: var(--blue-dark); font-weight: 850;
}
.hint-panel {
    border-radius: 14px;
    background: #eef5ff;
    padding: 14px 16px;
    color: var(--ink);
}
.feedback-success { border-left: 6px solid var(--green); }
.feedback-failure { border-left: 6px solid var(--red); }
.review-success { border-left: 4px solid var(--green); }
.review-failure { border-left: 4px solid var(--red); }
.primary-button { font-weight: 850; letter-spacing: .02em; }
@media (max-width: 700px) {
    .game-shell { padding: 16px; }
    .agent-tile { width: calc(50% - 8px); max-width: none; }
}
</style>
"""


def agents_for(side: str) -> list[dict[str, Any]]:
    return IRGC_AGENTS if side == "IRGC" else AZADIKHAH_AGENTS


def events_for(side: str) -> list[dict[str, Any]]:
    return IRGC_EVENTS if side == "IRGC" else AZADIKHAH_EVENTS


def agent_image_url(side: str, filename: str) -> str:
    return image_url(STATIC_ROUTES[f"{side}_agents"], filename)


def event_image_url(side: str, filename: str) -> str:
    return image_url(STATIC_ROUTES[f"{side}_events"], filename)


TRAIT_HINTS = {
    "binary_thinking": (
        "The institution demands a simple loyal-versus-hostile classification of the gathering. "
        "This card rewards the habit of forcing complex motives into two camps."
    ),
    "thoroughness": "Slow down and check the details rather than acting on the first plausible story.",
    "curiosity": "Look for someone inclined to investigate further instead of stopping at the obvious explanation.",
    "epistemic_justice": "Consider who is being believed, dismissed, or treated unfairly as a source of knowledge.",
    "legitimacy_awareness": "Think about how an action will affect whether people regard the institution as justified or trustworthy.",
    "arrogance": "A rigid sense of certainty or superiority may fit what this institution is asking for.",
    "epistemic_cowardice": "The useful disposition here avoids challenging a dominant view even when doubts are available.",
    "intellectual_humility": "The situation benefits from someone willing to admit uncertainty or revise an initial judgment.",
    "confirmation_bias": "The institution may reward someone who interprets new information in a way that protects an existing belief.",
    "open_mindedness": "Look for someone willing to seriously consider alternatives rather than locking onto one interpretation.",
    "close_mindedness": "The task may reward resistance to competing perspectives or inconvenient evidence.",
    "obstinacy": "Persistence in a fixed position, even under pressure to reconsider, is useful here.",
    "epistemic_authoritarianism": "The task favors deference to an imposed source of authority over independent evaluation.",
    "intellectual_courage": "The situation calls for someone willing to pursue or voice a difficult conclusion despite social or political risk.",
    "intellectual_integrity": "Look for consistency between what someone claims to value and how they actually reason or act.",
    "intellectual_empathy": "Try to understand the situation from the perspective of people whose experience differs from your own.",
    "legitimacy_preservation": "The institution is primarily concerned with protecting its standing and authority.",
}


def hint_for_event(event: dict[str, Any]) -> str:
    hints = [TRAIT_HINTS[value] for value in event["traits"] if value in TRAIT_HINTS]
    return " ".join(hints)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@ui.page("/")
def arcade_page() -> None:
    ui.add_head_html(STYLE_HTML)

    state: dict[str, Any] = {
        "phase": "home",
        "side": None,
        "deck": [],
        "index": 0,
        "selected": set(),
        "score": 0,
        "streak": 0,
        "best_streak": 0,
        "feedback": None,
        "results": [],
    }
    root = ui.column().classes("game-shell w-full gap-5")

    def best_scores() -> dict[str, int]:
        stored = app.storage.user.get("arcade_best_scores", {})
        return {
            "IRGC": int(stored.get("IRGC", 0)),
            "Azadikhah": int(stored.get("Azadikhah", 0)),
        }

    def start_run(side: str) -> None:
        deck = events_for(side)
        run_length = min(STANDARD_RUN_LENGTH, len(deck))
        state.update(
            {
                "phase": "play",
                "side": side,
                "deck": shuffled_run(deck, run_length, rng=RNG),
                "index": 0,
                "selected": set(),
                "score": 0,
                "streak": 0,
                "best_streak": 0,
                "feedback": None,
                "results": [],
            }
        )
        render()

    def leave_run() -> None:
        state["phase"] = "home"
        render()

    def current_event() -> dict[str, Any]:
        return state["deck"][state["index"]]

    def toggle_agent(agent_id: str) -> None:
        if state["feedback"] is not None:
            return
        selected: set[str] = state["selected"]
        if agent_id in selected:
            selected.remove(agent_id)
        else:
            requirement = int(current_event()["requirement"])
            if len(selected) >= requirement:
                ui.notify(
                    f"This card accepts exactly {requirement} agent(s). Deselect one first.",
                    type="warning",
                )
                return
            selected.add(agent_id)
        render()

    def submit_attempt() -> None:
        event = current_event()
        roster = agents_for(state["side"])
        selected_agents = [agent for agent in roster if agent["id"] in state["selected"]]
        try:
            result = evaluate_attempt(event, selected_agents)
        except ValueError as error:
            ui.notify(str(error), type="warning")
            return

        if result["success"]:
            state["score"] += result["points"]
            state["streak"] += 1
            state["best_streak"] = max(state["best_streak"], state["streak"])
        else:
            state["streak"] = 0

        result["card_number"] = state["index"] + 1
        state["results"].append(result)
        state["feedback"] = result
        render()

    def continue_run() -> None:
        if state["index"] + 1 >= len(state["deck"]):
            state["phase"] = "results"
            scores = best_scores()
            scores[state["side"]] = max(scores[state["side"]], state["score"])
            app.storage.user["arcade_best_scores"] = scores
        else:
            state["index"] += 1
            state["selected"] = set()
            state["feedback"] = None
        render()

    def render_header(kicker: str) -> None:
        with ui.row().classes("w-full items-end justify-between gap-4 flex-wrap"):
            with ui.column().classes("gap-1"):
                ui.label(kicker).classes("eyebrow")
                ui.label("INTELLECTUAL WARFARE").classes("section-title")
            if state["phase"] != "home":
                ui.button("EXIT RUN", on_click=leave_run).props("flat color=grey-8")

    def render_home() -> None:
        render_header("Single-player game")
        with ui.column().classes("gap-4 py-8"):
            ui.label("HOW TO PLAY").classes("display-title")

        with ui.card().classes("paper-card w-full p-5"):
            ui.label("Instructions").classes("text-xl font-black")
            with ui.row().classes("w-full gap-6 flex-wrap"):
                for number, title, body in [
                    (
                        "01",
                        "Choose a faction",
                        "Select Azadikhah or the IRGC. Each faction has a different roster.",
                    ),
                    (
                        "02",
                        "Review the event",
                        "Read the event and compare its problem with the traits of the available agents.",
                    ),
                    (
                        "03",
                        "Assign agents",
                        "Select exactly the number of agents required by the event.",
                    ),
                    (
                        "04",
                        "Submit the assignment",
                        "The submission is final. You receive one point when every selected agent "
                        "has at least one relevant trait. The relevant traits are shown after scoring.",
                    ),
                ]:
                    with ui.column().classes("gap-1 flex-1 min-w-64"):
                        ui.label(number).classes("eyebrow")
                        ui.label(title).classes("text-lg font-black")
                        ui.label(body).classes("muted")

        ui.label("Choose your faction").classes("section-title pt-4")
        with ui.row().classes("w-full gap-5 flex-wrap"):
            with ui.card().classes("paper-card faction-card azadikhah gap-4"):
                ui.label("AZADIKHAH").classes("eyebrow")
                ui.label("Opposition Coalition").classes("text-3xl font-black")
                ui.label(
                    "Play with the six-agent roster of the fictional Iranian opposition coalition."
                ).classes("muted")
                ui.button(
                    "PLAY AS AZADIKHAH",
                    on_click=lambda: start_run("Azadikhah"),
                ).props("unelevated color=primary size=lg").classes("primary-button")

            with ui.card().classes("paper-card faction-card irgc gap-4"):
                ui.label("IRGC").classes("eyebrow")
                ui.label("Islamic Revolutionary Guard Corps").classes("text-3xl font-black")
                ui.label(
                    "Play with the seven-agent roster of the Islamic Revolutionary Guard Corps."
                ).classes("muted")
                ui.button(
                    "PLAY AS IRGC",
                    on_click=lambda: start_run("IRGC"),
                ).props("unelevated color=red-8 size=lg").classes("primary-button")

    def render_status() -> None:
        total = len(state["deck"])
        progress = (state["index"] + 1) / total
        with ui.row().classes("w-full gap-3 flex-wrap"):
            for label, value in [
                ("CARD", f"{state['index'] + 1} / {total}"),
                ("SCORE", f"{state['score']} / {total}"),
                ("STREAK", str(state["streak"])),
            ]:
                with ui.card().classes("paper-card stat-card gap-0"):
                    ui.label(label).classes("eyebrow")
                    ui.label(value).classes("stat-value")
        ui.linear_progress(value=progress, show_value=False).props("rounded color=primary")

    def render_play() -> None:
        side = state["side"]
        event = current_event()
        feedback = state["feedback"]

        render_header(f"{side} solo run")
        render_status()

        with ui.row().classes("w-full gap-5 items-start flex-wrap"):
            with ui.card().classes("paper-card event-panel gap-4"):
                ui.image(event_image_url(side, event["image"])).classes("event-art")
                hint_text = hint_for_event(event)
                if hint_text:
                    with ui.expansion("HINT", icon="lightbulb_outline").classes("w-full"):
                        ui.label(hint_text).classes("hint-panel leading-relaxed")

            with ui.column().classes("roster-panel gap-4"):
                ui.label("SELECT YOUR AGENTS").classes("section-title")
                with ui.row().classes("w-full gap-3 flex-wrap"):
                    for agent in agents_for(side):
                        selected = agent["id"] in state["selected"]
                        css = "paper-card agent-tile selected" if selected else "paper-card agent-tile"
                        with ui.card().classes(css).on("click", partial(toggle_agent, agent["id"])):
                            ui.image(agent_image_url(side, agent["image"])).classes("agent-art")
                            ui.label(agent["name"]).classes("font-black")
                            ui.label("SELECTED" if selected else "Click to select").classes(
                                "text-xs text-primary font-bold" if selected else "text-xs muted"
                            )

                if feedback is None:
                    selected_count = len(state["selected"])
                    requirement = int(event["requirement"])
                    ui.label(f"Selected: {selected_count} / {requirement}").classes("font-bold")
                    submit = ui.button(
                        "COMMIT",
                        on_click=submit_attempt,
                    ).props("unelevated color=primary size=lg").classes("primary-button")
                    if selected_count != requirement:
                        submit.disable()
                else:
                    render_feedback(feedback)

    def render_feedback(result: dict[str, Any]) -> None:
        success = result["success"]
        css = "paper-card feedback-success" if success else "paper-card feedback-failure"
        with ui.card().classes(f"{css} w-full p-5 gap-3"):
            ui.label("CORRECT — +1 POINT" if success else "INCORRECT — NO POINT").classes(
                "text-2xl font-black"
            )
            for agent_result in result["agents"]:
                matches = agent_result["matching_traits"]
                with ui.row().classes("items-center gap-2"):
                    ui.icon("check_circle" if matches else "cancel").classes(
                        "text-positive" if matches else "text-negative"
                    )
                    if matches:
                        ui.label(
                            f"{agent_result['name']}: "
                            + ", ".join(pretty_trait(value) for value in matches)
                        )
                    else:
                        ui.label(f"{agent_result['name']}: no matching trait")
            ui.label(
                "Relevant traits: "
                + ", ".join(pretty_trait(value) for value in result["required_traits"])
            ).classes("text-sm font-bold")
            ui.button(
                "VIEW FINAL SCORE" if state["index"] + 1 == len(state["deck"]) else "NEXT CARD",
                on_click=continue_run,
            ).props("unelevated color=primary size=lg").classes("primary-button")

    def render_results() -> None:
        total = len(state["deck"])
        score = state["score"]
        percent = round((score / total) * 100)
        scores = best_scores()

        render_header(f"{state['side']} run complete")
        with ui.card().classes("paper-card w-full p-7 gap-4"):
            ui.label("FINAL SCORE").classes("eyebrow")
            ui.label(f"{score} / {total}").classes("display-title")
            ui.label(f"{percent}% accuracy · {run_rank(score, total)}").classes("text-2xl font-black")
            ui.label(
                f"Best streak: {state['best_streak']} · Personal best for {state['side']}: "
                f"{scores[state['side']]} / {total}"
            ).classes("muted")
            with ui.row().classes("gap-3 flex-wrap"):
                ui.button(
                    "PLAY AGAIN",
                    on_click=lambda: start_run(state["side"]),
                ).props("unelevated color=primary size=lg").classes("primary-button")
                ui.button("CHOOSE ANOTHER FACTION", on_click=leave_run).props("outline color=primary size=lg")

        ui.label("Run review").classes("section-title pt-3")
        with ui.column().classes("w-full gap-3"):
            for result in state["results"]:
                css = "paper-card review-success" if result["success"] else "paper-card review-failure"
                with ui.card().classes(f"{css} w-full p-4 gap-1"):
                    with ui.row().classes("w-full justify-between items-center gap-3"):
                        ui.label(f"{result['card_number']:02d} · {result['event']}").classes("font-black")
                        ui.label("+1" if result["success"] else "+0").classes(
                            "text-positive font-black" if result["success"] else "text-negative font-black"
                        )
                    ui.label(
                        "Selected: " + ", ".join(agent["name"] for agent in result["agents"])
                    ).classes("text-sm muted")

    def render() -> None:
        root.clear()
        with root:
            if state["phase"] == "home":
                render_home()
            elif state["phase"] == "play":
                render_play()
            else:
                render_results()

    render()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Intellectual Warfare — Solo Arcade",
        host=APP_HOST,
        port=APP_PORT,
        storage_secret=STORAGE_SECRET,
        reload=False,
    )
