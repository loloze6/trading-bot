# Run brief: combining two strategies (2026-11-22, written before the test)

**Purpose (operator):** "the potential of combining two strategies together ... and, at the opposite, combining two
strategies that are similar; for both, observe how the results fluctuate"; then "see if the similarity check is indeed
giving relevant outcome". Two ways of combining, on three pairs of paying books (`paying_rerun_run`, today's engine):
- **A. Two books side by side:** each keeps its own position on half the capital; the combination's daily return is the
  mean of the two books' daily returns (from their records; no new backtest).
- **B. One config, components weighted** (the mechanism the operator named): one forecast, the weighted mean (0.5
  each) of the two ideas' components, one position. Where one idea has a gate (a regime rule) and the other none, the
  gated regime holds both components and the other regime the ungated one alone. One holding period: the shorter of
  the two horizons (no bet held beyond its own idea's horizon). One backtest per pair, steps 4 and 6, on the coins both
  books trade.

| Pair | Book 1 | Book 2 | Share explained (similarity register) |
|---|---|---|---|
| different | strong monthly rises continue (momentum, 1d, 6 coins, holds 5 days) | volatile reversal completes quickly (reversal, 1d, BTC and ETH, holds 3 days) | 0.00 |
| in between | rising month, weekly momentum (1d, 6 coins) | high RSI, trend continuation (1d, 6 coins) | 0.80 |
| similar | strong rises keep rising (1d, 6 coins) | strong monthly rises continue (1d, 6 coins) | 0.99 |

**Measures:** each book alone and each combination: Sharpe, Calmar, deepest fall, the standard deviation of the daily
returns, the mean daily return (step 6's definitions), on the coins both books trade, folds A to D; for the different
pair also as recorded (each book on its own coins) and on the unseen dates (2016-17, 2026).

**Expected outcomes:**
| Pair | Expected | If not |
|---|---|---|
| different | A: the daily standard deviation and the deepest fall clearly below both books'; the Sharpe above both | the similarity check's "unrelated" does not mean "combine well": read why |
| similar | A: about the same as either book; nothing gained | a 0.99 share explained hides a difference: read why |
| in between | A: between the two | - |
| every pair, B against A | close to A, a little better where the forecasts net out (fewer trades, lower costs) | B differs much: the shared gate, the single holding period or the caps change the books; record which |

**Note, written before:** for A the result follows largely from the correlation of the two books' daily returns, which
the similarity check measures; A agreeing with the check is expected by construction. The tests of the check's use are
B and the unseen dates.

**Changed before B ran:** two of the books were planned before the holding setting existed and hold nothing (the
reversal, the high RSI); "the shorter holding period" so became: a book that holds nothing makes its combination hold
nothing. The different pair runs on BTC and ETH (the reversal book's coins; BNB has no data).

## Reading (2026-11-22; 0 USD; A from the paying books rerun's records, B three daily backtests, the unseen dates four)
Folds A to D, on the coins both books trade (`topics/08_review/combine_test.py`, `combine_test_A.json`):
| Pair (correlation of daily returns) | Book 1 | Book 2 | A: side by side | B: one config |
|---|---|---|---|---|
| different (+0.05) | Sharpe 1.26, deepest fall 40.9 %, daily sd 1.86 % | 1.23, 20.8 %, 1.03 % | **1.66, 17.1 %, 1.08 %** | 1.73, 24.6 %, 1.73 % |
| in between (+0.90) | 1.04, 26.6 %, 1.55 % | 1.04, 30.4 %, 1.43 % | 1.07, 25.5 %, 1.45 % | 1.06, 25.2 %, 1.33 % |
| similar (+0.99) | 1.03, 33.5 %, 1.69 % | 1.04, 29.4 %, 1.59 % | 1.04, 31.5 %, 1.63 % | 1.04, 31.5 %, 1.66 % |

**A, as expected:** two unrelated books together have a higher Sharpe than either (1.66 against 1.26 and 1.23), half the
Calmar again (2.22 against 1.15 and 1.20) and a smaller deepest fall than either (17.1 % against 40.9 % and 20.8 %); two
near copies give nothing (1.04); the pair at 0.90 gives almost nothing (1.07). The similarity check's numbers say in
advance how much a combination gains (by construction for A, as written before the test).

**B is a clean test only for the similar pair**, and there it agrees with A. For the two others the config changes the
books: the engine takes the weighted mean of the components present in a regime, so a component alone in its regime
gets the full weight, not half; and a config has one holding period. In the different pair, momentum alone runs at full
weight on the calm days (about 80 %), so B is mostly more momentum: Sharpe 1.73 but daily ups and downs 60 % larger
than A's and a deeper fall (24.6 % against 17.1 %). **Combining books through one config's weights is not faithful
when a book has a gate or the two hold differently; two books side by side (A) is.**

**The different pair on the unseen dates (A, BTC and ETH):**
| Period (correlation) | Momentum | Reversal | A: side by side |
|---|---|---|---|
| 2016-17 (−0.15) | Sharpe 3.73, deepest fall 27.0 % | −0.41, 42.0 % | 3.18, 18.4 % |
| 2026 (−0.11) | −0.20, 20.1 % | −0.52, 25.7 % | −0.56, 18.6 % |
The two books stay unrelated out of sample (the check's reading holds), and together they still fall less than either
alone. But the reversal book does not pay on either unseen period, so the combination earns less than momentum alone in
2016-17, and loses in 2026 when both lose. **Unrelated is what makes a combination smoother; it pays only if each book
pays on its own.** The only non-momentum book found so far does not hold out of sample.
