---
backtest: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8347 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2651 | above 0 | yes |
| Mean daily return, on days in a position | 0.002818 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6914 | above 0 | yes |
| Calmar | 0.9032 | above 0.75 | yes |
| Trades per day | 0.02057 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.263 % |
| Yearly return | +4.2 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
