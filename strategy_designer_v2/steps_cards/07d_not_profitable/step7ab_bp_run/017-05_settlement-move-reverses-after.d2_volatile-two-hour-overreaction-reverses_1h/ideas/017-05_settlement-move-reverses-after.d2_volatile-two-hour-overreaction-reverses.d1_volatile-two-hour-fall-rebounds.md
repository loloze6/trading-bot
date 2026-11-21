---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's large 2-hour fall, made while its 24-hour volatility is high, is followed by a rise over the next 24 hours, at any hour of the day. The larger the fall against the coin's usual 2-hour move, and the higher its 24-hour volatility against its 30-day average, the larger the rise.
Consequence: A trader buys sharp falls in volatile markets and holds about a day, instead of also shorting sharp rises, which keep going and carry the book's losses.
Why:
- F2: The loss comes from the shorts taken after rises. Trades with |entry forecast| above 2 earn +0.29 % to +0.80 % before fees when long. When short they lose -0.60 % to -1.16 % (34,781 trades with |forecast| above 10).
- F3: In high volatility (24-hour volatility at or above its 720-bar average), a 2-hour fall of at least 2 usual moves is followed by a large unusual rise. It is +60 bps over 8 hours (t 4.4, n 1,361), +172 bps over 24 hours (t 4.8, n 447) and +180 bps over 48 hours (t 3.0, n 218). The same-sized 2-hour rise is followed by only +21 bps of decline over 8 hours (t 1.9), +14 bps over 24 hours (t 0.5) and a 141 bps continuation over 72 hours (t -1.8).
- F4: The reversal is graded by the size of the 2-hour fall, and only the larger falls clear the 19 bps cost. On the 8-hour grid, in high volatility, the unusual move counted in both directions is 3.5 bps for |z| up to 1 (n 11,421) and 17 bps for 1 to 2 (n 4,477). It rises to 32, 50, 53 and 68 bps for 2–3, 3–4, 4–6 and above 6. After falls alone, over 24 hours, it is 7, 36, 87, 222 and 541 bps (t 3.5 in the top bin).
- F5: The reversal is also graded by how high volatility is against its average. For 2-hour moves of at least 2 usual moves, the 8-hour unusual move is -41 and -28 bps where the ratio is below 1.0. It is -6 bps at a ratio of 1.0–1.3, then 45, 67 and 92 bps at 1.3–1.7, 1.7–2.5 and above 2.5 (t 2.8, 3.6 and 2.8). Over 24 hours it reaches 163 bps at 1.7–2.5 (t 3.5).
- F8: The after-fall rebound over 24 hours holds in both halves of the windows. It is +82 bps in w1–12 (t 1.7, n 199) and +244 bps in w13–24 (t 4.7, n 248). By coin, the 24-hour moves after both directions are positive in 5 of 6 coins, with LTC the exception.
