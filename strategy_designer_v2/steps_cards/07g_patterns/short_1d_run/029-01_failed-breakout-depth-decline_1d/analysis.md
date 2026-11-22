---
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline_1d
idea tested: 029-01_failed-breakout-depth-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5284 USD
---
## Findings
- **F1:** The tested failed-breakout situation carries no downward follow-through: grid cases with an active failed breakout had a 5-day excess return of +0.16 % (t 0.22, n 272), against −0.19 % (t −0.94, n 2841) on other days, and the book's own cases show an unusual move of −0.13 % (t −0.29, 617 cases).
- **F2:** Failed breakouts are more often followed by a fresh break higher than other days are: a new close above the prior 20-day high came within the next 10 days on 48.3 % of failed-breakout grid bars, against 40.2 % on the rest, which is the brief's own second refutation condition.
- **F3:** The opposite situation pays instead. Days whose close sits above the prior 20-day closing high are followed by an excess rise of +1.01 % over 3 days (t 2.50, n 528), +1.58 % over 5 days (t 2.12, n 306) and +4.12 % over 10 days (t 2.36, n 167). Non-breakout days are −0.13 %, −0.19 % and −0.56 %. The strength is 0.11 to 0.23 of a usual move, and the 5-day total move is about 8 times the 0.19 % cost of a trade.
- **F4:** The breakout continuation in F3 is fragile. Without XRP it falls to +0.77 % over 3 days (t 1.98, n 463) and +0.43 % over 5 days (t 0.73, n 270). It is concentrated in 2018–2021 (+4.20 %, t 3.06, n 131), against 2022–2025 (−0.38 %, t −0.50, n 175). Only 55 % of coin-windows are positive. Given the many angles examined, it stands at the edge of chance.
- **F5:** Inside breakouts the grading by size is weak and not monotone: the 5-day excess by tercile of breakout size over 20-day volatility is +1.43 %, +0.64 % and +2.65 % (Spearman 0.069, n 306). By count of breakout closes in the last 5 days it is +0.72 %, +0.94 % and +2.18 % for 1 to 3 closes, then falls back.
- **F6:** The next day's excess return after a Friday bar is +0.31 % (t 3.76, n 2479) and is positive in both halves of the sample (t 2.99 and t 2.29). The other weekday effects do not hold across halves: Thursday is t 3.30 then t 0.10, and Wednesday is t −2.60 then t −0.99. A fixed calendar condition with no grading cannot be written as an idea here.
- **F7:** The other angles show nothing clearly beyond chance among about ten bar features. These were the 1-day, 5-day and 20-day returns, volatility, range, close location, upper wick, volume z-score and distance from the 20-day high or low, read against 5-day excess returns. Every Spearman correlation is below 0.05; the largest is volume z-score at 0.045 (p 0.015, n 2843).

## Ideas
- `029-01_failed-breakout-depth-decline.g1_breakout-size-continues-higher` (from F3, F4, F5, F2): The further a coin's daily close sits above its highest close of the prior 20 days, measured in units of its 20-day daily volatility, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
