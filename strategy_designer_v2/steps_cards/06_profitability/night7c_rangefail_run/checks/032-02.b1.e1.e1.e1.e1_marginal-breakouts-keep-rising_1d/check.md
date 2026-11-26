---
backtest: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8524 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2982 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005534 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6833 | above 0 | yes |
| Calmar | 0.6417 | above 0.75 | no |
| Trades per day | 0.01484 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.469 % |
| Yearly return | +7.5 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
