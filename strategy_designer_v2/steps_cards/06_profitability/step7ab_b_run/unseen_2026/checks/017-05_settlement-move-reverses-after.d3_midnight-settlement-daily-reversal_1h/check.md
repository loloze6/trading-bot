---
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.456 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.555 | above 0 | no |
| Mean daily return, on days in a position | -0.001029 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.844 | above 0 | no |
| Calmar | -0.9918 | above 0.75 | no |
| Trades per day | 1.682 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.348 % |
| Yearly return | -33.5 % (over 0.87 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2026/backtests/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
