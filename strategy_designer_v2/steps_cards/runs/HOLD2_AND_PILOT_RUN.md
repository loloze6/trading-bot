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

## Reading, A. the pilot (`std_time_pilot_run`, 4 of 4, done 13:00 Paris)

`standardise` window 1,440 bars (60 days), minimum history 480, the corrected holding rule; against the same books'
night records (window 60 to 500 bars, old rule).

| Book (bars held) | Forecast changes per bar: night → pilot | Forecast at 0 | Units: night → pilot | Earned per unit before costs (bps) | Sharpe night → pilot | Calmar night → pilot | Step 6, pilot |
|---|---|---|---|---|---|---|---|
| grinding-rises (72) | 9.9 % → 6.4 % | 84 % | 3,301 → 3,566 | 60.5 → 57.7 | 0.875 → 0.877 | 0.645 → 0.634 | fails Calmar |
| volatile evening-fall d2 (24) | 1.7 % → 1.7 % | 99 % | 2,604 → 2,793 | 53.2 → 53.7 | 1.14 → 1.175 | 0.64 → 0.694 | fails Calmar only |
| deep-decline (72) | 43.9 % → 45.0 % | 51 % | 2,982 → 3,054 | 33.0 → 31.9 | 0.24 → 0.251 | −0.01 → 0.008 | fails vs holding, mean return, Calmar |
| fresh-drop-rebound (72) | 30.7 % → 32.0 % | 67 % | 3,347 → 3,211 | 31.5 → 37.4 | 0.24 → 0.314 | −0.02 → 0.036 | fails vs holding, mean return, Calmar |

**Counts.** Sharpe changes +0.00 to +0.07 on 4 of 4; Calmar −0.01 to +0.06; 0 of 4 pass step 6. The corrected rule alone
moves these books by up to about 5 % (replay), so the changes are within what the rule itself explains.

**Outcome: A2 on grinding-rises, A4 on the other 3. The window is not the lever.**
- grinding-rises (A2): the forecast changes a third less often, and nothing else moves. A replay of the window from 3
  days to 1 year (topic 36, `36_review/book_sim.py`, exact on its forecast) gives Sharpe 0.88 to 0.95: flat.
- deep-decline and fresh-drop-rebound (A4): the forecast changes as often as before (31 to 45 % of bars). Their
  frequent changes come from the components themselves (price changes over 1 and 3 days, recomputed every hour), not
  from the scaling.
- volatile evening-fall (A4): its forecast is 0 on 99 % of bars, a one-moment signal held 24 bars, so the scaling
  window has almost nothing to act on. It stays the best hourly book: Sharpe 1.175, beats holding the coin by 0.62,
  about 0 % of its gain is the market's (night diagnosis). It fails only Calmar: 0.694 against 0.75.

**What follows.** The `standardise` window is not why hourly books do not pay; leave it as it is for now. Whether to
state it in time anyway (one rule for every timeframe) is for the operator: no result asks for it. The levers left are
the ideas' edge (topic 34: a move that pays for its trip; topic 35: a horizon in price), and, for volatile evening-fall,
what makes its deepest fall (its diagnosis by window), before anything is changed.

## Reading, B. the corrected rule on paying books (`hold2_rerun`, 10 books, done 15:56 Paris)

The last 9 ran in 3 parts side by side (topic 37, option D: `runs/hold2_parts/`). Sharpe and Calmar after costs; step 6:
"pro" profitable enough.

| Book (bars held) | Sides | Without hold | Old rule | Corrected rule | Unseen dates 2016-17 / 2026 (corrected) |
|---|---|---|---|---|---|
| nearness to highs more coins, 1h (168) | long | pro 1.05 / 1.01 | – | **pro 1.24 / 1.49** | not profitable / no verdict |
| golden-cross momentum more coins, 1h (240) | long | pro 1.12 / 1.05 | pro 1.04 / 0.78 | pro 1.06 / 0.80 | profitable / no verdict |
| dual momentum, 1h (72) | long | pro 0.98 / 1.03 | pro 1.07 / 1.10 | pro 1.05 / 1.19 | not run (step 5 inconclusive) |
| nearness to highs more coins, 1d (7) | long | pro 1.25 / 1.67 | pro 1.20 / 1.49 | pro 1.22 / 1.53 | profitable / not profitable |
| nearness without the short side, 1d (7) | long | pro 1.01 / 0.96 | pro 1.05 / 1.08 | pro 1.05 / 1.04 | not run (inconclusive) |
| rsi above streak, 1d (14) | long | pro 1.04 / 0.92 | pro 1.00 / 0.84 | pro 0.98 / 0.79 | not run (inconclusive) |
| above-average drift, 1d (20) | long | pro 0.95 / 0.92 | pro 0.91 / 0.79 | pro 0.93 / 0.86 | not run (not observable) |
| heavy-volume follow-through, 1d (3) | long | pro 0.91 / 0.80 | – | pro 0.99 / 0.81 | not profitable / not profitable |
| rsi side predicts next week, 1d (7) | both | pro 1.03 / 1.14 | pro 0.99 / 0.90 | pro 0.97 / 0.87 | not profitable / profitable |
| volatile reversal completes quickly, 1d (3) | both | pro 1.16 / 1.05 | not −0.03 / −0.07 | **not 0.44 / 0.21** | – |

**Counts.** 9 of 10 stay profitable. Against their records without hold, Sharpe moves −0.06 to +0.19 on those 9 (8 within
±0.15). The one that stops paying is the 3-day two-sided reversal: 1.16 → 0.44 (the old rule's defect had it at −0.03).

**Outcome: B1 on 9 of 10, B2 on 1.** The hold is neutral on books that already pay, one-sided and two-sided alike (rsi
side: 1.03 → 0.97), and it lifts the longest hourly one (nearness to highs, 168 bars: 1.05 → 1.24). It costs the
quick two-sided reversal its quick reversals: a 3-day bet held while the forecast turns the other way. Its closing
time is the next thing to read (topic 34's diagnosis) before anything is changed.

**Check C passed** (`topics/30_review/opt2_check_c.py`, on the 10 books and the 4 pilot books):
- the engine's position equals `core/holding_period.py` replayed from the recorded forecast and target, with the
  engine's own trade approvals: 0 bars differ on about 2.1 million;
- positions on the other side of the forecast: within their bets' horizon, as defined (a long bet held through a turn
  of the forecast). After their bets: 76 bars on the 2 two-sided books, all tiny leftovers (−0.01 to −0.07) that the
  trade band refuses to close (both changes below 0.2), the band's rule from before the hold. The brief's "0 % held
  against the forecast" was too strict: it contradicted the side-switch case of the definition.

## Reading, the parallel test (topic 37, option D)

| Part | Where | Books | Start → end (Paris) | Time |
|---|---|---|---|---|
| A | this session | 1 hourly, 3 daily | 14:43 → 15:03 | 20 min |
| B | its own session | 1 hourly (240 bars, with unseen dates), 2 daily | 14:44 → 15:41 | 57 min |
| C | its own session | 1 hourly (168 bars, more coins, with unseen dates), 1 daily | 14:44 → 15:56 | 72 min |

The 9 books took 72 minutes side by side, against about 149 minutes one after another (the sum of the 3 parts): about
2 times faster, with no result changed (one engine, one commit). The cost: each new session built its venv (under 1 min),
its model use was small (about 0.4 USD each at start), and merging back took 2 merges in which the INDEX files were
merged row by row (10 files each, no row in conflict). The longest part sets the time: a better split balances by
expected time (hourly books with more coins first).

## Step back: hourly bars, where we are (2026-11-20, 16:20 Paris)

**1. Hourly books that pay exist: 3, all hourly versions of daily ideas with horizons of days.** On the corrected rule:
| Idea | Daily (its own record) | Hourly, held |
|---|---|---|
| nearness to highs, more coins | 1.25 / 1.67 | 1.24 / 1.49 (168 bars) |
| golden-cross momentum, more coins | 0.90 / 0.88 | 1.06 / 0.80 (240 bars) |
| dual momentum | 1.06 / 1.22 | 1.05 / 1.19 (72 bars) |

(Sharpe / Calmar after costs.) An idea that pays on daily bars pays about as well on hourly bars when each bet is held
for its horizon (the operator's premise). Hourly bars add no edge yet: the same idea, about the same result.

**2. The hourly-native ideas (the intraday briefs) do not pay, for 3 reasons the diagnosis shows** (`common/book_diagnosis.md`;
move over the horizon after the bot can act, against a round trip of about 21 bps measured):
| Kind | Books | Move / round trip | Market's share of the gain | Why it does not pay |
|---|---|---|---|---|
| short horizon (2 to 4 bars) | settlement-move, late-evening rebound, post-settlement decline | 4 to 13 / 21 bps | – (the books lose) | the move is smaller than a trip |
| long horizon, wrong timing | deep-decline, fresh-drop-rebound (72) | −25 and −40 / 21 bps | 252 %, 211 % | the bets lose against the coin's drift; the small gain is the market's (step 5 confirmed them: its measure and the book's bets do not agree) |
| long horizon, a real edge | volatile evening-fall (24) | **56 / 21 bps** | 27 % | fails Calmar only (0.694 against 0.75), on 6 coins |
| long horizon, trend | grinding-rises (72) | 42 / 21 bps | 73 % | the gain is mostly the market; fails Calmar |
| (paying, for comparison) dual momentum (72) | | 37 / 21 bps | 49 % | – |

**3. Levers tried and set aside:** the `standardise` window (pilot: flat); closing leftovers below the trade band
(`topics/30_review/close_rule_replay.py`: the leftovers are 52 % of volatile evening-fall's time in a position, all
under 0.2, but closing them adds +0.01 to +0.02 of Sharpe).

**The paying books' own diagnosis** (the two "more coins" books were read in the sessions that ran them, where their
bar files are): golden-cross more coins (240): move 233 against a trip of 22 bps (10.6 times), market's share 52 %,
still rising at twice its horizon (468 bps at bar 480); nearness more coins (168): 121 against 22 (5.5 times), 47 %,
still rising at twice its horizon (175 at bar 336); dual momentum (72): 37 against 21 (1.8 times), 49 %, still rising at
twice its horizon (63 at bar 143). Their moves run longer than their horizon: they close early, not late.

**4. What the 3 paying books have that the others lack:** a move per bet well above a trip and from the idea's timing
(market share under half), and two of the three are "more coins" versions (step 7.b, an idea on more data):
diversification over 15 to 20 coins lowers the book's deepest fall, which is what Calmar reads.
