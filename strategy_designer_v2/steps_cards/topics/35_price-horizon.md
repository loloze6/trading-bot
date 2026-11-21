# Topic 35: a horizon in price, not only in time

Status: open  
Where: research: shared definitions (`common/idea_definition.md`, `common/forecast.md` 7), steps 2, 3; the engine
(shared code) if it is built  
Opened: 2026-11-20, the operator, during the review of topic 34

## Question
Should an idea be able to say when its move ends by a price (the move reached, or given back), and not only by a number
of bars?

## Seen
- Today an idea's horizon is a time: "the coin moves over H bars". The holding period (`min_holding_bars`) holds each
  bet for H bars (`forecast.md` 7, option 2).
- The night's diagnosis readings (topic 34) show moves that end at different times:
  - evening-bounce (2 bars) peaks at bar +2 and gives back by +5;
  - volatile evening-fall (24 bars) is still rising at bar +27;
  - grinding-rises (72 bars) peaks near bar 78.
- On real positions, part of the time is spent past the bets: 30 % on grinding-rises, where it loses (−0.6 bps a bar).
- A time horizon closes on the clock, whether the move is done or not.

## Why it matters
If an idea's move has a typical size but not a typical duration, a time horizon closes either too early (part of the
move missed) or too late (the move given back, or the coin's risk taken for nothing). A price horizon would close
when the move is done.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Keep the horizon in time only | nothing to build | closing stays on the clock |
| B. A horizon in price: the idea states its move (e.g. "+2 %"), and the bet ends when it is reached or given back (a stop) | closing follows the move | new definitions (forecast, bet, holding); engine change (shared code, the operator's go); a target and a stop are tuned values, which adds choices to test |
| C. Both: the bet ends at the price or at the time, whichever comes first | keeps the time limit while closing on the move | the same as B, with two settings per idea |

Recommended: decide after topic 34's step 3. On the night's books, reading 3 (closing time) shows whether moves have a
typical size more than a typical duration: peaks at very different bars but of a similar size would argue for B or C.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
Waits for topic 34's step 3 (the diagnosis on the night's books, set 3 as the control), then the operator's decision.

## Links
Topic 34, `topics/34_review/book_diagnosis.md` (reading 3, closing time; reading 4, holding past the bets), `common/forecast.md` 7,
`runs/HOLDING_NIGHT_RUN.md`.
