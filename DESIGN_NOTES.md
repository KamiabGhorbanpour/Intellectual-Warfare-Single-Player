# Solo conversion notes

## Decisions in this first version

- One player chooses either the Azadikhah or IRGC roster.
- A standard run contains 10 randomly selected, non-repeating cards.
- The player must select exactly the printed requirement before submission.
- Selections can be revised until submission.
- The first submission is final for scoring: success is worth one point and failure is worth zero.
- A selection succeeds only when every assigned agent shares at least one trait with the event's hidden relevant traits. This is the resolution rule used by the supplied multiplayer source.
- Hidden traits and per-agent matches are revealed after the attempt.
- Scores, streaks, a final rank, a run review, and per-faction personal bests are displayed.
- Personal bests are browser-specific. There is no login, public leaderboard, or database in this version.

## Original content corrections

Two supplied IRGC cards could not be solved under the original resolution rule:

1. **Climate and Energy Crisis** required `Epistemic Humility`, but no IRGC agent possessed that trait. It now uses `Intellectual Humility`, allowing Agent Khani to match.
2. **Bazaari Class Protests** printed a requirement of three but its only hidden trait, `Epistemic Justice`, matched just one agent. The printed requirement is preserved, while the hidden solution now includes `Epistemic Justice`, `Intellectual Humility`, and `Open-mindedness`, producing three eligible agents.

The tests will flag future edits that make an event impossible.

## Supplied blank card

The Azadikhah asset folder contains `15.png`, but the supplied multiplayer source defines only 14 Azadikhah events. The image itself has a requirement and longevity but no event text. It is preserved in the assets folder but is not placed in the playable deck until its event text and hidden traits are defined.

## Natural next additions

- Difficulty modes or full-deck runs
- Time-based bonuses
- Global Railway/PostgreSQL leaderboard
- Accounts and saved run history
- Event editor or JSON-based content packs
- Sound, transitions, and an attract-screen arcade presentation
