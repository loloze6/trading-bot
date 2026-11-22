# Topic 45: why the research finds almost only long momentum, and what the workflow misses

Status: open (investigated 2026-11-22; changes for the operator's go)  
Where: research: step 6's rule (`06_profitability/helper/rule.yaml`), the books judged alone (topic 44), the one-coin rule
(`common/idea_definition.md`), step 7's lines  
Opened: 2026-11-22, the operator: "really surprised that we are struggling to find non-momentum and non-long-only
profitable strategies: investigate ... what the research workflow is missing".

## Question
Is it the market (nothing else pays on these coins), or the workflow (something else pays and the workflow does not keep it)?

## Seen (scripts and numbers in `topics/45_review/`; daily bars, fold years 2018-2025 only, never the unseen or sealed periods)
**A. The market (`facts.py`).** The core 6 coins rise +0.13 % a day on average with daily swings of 4.8 %; holding them
has a Sharpe of 0.53 (0.6 to 0.9 on most of the 19 coins). The market rises even below its 200-day average (+0.08 % a
day, against +0.17 % above). After a fall of more than 2 usual moves the next day averages +1.5 %; after a rise of more
than 2, +0.09 % (the drift). Daily returns reverse slightly (autocorrelation −0.07), weekly ones continue (+0.06). The
market explains 71 % of a coin's daily moves.

**B. Quick strategy families outside the bot (`sim.py`, Kraken's costs per coin, 40 % a year risk sizing):** on 6 and 19
coins, every short-only family loses (Sharpe −0.1 to −1.4); trend long only is the only family that passes step 6's
bars; one-day reversal has a Sharpe of 0.67 before costs and 0.00 after; ranking the coins against each other (long the
strongest third, short the weakest: a rule the workflow cannot express, one coin at a time) gives 0.32 to 0.49.

**C. Where the short side pays (`diag.py`):** in the two falling years only (2018: Sharpe 0.73; 2022: 0.32 to 0.70), when
momentum loses (−1.69, −1.39); it loses in the six others. Judged alone over eight years, a short book cannot pass; its
value is as a hedge, which no step judges.

**D. The books step 6 rejected (`rejected.py`, `rejected_books.csv`):** of 285 confirmed ideas, 95 profitable enough;
**50 others failed only on the mean daily return (0.05 % a day) and/or Calmar (0.75)**, with a Sharpe of 0.56 to 1.18,
above holding's. Five of them are unrelated to every paying book and trade both sides (about half their trades short):
| Book | Sharpe | Share explained by the nearest paying book | Momentum (022-03) alone, then with it at equal risk | Failed |
|---|---|---|---|---|
| 026-03.d3 Saturday move continues early week (1h) | 1.08 | 0.05 | 1.04 → 1.42 | mean 0.042 %, Calmar 0.61 |
| 022-04.b1 nearness power turns around (1d) | 0.92 | 0.03 | 1.04 → 1.35 | Calmar 0.54 |
| 016-03 late-evening rebound (1h) | 1.18 | 0.24 | 1.04 → 1.35 | Calmar 0.69 |
| 026-04.b2 heavy weekend moves continue (1h) | 0.89 | 0.07 | 1.04 → 1.26 | mean 0.024 %, Calmar 0.61 |
| 022-04.b2 volatility power turns around (1d) | 0.68 | 0.01 | 1.04 → 1.23 | mean 0.044 %, Calmar 0.26 |
Not yet tested on the unseen dates (the unseen test runs only on profitable books).

## Why it matters
The workflow keeps only what passes step 6 alone, and step 6's two bars that a diversifier rarely meets (a mean of 0.05 %
per calendar day, which grows with the position's size and the time in a position; a Calmar of 0.75 over eight years that
hold an 82 % market fall) reject the unrelated books it found. Step 7 learns from what passed, so each brief drifts back
to continuation (night 4: every brief; brief 029: 61 of 66 ideas from step 7's lines).

## Options
| Option | Gain | Risk |
|---|---|---|
| A. The unseen test on the five unrelated books now (step 4 with the unseen windows, no model call) | tells whether they hold out of sample before any rule changes | none |
| B. Step 6 judges size-free: Sharpe, Sharpe minus holding's, leave one window out, trades per day; the mean daily return and Calmar become informative measures | the unrelated books are kept and reach the unseen test and the register | more books pass: some weak ones; the unseen test and the similarity check stay the filters |
| C. A second way to pay: "adds to the portfolio" (the book improves the Sharpe of the paying books combined, at equal risk), judged with topic 44's method A | the short and hedge books are judged for what they are worth | a new measure, needs its definition and card |
| D. Several coins in one idea (relative ranking, market-neutral) | a family the one-coin rule excludes | a change to the idea's definition and step 4; small gain seen (0.32 to 0.49) |

Recommended: A first; then B; C with topic 44; D not now.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Links
`topics/45_review/`, `06_profitability/card.md`, topics 41, 42, 44, `runs/NIGHT4_RUN.md`, `runs/SHORT_1D_RUN.md`.
