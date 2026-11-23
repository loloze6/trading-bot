---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power over the following 90 days. The turn shows on the rising side: the more strongly this reversal points up, the higher the coin's return over the next 5 days.
Consequence: A trader should act on the turnaround of a nearness-to-high relation only by buying, in proportion to the reversal's strength, and refuse the shorts that lost the book 41 % in a rally.
Why:
- F1: The book's deepest fall, -41.2 % against a Calmar of 0.37, is one episode from w14 to w17 (2020, 347 days to the trough): the book lost 40.6 % while holding its coins gained 195 %. The book fell because it held shorts through a broad rally, and it summed between -1.4 % and -8.8 % in each of w14, w15, w16 and w17, while holding rose 33 % to 54 % in three of those windows.
- F2: The losses come from the short side. Bars held short earn -0.033 % per bar (10,664 bars), while bars held long earn +0.119 % per bar (11,964 bars), and the book is short on 44 % of its coin-bars.
- F3: Shorts lose most when the coin is rising or sits near its high:
- F4: The rising 30-day return also carries an effect of its own, so it cannot serve as the repair's condition:
- F6: The rest of the book passes: Sharpe 0.70, 0.16 above holding, lowest Sharpe with one window left out 0.56. Calmar is the only measure that fails, and the shorts held through F1's rally are what fail it.
