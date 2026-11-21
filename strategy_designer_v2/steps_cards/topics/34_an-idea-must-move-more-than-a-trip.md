# Topic 34: why a real idea does not pay, and an idea that pays for its trip

Status: open (designing)  
Where: research: shared definitions (`common/`), the observe-and-advise stage (topic 08), steps 2 and 7  
Opened: 2026-11-20, a session, from the holding night (`runs/HOLDING_NIGHT_RUN.md`, sets 1 and 2); widened the same day
by the operator: "identified too late, closed too late, or...", and "do not bet on a trending market by holding".

## Question
When step 5 confirms an idea and step 6 finds its book does not pay, why? And how do we make the workflow look for
ideas whose move, from the moment the bot can act, pays for the trade that captures it?

## Seen
2026-11-20, every confirmed hourly idea, held for its own horizon (option 2). Read from the bar files only, without a
backtest. The coin's own drift is removed, so a rising market does not count as the idea's move.
Scripts: `<scratchpad>/night/trend_timing.py`, `path.py`, `closure.py`; to be standardized, see Next.

**1. Size: is the move bigger than a round trip?** A round trip is two units (in and out), about 20 bps.
| Horizon | Books | Earned per unit traded, before costs | Sharpe after costs, held |
|---|---|---|---|
| 1 to 4 bars | 14 | 0.8 to 7 bps | 0 above 0 |
| 24 to 72 bars | 8 | 20 to 60 bps | 7 above 0 (0.24 to 1.14), 2 beat holding the coin, 0 pass step 6 |

**2. Move left once the bot can act (first read as "identified too late?", see below).** This is the average move per bar in the idea's direction around the bar whose
close fires the signal (bar 0). The bot earns from bar +1 on.
| Idea (horizon) | Bar −1 | Bar 0 | Bars +1 to +2 | Peak after the signal |
|---|---|---|---|---|
| evening-bounce (2) | −13 | −11 | +12 | +12 at +2, +3 by +5 |
| settlement-move (2) | −49 | −45 | +4 | +5 |
| hourly reversal (1) | 0 | −52 | +3 | +4 |
| grinding-rises (72) | +7 | **+69** | 0 | +14 at +24 |
| volatile evening-fall (24) | −15 | −15 | +18 | +58 at +27, still rising |

All values are in bps. What is left once the bot can act is 4 to 13 bps on the short ideas, below a round trip (about
20 bps). The trigger bar's move does not show lateness on its own (corrected the same day, operator: "the wording
differs from the measurement"). On the reversal ideas (settlement-move, hourly reversal, the evening ideas), the trigger
bar moves against the bet: it is the fall that sets the idea off, not a move already spent. Only on a continuation
(grinding-rises, +69 bps on bar 0 in the bet's direction) did part of the move happen before the bot could act.
Whether a reversal's rebound started inside the trigger bar is not measured by these bars.

**3. Closing: closed too late?** Measured on the book's real positions: their length against the horizon, and the
earnings per bar within and after it.
| Idea (horizon) | Longer than the horizon | Time in position after the horizon | Earned per bar within / after |
|---|---|---|---|
| evening-bounce (2) | 11 % | 50 % | 6.8 / 1.0 bps |
| post-settlement decline (4) | 82 % | 75 % | 1.2 / 0.6 |
| volatile evening-fall (24) | 49 % | 54 % | 3.2 / 1.5 |
| grinding-rises (72) | 91 % (a median of 231 bars) | 70 % | 0.4 / 0.2 |
After the horizon, the time still earns slightly more than 0 on all 9 books read: no losses from a reversal. On 7 of the
9 it earns less per bar than before the horizon. It takes the coin's risk for little return, which dilutes Sharpe and
Calmar. Not separated yet: a stale position from one renewed by a new signal (option 2 lets a new rise extend the hold).

**4. Trend: a bet on a rising market?** The book against the same average exposure held all the time.
| Book | Share that is just being in the market |
|---|---|
| grinding-rises | 57 % |
| daily-move reversals g1, g2 | 46 %, 54 % |
| evening-fall d1, d2 | about 0 % |
Step 6 already checks this with "beats holding the coin": 6 of the 8 long-horizon books fail it.

## Why it matters
Without knowing why a confirmed idea does not pay, step 7 proposes its next ideas blind. Holding longer is no answer
(the operator: that bets on a trending market). Most hourly ideas found so far are real, but the part of their move
left once the bot can act is smaller than a round trip.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. A shared definition in `common/`: an idea is worth testing when the move it predicts, from the bar after its signal and net of the coin's drift, is well above a round trip (the venue's cost, read from the config). Steps 2 and 7 read it | one rule for every timeframe; it changes the ideas proposed, not the checks | the models may misjudge a move's size; it shows at steps 5 and 6, nothing guards it |
| B. The four readings above as one standard diagnosis of a confirmed idea's book (size, timing, closing, trend), defined in `common/`, made by one helper; observations of the observe-and-advise stage (topic 08), which step 7 reads | step 7 gets the lever from real numbers: a longer horizon, an earlier trigger, closing at the horizon, beating the drift; it holds for daily and hourly alike | four new measures to define well (drift, log or simple moves, renewed or stale positions) |
| C. A minimum horizon on hourly bars | simple | a limit written for one timeframe, against "one rule for every case"; it would refuse a short idea with a large move |

Recommended: B, then A. B first, because it measures what goes wrong, and A's rule then rests on B's numbers (the
"move after the signal" is B's size and timing reading). Both follow the operator's ruling of 2026-11-19 (topic 08): step 6 stays
a profitability check (pass or fail), and observations belong to the observe-and-advise stage after steps 5 and 6.
The trend reading (4) is close to topic 08's first observation (a book's return in rising and falling windows); they
are designed together.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-20 | Holding means holding for the horizon the idea states, never longer to rescue a book | the operator | holding longer bets on a trending market | "hold longer when net profit is missing" |
| 2026-11-20 | Take the night's readings as a draft approach: review it, standardize it, go further, and test it | the operator | the readings tell why a proven idea does not pay | – |
| 2026-11-20 | A forecast that stays on with no new rise counts as past its bets | the operator | option 2: each rise is the event that asks for a hold | each bar the condition holds is a new prediction |
| 2026-11-20 | Long term, the diagnosis is part of the analysts' work (step 7), around profitability; the helper in `common/` is temporary, for this test | the operator | the analysts read why a confirmed idea does not pay | a separate stage |

## Status and next
2026-11-20: step 1 drafted, `topics/34_review/book_diagnosis.md`, for the operator's review (three open points at its end).
2026-11-20, review 1 (operator): readings worded as what they measure; reading 1 named "big enough"; the idea's closing
time (does the move end at the horizon) added as its own reading, distinct from the book staying in after its bets.
Review 2 (operator): opening time and closing time as a pair; the per-bet move against a round trip joins "big
enough"; "book stays in" renamed "holding past the bets" (the book's real positions, not the coin after a signal).
Review 3 (operator): "big enough" compares the price move over the horizon with the cost rate of a round trip;
quantity does not enter (profit and cost both scale with it). The book-level per-unit version is dropped.
2026-11-20, step 2 built (operator's go): `topics/34_review/book_diagnosis.py`, next to its definition until the observe-and-advise
stage exists; 8 tests on records whose answers are known by construction (bets, a known fee, a known path, overlap,
holding past the bets, a book that is all market, the horizon read from the plan); all pass. Proof: a rerun on the same
record gives an identical `diagnosis.json`. The 3 open points are applied as proposed until decided. First real record
(grinding-rises held, H 72): move over the horizon 38.9 bps against a round trip of 21.4; signal bar +58.1; peak 44.6 at
bar 78; 30 % of the time in a position past its bets (earning −0.6 bps a bar against +0.4 covered); market 73 % of the
book's daily gain.
1. Review: define the four readings in `common/` (business definition first, then the formula), and settle the open
   points: drift removal, log or simple moves, the cost of a round trip read from the venue config, overlapping
   signals, and renewed or stale positions (trace each position to the signal that holds it).
2. One helper, with tests, writing the diagnosis of a backtest as a file next to it.
3. Test: rerun it on fixed inputs and compare the files. Then read it on the night's books (sets 1 and 2) and on the
   paying books of set 3 as the control: a diagnosis that does not tell a paying book from a non-paying one is not
   ready.
4. Then the operator decides how step 7 reads it (through the observe-and-advise stage), and option A.

## Links
`runs/HOLDING_NIGHT_RUN.md` (readings of sets 1 and 2), topic 30, `common/forecast.md` point 7 (the holding period),
`topics/30_review/hold_rerun.py`, topic 08 (the observe-and-advise stage; step 6 stays pass or fail).
