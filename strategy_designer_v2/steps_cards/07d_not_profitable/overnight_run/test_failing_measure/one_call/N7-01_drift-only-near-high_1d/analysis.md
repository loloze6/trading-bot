---
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
idea tested: N7-01_drift-only-near-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3556 USD
---
## Findings
- **F1:** The Calmar failure comes from deep falls inside single windows, not from one bad stretch. The book's largest falls within a window were −33.4% (w10), −31.6% (w13), −30.7% (w22), −30.3% (w12) and −29.8% (w7), against a 10-day block mean of +1.36%. Across the 304 non-overlapping 10-day blocks of the book's daily returns, the worst was −18.4%, and the worst 10% of blocks hold 54% of all losses.
- **F2:** Long blocks that start after a large 20-bar run-up are where crashes concentrate, and they do not pay for the risk. Over 5 bars, with each 5-bar period counted once, blocks in the top run-up fifth (20-bar return above 33%, n=222) earn only +55 bp over the coin's mean (t=0.54). 18.0% of them lose more than 10%, and their 5th percentile is −19.0%. Blocks after a moderate 5.5–11.5% run-up (n=222) earn +177 bp (t=2.32), and only 6.3% lose more than 10%.
- **F3:** The gain is concentrated right after a fresh high and fades as the high ages, while the crash risk does not fade.
- **F4:** Where the close sits in its 20-day range adds held exposure with no gain outside the very top. Blocks with the close in the lower half of the range earn −117 bp (n=41, t=−0.78). Blocks with the close at 0.9–0.99 of the range earn only +18 bp (n=175, t=0.19), yet 13.7% of them lose more than 10%.
- **F5:** Held-day crashes rise steeply with recent volatility. The share of held days losing more than 8% grows from 0.7% in the lowest 20-day-volatility fifth to 7.9% in the highest (1117 days each). That top fifth still carries the largest 5-bar excess, +202 bp (n=222, t=2.03), so volatility alone raises both the gain and the falls.
- **F6:** In several falling windows the book lost more than simply holding the coins, which points to failed breakouts in down markets.

## Ideas
- `N7-01_drift-only-near-high.d1_overextended-highs-crash-more` (from F2, F1, F5): When a coin makes a new 20-day closing high after a 20-bar rise far larger than its usual 20-bar move, its next 5 bars fall by more than 10% more often than after a high reached through a moderate rise, without a larger average gain.
- `N7-01_drift-only-near-high.d2_drift-fades-with-high-s-age` (from F3, F1): The excess rise after a new 20-day closing high is carried by the first few bars after the high and is gone once the high is more than about 10 bars old, while the risk of sharp falls stays the same.
- `N7-01_drift-only-near-high.d3_rise-needs-close-at-high` (from F4, F3): A close that slips back from a fresh 20-day high to just under the top of its range, or below its middle, is followed by below-average 5-bar returns. The rise continues only while the close stays at the high itself.
- `N7-01_drift-only-near-high.d4_breakouts-fail-in-downtrends` (from F6, F1): In a coin whose longer trend is falling (close below a long moving average), new 20-day closing highs are followed by below-average returns: they are failed bounces, not new trends.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
