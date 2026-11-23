---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday-to-Sunday close-to-close fall, measured in percent of its price, is followed by a rise over the next 3 days (Monday to Wednesday), and the deeper the percent fall, the larger that rise, while the coin's last 30 days have been calm against its last 180 days; the calmer they were, the larger the rebound.
Consequence: Hold the Monday-to-Wednesday rebound long in calm months and stay out of it when the coin's recent volatility is well above its usual level.
Why:
- F1: The book's deepest fall, −26.7 % against a yearly return of +10.2 % (Calmar 0.30), ran over 412 days from w3 to w7, while the coins' summed daily returns fell −69.8 %. The book lost −22.1 % in that stretch: −10.5 % in w4, −7.3 % in w5 and −4.3 % in w7. In w4 to w7 every one of its Monday, Tuesday and Wednesday holdings lost (−8.1 %, −12.0 %, −7.0 % summed) as the coins kept falling on those weekdays (−42 %, −25 %, −31 %). In every window from w8 to w24 the book gained (+1.9 % to +5.8 % each, except w13 at −1.5 %).
- F4: Split by the coin's 30-day daily volatility against its 180-day volatility, the quarter of cases with the most excited volatility rebounded only +0.42 % (t 0.89), with the widest spread of position gains (0.048 against 0.022 to 0.027). The calmer three quarters rebounded +1.18 % to +1.81 % (t 3.1 to 4.9).
- F5: Rebuilt from the record, with the Monday-to-Wednesday holdings removed after Sundays whose prior 30-day return was below −12.5 %, the book's Calmar is 0.83 (deepest fall −13.7 %, yearly +11.4 %, Sharpe 0.88). Leaving out the excited-volatility cases instead gives a Calmar of 0.79. Leaving out both gives a Calmar of 0.90 (deepest fall −9.0 %, Sharpe 1.02).
