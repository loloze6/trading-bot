---
backtest: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.021 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4667 | above 0 | yes |
| Mean daily return, on days in a position | 0.003322 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8479 | above 0 | yes |
| Calmar | 1.186 | above 0.75 | yes |
| Trades per day | 0.03076 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.387 % |
| Yearly return | +7.6 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
