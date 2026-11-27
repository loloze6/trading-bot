---
line: 7.g patterns
backtest: 081-01.d3_deep-up-day-fade-outside-uptrends_1d
idea tested: 081-01.d3_deep-up-day-fade-outside-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4535 USD
---
## Findings
- **F1:** The fade lives in up days that follow a down day: deep up days (top depth tertile) after a down day were followed by an unusual next-day move of −1.27 % (t −3.23, 1216 cases on 371 days), against −0.34 % (t −0.71, 612 cases on 224 days) after an up day; the middle tertile shows the same split (−0.46 %, t −2.09 against −0.14 %, t −0.53).
- **F2:** The fade keeps building into the second day: over the next 2 days, deep up days (top depth tertile) moved −1.24 % against the coin's 2-day drift (t −2.94, 1817 cases on 492 days), against −0.33 % (t −1.28) for the middle tertile and +0.72 % (t 2.04) for the shallow tertile. That is about three times the 1-day move the tested idea captures; per case, the 1-day total move is only 1.1 times the 0.22 % cost of a trade.
- **F3:** The fade is graded by depth: by up-day depth quintile, the next day's unusual move goes +0.20 % (t 0.68), +0.07 % (t 0.31), −0.47 % (t −2.42), −0.71 % (t −2.33), −1.01 % (t −2.53); down days at the same depths show nothing (t from −0.07 to 1.91, the deepest quintile +0.88 %).
- **F4:** Inside the deep tertile, the size of the up day adds nothing: by tertile of the day's return in 20-day swings, the next day moves −0.91 % (t −2.46), −0.94 % (t −2.35) and −1.06 % (t −1.83). The depth carries the effect, not the strength of the bounce.
- **F5:** The deep-up fade is absent in rising markets: the deep tertile gives +0.01 % (t 0.04) there, against −1.24 % (t −2.19) in choppy and −1.09 % (t −1.80) in falling markets. This is consistent with the tested idea's exclusion.
- **F6:** The fade is broad across coins: all 13 coins have a negative mean after deep up days, 6 of them with t below −2: XMR −1.45 % (t −3.59), LTC −1.07 % (t −2.92), ZEC −1.08 % (t −2.62), XRP −0.87 % (t −2.52), BTC −0.80 % (t −2.13), ADA −0.97 % (t −2.06).
- **F7:** Outside rising markets, the deep fade is larger in agitated markets than in calm ones: −1.52 % (t −2.23, 113 days) against −0.74 % (t −1.62, 173 days). Given how many angles were looked at, this is not separable from chance on its own. Its falling-agitated part also overlaps the bounce fades the map already holds (074-01.g1.d1, 074-01.b1.b1.b1.b1.d1.g1).
- **F8:** The book is a short-beta book: its daily returns correlate negatively with the coins' in every window (−0.14 to −0.65). On its best 5 % of days the coins fell −6.9 % on average, and on its worst 5 % they rose +5.8 %. This is why its Calmar (0.26) and its Sharpe against holding (−0.13) fail.

## Ideas
- `081-01.d3.g1_first-relief-bounce-fade` (from F1, F3, F5, F6): In any market except one where the coin has been rising over the last 60 days, the first up day after a down day that closes deeper below the coin's 20-day high, measured in its own usual daily swing over the last 20 days, is followed by a larger fall over the next day.
- `081-01.d3.g2_deep-up-day-two-day-fade` (from F2, F3, F4, F5): In any market except one where the coin has been rising over the last 60 days, a day that closes up while sitting deeper below the coin's 20-day high, measured in its own usual daily swing over the last 20 days, is followed by a larger fall over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
