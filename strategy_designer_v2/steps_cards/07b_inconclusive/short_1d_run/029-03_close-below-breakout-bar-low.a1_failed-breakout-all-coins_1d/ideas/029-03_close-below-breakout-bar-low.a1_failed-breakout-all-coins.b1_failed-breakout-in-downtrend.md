---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
line: 7.b inconclusive
backtest: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, only while the coin's 60-day return is negative, and the further that close sits below the breakout day's low, the larger the fall.
Consequence: A trader would short failed breakouts that are counter-trend rallies in a falling coin, and refuse to short them while the coin is in a rising 60-day trend.
Why:
- F2: The effect appears only when the failed breakout comes inside a falling market.
- F3: The effect changes sign from year to year, so the market's own regime drowns it. 2022 gives +16.5 % (t 3.44, 9 cases) and 2025 +3.75 % (t 2.52, 20 cases), while 2020 gives −4.83 % (t −1.68, 9 cases) and 2024 −1.91 % (t −1.05, 24 cases).
- F1: The tested result is on the predicted side but held down by a few extreme cases. The 113 cases have a mean short-signed unusual move of +1.33 % over 5 days (t 1.09), while their median is +2.08 %, 64 % of them are positive, the 5 % trimmed mean is +1.74 % and the Wilcoxon p is 0.019; the single worst case is −84.5 % against a best of +51.8 %.
- F7: The test already used all 19 coins on all four folds of daily data, so more of the same data cannot lift the t. A clear answer needs the idea narrowed to where its move shows (F2).
