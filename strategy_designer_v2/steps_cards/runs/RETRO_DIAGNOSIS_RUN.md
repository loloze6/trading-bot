# Run brief: the book's diagnosis on every past record (2026-11-20, written before the run)

**Purpose (improvement I1 of `topics/30_review/WORKFLOW_REVIEW.md`; topic 34's step 3):** before redesigning any step
around "is this effect large enough to trade", check on the records we already have that the notion tells paying books
from the others. Every backtest record whose bar files are in this container (21 runs, about 250 books, daily and
hourly) gets the diagnosis (`common/book_diagnosis.py`), next to its step 5 verdict and step 6 status. Code only, no model
call, no backtest.

**The readings used:** the move per bet over the horizon once the bot can act, net of the coin's drift, divided by the
round trip the backtest paid (the "edge ratio"); the market's share of the book's gain; the move on the signal's own bar.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| R1. The edge ratio separates | Profitable books have an edge ratio clearly above 1 (most above 2); most non-profitable books below 1 | I1 is supported: "a move worth several round trips" is the notion to put in `common/` and in steps 1, 2, 7 |
| R2. The market's share separates the rest | Among books with an edge ratio above 1, those that fail step 6 have a higher market share | I1 needs a second reading: the edge must come from the idea's timing, not the market |
| R3. Neither separates | Profitable and non-profitable books overlap on both | the readings do not explain step 6; rework the diagnosis before using it |
| R4. Step 5 and the bets disagree | Confirmed ideas whose edge ratio is at or below 0 (their bets lose against the drift) | how often step 5's measure is not the move the book captures (candidate D) |

**Limits known in advance:** books of the same idea appear several times (reruns, holding variants): counted per
record, and the duplicates named. In-sample: these are the folds the ideas were chosen on.

## Reading (2026-11-20, 20:19 Paris)

248 records diagnosed, 0 errors; 238 with a step 6 result (192 distinct ideas; reruns and holding variants counted per
record). Table: `topics/30_review/retro_diagnosis.csv`; script: `topics/30_review/retro_diagnosis.py`.

**R1, the edge ratio: partly. It is necessary, not sufficient.**
| Edge ratio | Books | Pay | Daily | Hourly |
|---|---|---|---|---|
| ≤ 0 (the bets lose against the drift) | 38 | 0 | 20 | 18 |
| 0 to 1 (the move does not cover a trip) | 53 | 0 | 17 | 36 |
| 1 to 2 | 25 | 3 (12 %) | 22 | 3 |
| 2 to 4 | 44 | 4 (9 %) | 27 | 17 |
| > 4 | 78 | 25 (32 %) | 72 | 6 |
**0 of the 91 books whose move does not cover a round trip pays**: none, daily or hourly. Above 4 trips, one book in
three pays. Hourly books sit mostly below 1 (54 of 80), daily books mostly above 4 (72 of 158).

**What stops a large edge from paying** (53 books with a ratio above 4 that do not pay, 50 of them daily): Calmar fails
for 50, the mean daily return for 42, beating holding for 29; 10 fail Calmar alone. Their median Sharpe is 0.52, against
1.04 for the paying ones. Step 5 called 34 of them inconclusive. So a large move per bet is not enough: there must be
enough of it (bets often enough to earn a daily return) and its falls must stay shallow.

**R2, the market's share: does not separate** (outcome R3 for this reading). Among books above 1 trip, the paying ones
have a median share of 39 % and the others 24 %, the opposite of the expected direction, and the ranges overlap. The
market's share explains individual books (grinding-rises), not the step 6 result across books. Step 6's "beats holding"
check already carries what it would add.

**R4, step 5 and the bets: they disagree often.** Of 123 confirmed books, **53 (43 %) have a move per bet that does not
cover a round trip**, and **11 (9 %) have bets that lose against the drift**. Those 11 are 5 ideas (deep-decline and
fresh-drop-rebound in several runs, up-jump reversal, and two daily ones: a large rise continuing five days, a
capitulation-volume rebound). Step 5 confirms that an effect
exists, not that the book's bets capture it.

**What it means for the improvements.**
- **I1 is supported, in this form:** "the move per bet, once a trader can act, covers several round trips" is a
  necessary condition (0 of 91 below 1 pays), not a promise. An idea below it cannot pay however it is held or sized.
  The data puts "several" at about 2 to 4 (12 % pay between 1 and 2, 9 % between 2 and 4, 32 % above 4).
- **A second notion is needed: enough of it.** The edge per bet times how often the idea bets, against step 6's daily
  return, and the depth of its falls. That is a book's yield, which step 2 and step 7 can reason about from an idea's
  frequency (how often its situation occurs).
- **The market's share stays a diagnosis reading**, not a notion for the steps.
- **Candidate D is supported:** 43 % of confirmed books cannot pay a trip. Step 5 measuring on the book's bets would
  have said so at the verdict.

## A second question on the same table: I3, do hourly bars catch more of a daily idea's move?

The 12 daily ideas retested on hourly bars (`retest_1h_run`, without the holding period), each against its daily record
(the same idea text; horizon in the same days):
| | Count of 12 |
|---|---|
| The hourly version's move per bet is larger than the daily one's | 2 |
| The hourly version's Sharpe is higher | 1 |
| Both pay / only the daily one / only the hourly one | 3 / 8 / 0 |

Per bet, the daily version captures more 10 times out of 12 (for example nearness to highs, more coins: 168 against
121 bps; dual momentum: 106 against 37). The hourly version computes the daily idea on hourly closes and bets on every
hourly rise of its forecast, many of them late in a move already made. **I3 as framed ("hourly bars catch the move
earlier") is not supported by the records.** Its real test would be a different plan, one entry when the daily
condition first holds during the day, which none of these books did. Not run: it needs its own plan design (step 3).

## A third question: candidate D, step 5 measured on the book's own bets

On the 230 judged records: the t of the move per bet (the holding period's bets: a rise of the forecast of at least
the band; one bet per grid cell of the horizon, so no move counted twice; from the signal bar's close over the
horizon, net of the coin's mean move over all its windows; median 1,807 bets per record), against step 5's verdict and
step 6. Script: `topics/30_review/retro_bet_t.py`; columns added to `retro_diagnosis.csv`.

| Rule for "the idea is real" | Books passing | Of which pay | Paying books caught (of 30) |
|---|---|---|---|
| Step 5 today: confirmed | 123 | 20 (16 %) | 20 |
| The book's bets: t ≥ 2 | 117 | 18 (15 %) | 18 |
| Bets t ≥ 2 and a move per bet of at least 1 round trip | 84 | 18 (21 %) | 18 |
| **Bets t ≥ 2 and a move per bet of at least 2 round trips** | **69** | **18 (26 %)** | **18** |

- Of the 123 books step 5 confirms, **45 show no reliable move on their own bets** (t below 2).
- Measured on the bets with the move covering 2 round trips, a confirmed idea pays one time in four (26 %) instead of
  one in six (16 %), and 18 of the 30 paying books are still caught (20 today). The 12 paying books neither rule
  catches are mostly step 5 "inconclusive" ones (10).
- **Candidate D is supported in this form:** step 5's verdict on the book's own bets, with the move per bet against a
  round trip, says "real and large enough to trade" with fewer false alarms, at almost the same catch.
- In-sample, the same folds: a design to propose with its proof (rerun past verdicts), not a rule yet.
