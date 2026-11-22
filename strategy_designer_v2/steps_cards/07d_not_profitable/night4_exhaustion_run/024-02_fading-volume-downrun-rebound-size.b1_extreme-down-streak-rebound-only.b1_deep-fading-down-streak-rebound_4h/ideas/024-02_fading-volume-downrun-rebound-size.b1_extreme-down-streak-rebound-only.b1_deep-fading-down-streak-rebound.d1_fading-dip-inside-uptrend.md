---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while its price stands above its 30-day average. The further above that average, counted in the coin's typical four-hour move over the past 30 days, and the larger the streak's loss in that move, the larger the rise.
Consequence: A trader buys fading-volume down-streaks as dips inside an uptrend and refuses the same streaks when the coin is below its monthly average, where the rebound is absent and the deep falls occur.
Why:
- F3: The rebound appears when the coin is in an uptrend. Cases whose close stands 9–66 typical 4h moves above its 30-day average return +1.53 % over 18 bars (t 4.16, 734 cases), against a normal drift of 0.41 %. Cases 2.7–7.7 moves below it return −0.23 % (t −0.81).
- F4: The same pattern shows on two other measures of trend. Cases with a 30-day return above +23 % return +1.46 % (t 3.64, 596 cases). Cases within 4 typical moves of the 30-day high return +1.19 % (t 3.56, 734 cases). Cases after a 30-day loss of 4–17 % return −0.34 % (t −1.28), and those 18–52 moves below the high return +0.24 % (t 0.80).
- F5: The idea's unusual move is +0.05 % per case (strength 0.007, 4039 cases), 0.3 times the 0.19 % cost of a trade. In the uptrend groups of F3 and F4 the excess over drift is about 1.0–1.1 %, which is 5–6 times that cost.
- F1: The book's chained daily returns fell 53.3 % at their deepest, which is what fails Calmar (0.39 against 0.75), and the losses sit in long holdings. Trades held 3.8–6.5 days average −0.72 % net and trades held 6.7–43 days average −1.13 % net (1448 and 1434 trades). Trades held 0.5–3 days average +1.49 %. The 40 worst trades lose 39.3 % on average and last 13.7 days, against 4.2 days for all 7411 trades.
- F6: On the book's days in the deepest 10 % of its drawdown, the book loses 0.32 % a day against 0.25 % for holding the coins, so in its falls it does worse than simply holding. The book is invested on 80 % of days, with a mean allocation of 0.41 even in the lowest 30-day-return quintile.
