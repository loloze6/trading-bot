---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the larger the product of that signal's excess past 365-day power for 5-day returns and today's deviation of nearness from its 365-day level, when it implies a rise, the larger the coin's fall over the next 5 days.
Consequence: A trader would short on the nearness-power reversal reading in any coin, sized by the reading, without waiting for a negative 20-day return.
Why:
- F6: The tested reading's falls are not specific to falling coins. Strong shorts (forecast below -0.5) where the 20-day return was not negative were followed by -1.77 % beyond drift (t -2.41, 176 cases). In the active regime they were followed by -0.89 % (t -2.27, 714 cases), and active-regime cases rose beyond drift in 2023 (+0.29 %, 194 cases).
