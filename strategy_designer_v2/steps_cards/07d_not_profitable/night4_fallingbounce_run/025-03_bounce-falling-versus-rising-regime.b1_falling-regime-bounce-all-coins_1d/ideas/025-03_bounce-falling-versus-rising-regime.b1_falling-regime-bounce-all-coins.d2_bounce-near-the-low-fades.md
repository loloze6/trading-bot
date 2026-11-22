---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin whose 90-day return is negative, a one-day rise of several usual daily moves is followed by a lower 5-day return the closer the coin's close stands to its lowest close of the past 90 days.
Consequence: A trader would fade a bounce that starts near the coin's 90-day low, and refuse to fade one from a coin already far above that low.
Why:
- F4: On the 5-day grid, the short signals made in the falling regime fade only while the coin is still deep in its fall. In the most negative quarter of 30-day returns (mean −28 %) the unusual 5-day move is −3.9 % (t −3.29, 135 cases). In the quarter whose 30-day return is already positive (mean +21 %) it is +1.3 % (t +1.15, 134 cases). The grading is monotone across the four quarters (−3.9, −1.5, −0.1, +1.3 %).
- F5: The same grading holds for distance from the 90-day low. Bounces that start within about 6 % of that low are followed by −4.3 % (t −2.42, 37 cases), and those within 14 % by −3.5 % (t −2.07, 36 cases). Bounces from a coin already 60 % above its low are followed by +4.2 % (t +1.60, 37 cases), which is a move against the short.
- F2: The book's deepest fall ran −59 % over 1014 days, across w15 to w23. Over that stretch the short positions lost −0.70 in summed daily gain and the long positions only −0.06, so the shorts carried almost all of it.
