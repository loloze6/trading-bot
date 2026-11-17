---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues
line: 7.d not profitable
backtest: 013-03_breakout-above-high-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the further above that high it closes, the larger its return over the next 10 days, only while its close stays above that broken high, and the more so the fewer days have passed since the break.
Consequence: A trader should hold a fresh break for about ten days rather than one day, weight it by how far it cleared the high and how fresh it is, and drop it once price closes back below the broken level.
Why:
- F2: The forecast resets to zero the day after a break. Once the new high joins the 365-day window, the coin is no longer above it, so positions end almost at once. 145 of 166 trades last 2 days or less and net only 0.10 % on average. The 21 trades held longer than 2 days carry the book: mean net 15.5 % for 2–5 days, 24.5 % for 5–10 days and 116.7 % for 10–20 days.
- F3: The break does continue, but over days, not over one bar. Across the 75 fresh breaks (the first break after at least 10 days without one), the coin rose on average 2.1 % over the next day, 6.1 % over 5 days, 9.5 % over 10 days (n 73) and 15.8 % over 30 days (n 52). The book captured almost none of this.
- F4: The follow-through fades with the age of the break. While the close stays above the broken high, the coin's daily return above its own mean is:
- F5: Breaks that hold continue; breaks that slip back do not. Breaks that did not close back below the old high within 5 days returned 23.0 % over 30 days (n 34), against 2.1 % for breaks that fell back (n 18). Fall-backs were 38 % of breaks. Within 30 days of a break, days spent above the old high earned +0.00276 daily excess (t 1.75, n 1517), against +0.00115 for days back below it (n 600).
- F6: The size of the break predicts the next 10 days, but not later. At the break itself, the 10-day return rises with the distance above the old high (slope 0.0121, t 3.15, n 73). The 30-day slope is weaker (t 1.87, n 52). On the later days, the distance above the broken high carries nothing: daily slope t −0.41 (n 1517), 10-day grid slope t 0.15 (n 141).
- F1: The book is almost never in the coin, so it cannot earn. The forecast is positive on only 0.7–2.4 % of bars per coin, and the book holds a position on 0.6–2.7 % of bars (248 of 17,044 coin-days). Days out of the coin earn −0.000018 on average. That is why the mean daily return is 1.5e-06 and trades per bar is 0.0096.
