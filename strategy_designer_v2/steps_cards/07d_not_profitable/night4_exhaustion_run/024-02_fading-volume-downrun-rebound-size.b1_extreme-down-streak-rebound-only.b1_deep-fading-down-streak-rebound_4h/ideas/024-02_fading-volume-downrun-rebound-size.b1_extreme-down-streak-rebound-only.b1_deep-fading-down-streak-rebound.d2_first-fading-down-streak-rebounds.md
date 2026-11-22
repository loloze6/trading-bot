---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, the more so the fewer such fading-volume down-streaks the coin has had over the past 7 days, and the larger the streak's loss relative to its typical four-hour move over the past 30 days.
Consequence: A trader buys the first fading-volume down-streak after a quiet week and refuses the ones that repeat during a grinding decline, which are the ones that become long, losing holdings.
Why:
- F2: Cases that follow several earlier signal bars lose the rebound. With 5–13 active bars in the previous 7 days, the 18-bar return is −0.11 % (t −0.35, 803 cases); with 0–2 active bars it is +1.05 % (t 3.61, 803 cases). The count of active bars in the past 3 days also ranks returns down (Spearman −0.045 over 3 days, −0.065 over 7 days, against +0.060 for the forecast itself). The worst 3-day quintile returns −0.41 % (t −1.37).
- F1: The book's chained daily returns fell 53.3 % at their deepest, which is what fails Calmar (0.39 against 0.75), and the losses sit in long holdings. Trades held 3.8–6.5 days average −0.72 % net and trades held 6.7–43 days average −1.13 % net (1448 and 1434 trades). Trades held 0.5–3 days average +1.49 %. The 40 worst trades lose 39.3 % on average and last 13.7 days, against 4.2 days for all 7411 trades.
- F6: On the book's days in the deepest 10 % of its drawdown, the book loses 0.32 % a day against 0.25 % for holding the coins, so in its falls it does worse than simply holding. The book is invested on 80 % of days, with a mean allocation of 0.41 even in the lowest 30-day-return quintile.
