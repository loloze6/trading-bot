---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: At Sunday's close, a coin's Saturday return continues in the same direction over the next 2 days (Monday and Tuesday), and the continuation is larger the larger Saturday's return is relative to the coin's 20-day daily volatility.
Consequence: A trader holding the Sunday-close reversal bet would be leaning against a Saturday move that tends to keep going, and could trade with Saturday's move instead, sized by its vol-scaled size.
Why:
- F1: On Sunday bars, the weekend splits into two opposite effects. In a joint regression over 4325 Sunday cases, Saturday's vol-scaled move carries on into Monday–Tuesday (beta +0.216, t 5.97; into Monday alone +0.135, t 5.55). Sunday's own move reverses (beta −0.078, t −2.39; Monday alone −0.071, t −3.23). That is why the Saturday+Sunday return predicts continuation (slope +0.053, t 2.09) while the Sunday return alone predicts reversal (−0.092, t −2.82).
- F2: Sunday's reversal is a market-wide move in time, not a difference between coins on the same date. Measured per date, sign(Sunday move) × the next days' vol-scaled return is −0.111 for one day (t −2.51), −0.178 for two days (t −2.85) and −0.224 for three days (t −2.72), over about 340 dates. The per-date cross-coin slope has the opposite sign (+0.060, t 1.46). For the next day, only 3 of 19 coins have a continuation slope.
