---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days, only after a falling weekend, and the further fall is larger the higher the weekend's volatility compared with the previous week.
Consequence: A trader should follow turbulent weekend drops into Monday and Tuesday, more so the more turbulent the weekend, and refuse to chase turbulent weekend rallies.
Why:
- F2: The effect sits only in the most turbulent weekends: in the top fifth of the weekend-to-prior-week volatility ratio the unusual move is +1.38 % per case (t 3.14, 446 cases, strength 0.197, book +0.92 % per case), while the bottom two fifths show −0.19 % and −0.35 % (t −0.66, −1.05) and the middle fifths +0.10 % and +0.32 %.
- F6: The continuation comes from falling weekends: cases following a falling weekend have an unusual move of +0.55 % (t 2.32, 1023 cases), and cases following a rising weekend have −0.002 % (t −0.01, 1205 cases).
- F7: The move is spread over both days, +0.16 % on day 1 (t 1.36) and +0.11 % on day 2 (t 1.13), and nothing follows on days 3 to 4 (−0.03 %, t −0.20), so holding longer would not add gain.
