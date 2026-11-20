# Run brief: the corrected holding rule and the `standardise` pilot, 2026-11-20

Written before any result is read. The queue (`<scratchpad>/night/queue.sh`) started at 11:07 Paris, after the
operator's go. Everything below was fixed before the first book finished.

## What we try to prove
**The vision (operator):** if an idea pays on daily bars, the same kind of idea can pay on hourly bars. What the night
showed so far:
1. Holding each bet for its horizon is necessary on hourly bars. Without it, no hourly book was above 0.
2. It is not sufficient. 0 hourly books pass step 6, because:
   - most hourly ideas predict a move smaller than a round trip (about 20 bps);
   - the long-horizon books that clear costs fail on Calmar or on beating the coin;
   - two of them were positive only through the old rule's defect.

This run asks two questions, and checks a third.
- **A. Pilot (topic 36): is the hourly forecast mis-scaled?** On hourly bars `standardise` compares the forecast with
  its last 2.5 to 21 days; on daily bars, with its last months to a year. Scaled on the same span as daily (60 days),
  does an hourly book become steadier, cheaper and better? If yes, the next lever is a fix that holds for every
  timeframe.
- **B. The corrected rule on paying books: is holding neutral where a book already pays, now on two-sided books
  too?** Set 3 said yes for the 9 one-sided books. The 2 two-sided ones were held against the forecast by the defect.
- **C. Check: does the corrected rule behave on real books as on its 11 cases?** A replay of the engine against its
  module on each new record, plus 0 % of the time in a position held against the forecast.

## The books
| Part | Books | Compared with |
|---|---|---|
| A. Pilot (`std_time_pilot_run`), `standardise` window 1,440 bars (60 days), minimum history 480 (20 days), corrected rule | grinding-rises (72), volatile evening-fall d2 (24), deep-decline (72), fresh-drop-rebound (72): the long-horizon, one-sided hourly books | the same books held under the old rule (night records). On these books the rule change alone moves positions by 3 to 24 % of bars but earnings before costs by at most about 5 % (replay; deep-decline 5.1 %), so a larger change is the window's effect |
| B. `hold2_rerun`, list 2 | volatile reversal completes quickly (1d, 3), rsi side predicts next week (1d, 7), and set 3's last 2: nearness to highs more coins (1h, 168), heavy-volume follow-through (1d, 3) | their records without hold, and the 2 two-sided under the old rule |
| B. `hold2_rerun`, list 3 | the paying books the corrected rule moves by 5 % or more: golden-cross momentum more coins (1h, 240), dual momentum (1h, 72), above-average drift (1d, 20), rsi above streak (1d, 14), nearness more coins (1d, 7), nearness without the short side (1d, 7) | their records without hold, and under the old rule |

Not rerun, by one rule: a book that does not pay is rerun only if, under the corrected rule (replayed), it earns more
per unit traded before costs than a round trip costs. That excludes the 5 two-sided hourly reversals (they lose even
before costs) and 3 non-paying books the rule barely moves.

## What we measure
Per book, against its reference:
1. **Did the change do what we think? (the mechanism)**
   - Pilot: the share of bars where the forecast changes; mean |forecast|; share at the cap (±20); share at 0; bets per
     day (the engine's rule); units traded; bars without a forecast at window starts (the warm-up). The warm-up
     loaded before each window is 2 × the required bars, so none are expected.
   - Corrected rule: the replay check (the engine against `core/holding_period.py`); the time held against the forecast.
2. **Economics:** earned per unit before costs; cost per unit; Sharpe; Sharpe minus holding's; mean daily return; Calmar;
   step 6, and which check decides.
3. **Why (the book's diagnosis, `common/book_diagnosis.md`):**
   - big enough (the move over the horizon against a round trip);
   - opening time and closing time;
   - holding past the bets;
   - trend (the market's share of the gain).

   A pass carried by the market (grinding-rises: 73 %) is not the idea paying.
4. **Robustness:** the lowest Sharpe with one window left out; per coin (how many coins earn); for a book that passes,
   the unseen-dates test (run on its own by the script).

## Expected outcomes
**A. Pilot**
| Outcome | What the counts would show | Meaning, and what follows |
|---|---|---|
| A1. The lever works | The forecast changes on fewer bars and fewer units are traded. Earned per unit rises and Sharpe rises on 3 or 4 of 4. At least 1 book passes step 6 with a market share under half (most likely the volatile evening-fall d2, which today fails only on Calmar: 0.64 against 0.75) | The hourly forecast was mis-scaled. Step 3's guide states the window in time for every timeframe (topic 36). Rerun the confirmed long-horizon hourly ideas with it. The passer goes to its unseen dates |
| A2. The mechanism works, no economic gain | Fewer changes and units, but Sharpe and Calmar within ±0.1 | The window is not the lever. Keep it in time all the same (one rule for every timeframe). The lever is the ideas' edge (topic 34: a move that pays for its trip; topic 35: a horizon in price) |
| A3. Worse | Sharpe falls on 3 or 4. For example, a forecast scaled on 60 days is larger in volatile stretches and loses more there | Read why in the diagnosis before any change. The 60-day rule taken from daily bars may not suit every component |
| A4. No mechanism | The forecast changes as often as before | The jitter comes from the components' own inputs (hourly lookbacks, regime windows), not from `standardise`. Next: the other bar-counted settings of topic 36 |

**B. The corrected rule on paying books**
| Outcome | What the counts would show | Meaning, and what follows |
|---|---|---|
| B1. Neutral, two-sided included | All 12 rerun books stay profitable. Sharpe within ±0.15 of their record without hold. The replay matches the engine. 0 % held against the forecast. The volatile reversal (1d) pays again | The hold is neutral where a book already holds its bets for days. It can be every plan's default (step 3 already sets it). Ready for the operator's go to merge into master, with the proof done (absent key: identical files) |
| B2. Neutral on one-sided books, not on two-sided | The two-sided daily books stay below their record | The hold costs a two-sided book its quick reversals. Read the closing time: the 3-day reversal may close too late |
| B3. A paying one-sided book stops paying | — | The corrected rule's noise threshold or side switch hurts something the cases did not cover. Back to the cases |

**C. Check:** any mismatch between the engine and the module beyond fill rounding, or any time held against the
forecast, is a defect. It is read first, and the runs are not read until it is fixed.

## Already known (to not mistake for a result)
- The night's two "positive" two-sided hourly books (Sharpe 0.32 and 0.45) came from the defect. Under the corrected
  rule they lose before costs (replay). They are not rerun.
- The pilot's references are old-rule records. The rule change alone moves these 4 books' earnings before costs by
  at most about 5 % (replay), so the comparison holds within that.
- In-sample: these books and folds were already looked at. One pass in 4 is not a proof until its unseen dates hold.
