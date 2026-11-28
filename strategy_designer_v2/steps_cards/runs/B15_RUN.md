# B15 (2026-11-28): can a run's test confirm an effect that is real? (written before the run)

**The operator (2026-11-28):** "Go for all" (the handover), then "Go" on the sample of 30 and 3 sessions. No model
call; no research budget.

## Purpose
One question: **when an effect is confirmed on the 25 portfolio coins, how often does a run's test, on its 8 drawn
coins, confirm it?** And on 12 or 16 drawn coins?

Why: in the new data use 61 ideas were tested, 1 confirmed, 0 profitable (`PILOT_A4_RUN.md`, `NIGHT10_RUN.md`); in the
old one, nights 7 to 9, 157 of 477. Either the old confirmations leaned on their 6 coins, or 8 drawn coins are too few
to confirm what is real. Searching more before knowing which would spend budget on a test that may not be able to say
yes.

## Method (`topics/b15_review/b15.py`)
- **The sample:** 30 of the 108 strategies whose common record (25 coins) step 5 confirmed, drawn once by a fixed seed
  (`sample.json`: 22 daily, 3 four-hour, 5 hourly).
- **For each:** step 4 rerun on the 25 portfolio coins (the common record's own code; the bars were not committed),
  then step 5 with the strategy's own stored `measure.py` on:
  1. the 25 coins as the common record did (no direction check): must give the stored verdict again, or the
     difference is explained (the proof that the rerun is the same record; known: records made before A12 hold about
     3 windows per early coin that the count now leaves out);
  2. the 25 coins as a run does (the direction check on the check half);
  3. 40 draws of 8 coins, 40 of 12, 40 of 16, by the research draw's rule among the 19 drawable coins (seeds
     `b15_draw_001` to `040`, the same draws for every strategy), each as a run does.
- **Read:** per strategy, the share of draws that confirm, at each size; over the sample, the mean share. Also why a
  draw fails: the t under 2, or the direction check.
- Three sessions (Sonnet), 10 strategies each, each on its own branch; results are one small file per strategy.

## Expected outcomes
| # | Outcome | Shown by | What it would mean |
|---|---|---|---|
| T1 | The test on 8 coins sees real effects | most strategies confirmed on most draws of 8 (mean share at or above 70 %) | 8 coins are enough: the new search found nothing because its ideas had no effect, not because of the test |
| T2 | The test on 8 coins misses real effects, more coins repair it | mean share on 8 clearly under 50 %, rising with 12 and 16 | a rule on the number of coins per run, proposed to the operator with its engine cost |
| T3 | The test misses them at every size | low shares at 8, 12 and 16 (the 19 drawable coins differ from the 25, or the direction check stops them) | the cause is not the number of coins: read which check fails |
| T4 | The measurement itself fails | the 25-coin rerun does not give the stored verdict for unexplained reasons | fix the tool before reading anything |
A limit known before the run: these 108 were confirmed on the 25 coins, of which a draw's coins are a part, and most
were first found on the old 6 research coins; the shares say what the test sees of effects already selected this way,
not of new ideas.

## Reading
(after the run)
