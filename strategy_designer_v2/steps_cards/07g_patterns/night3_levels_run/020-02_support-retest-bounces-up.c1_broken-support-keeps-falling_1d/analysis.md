---
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3823 USD
---
## Findings
- **F1:** Nothing in the bars stood out once I account for how many angles I tried (11 one-bar and multi-day features at a 5-day horizon, a volatility interaction, weekday, year, window half and coin). The best single result was the book's own forecast: the 5-day unusual move in units of the coin's usual move rose from -0.080 in the most negative forecast quintile to +0.082 in the top quintile (t 2.82, 3419 non-overlapping cases). No other feature's top-minus-bottom quintile reached |t| 1.4.
- **F2:** Where the forecast was zero (no 90-day swing low above the close), the next 5 days ran above the coin's normal drift on all 6 coins, by +0.044 to +0.235 of a usual move. Where it was negative, they ran below it on all 6, by -0.012 to -0.077. The forecast-to-move rank correlation was only 0.018 to 0.084 per coin, so this is a weak form of "near the highs keeps rising" (earlier F3), not a new effect.
- **F3:** The book loses on every coin, -0.016 % to -0.147 % a day, against holding's +0.067 % to +0.155 % a day. Its short cases face a normal drift of -0.59 % per 5 days against them. The unusual move is +0.12 % (strength 0.005), 0.6 times the 0.19 % round-trip cost, and the total move is -2.5 times that cost, so no change of holding or sizing can make this idea pay.
- **F4:** When volatility was high, a 20-day move was followed by 5 days in the same direction: +0.80 % beyond drift, strength 0.067, t 2.48 over 1421 pooled cases. This does not hold up:
- **F5:** Next-day returns on Thursday and Friday beat Monday and Wednesday on all 6 coins, by +0.31 % to +0.73 % (Welch t 1.7 to 3.1). This also does not hold up:

## Ideas
- No ideas: After about 40 comparisons, nothing beyond the forecast's own weak echo of the known near-highs drift (F1, F2) is clearly more than chance: high-volatility momentum (F4) rests on one half of the windows and one coin, and the weekday gap (F5) is unstable across years and is not a graded situation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
