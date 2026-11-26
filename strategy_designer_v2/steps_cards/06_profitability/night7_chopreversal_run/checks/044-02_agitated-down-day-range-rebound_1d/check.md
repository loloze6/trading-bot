---
backtest: 044-02_agitated-down-day-range-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.111 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5415 | above 0 | yes |
| Mean daily return, on days in a position | 0.001347 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.014 | above 0 | yes |
| Calmar | 1.176 | above 0.75 | yes |
| Trades per day | 0.1776 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.794 % |
| Yearly return | +17.0 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/044-02_agitated-down-day-range-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
