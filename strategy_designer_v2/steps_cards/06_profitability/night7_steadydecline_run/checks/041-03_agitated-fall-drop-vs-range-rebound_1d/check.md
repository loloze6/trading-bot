---
backtest: 041-03_agitated-fall-drop-vs-range-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.124 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5543 | above 0 | yes |
| Mean daily return, on days in a position | 0.002539 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.924 | above 0 | yes |
| Calmar | 0.8091 | above 0.75 | yes |
| Trades per day | 0.07365 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.626 % |
| Yearly return | +13.6 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/041-03_agitated-fall-drop-vs-range-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
