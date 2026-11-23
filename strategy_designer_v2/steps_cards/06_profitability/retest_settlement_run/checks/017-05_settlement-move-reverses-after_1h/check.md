---
backtest: 017-05_settlement-move-reverses-after_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -3.966 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.52 | above 0 | no |
| Mean daily return, on days in a position | -0.002 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -4.144 | above 0 | no |
| Calmar | -0.5203 | above 0.75 | no |
| Trades per day | 3.734 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.943 % |
| Yearly return | -51.9 % (over 7.94 years) |
| Days in a position | 98 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
