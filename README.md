# Intellectual Warfare — Solo Arcade

This version turns the original six-group workshop game into an online game for one player.

## The solo loop

1. Choose the Azadikhah or IRGC faction.
2. Play a shuffled run of 10 event cards.
3. For each card, select exactly the number of agents shown by its requirement.
4. Commit one scored attempt. A successful first attempt earns one point.
5. Review the relevant traits, continue, and finish with a score out of 10.

Selections can be changed freely before submission. Once submitted, the result is locked and the solution is revealed. The browser keeps a separate personal best for each faction.

## Run locally

Python 3.11 or newer is required.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open <http://localhost:8080>.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

## Deploy on Railway

1. Put this folder in a GitHub repository.
2. In Railway, create a project from that repository.
3. Add a service variable named `STORAGE_SECRET` with a long random value.
4. Deploy. Railway will use the included `Dockerfile` and check `/health` before switching traffic.
5. Generate a public Railway domain in the service networking settings.

The application already listens on Railway's injected `PORT` and on `0.0.0.0`.

No database is required for this version. Personal bests use NiceGUI's per-browser storage. A later global leaderboard or account system should use PostgreSQL.

## Modify the content

- `game_content.py` contains both factions' agents, event text, hidden solution traits, requirements, and the standard run length.
- `game_engine.py` contains the scoring and validation rules.
- `app.py` contains the interface and one-player flow.
- `assets/agents/` and `assets/events/` contain the supplied artwork.

Run the checks after changing cards or traits:

```bash
python -m unittest discover -s tests -v
```

The content tests verify that every event is solvable and every referenced image exists.
