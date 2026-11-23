---
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.312 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.865 | above 0 | no |
| Mean daily return, on days in a position | -0.0006766 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.545 | above 0 | no |
| Calmar | -0.2301 | above 0.75 | no |
| Trades per day | 1.514 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.457 % |
| Yearly return | -18.6 % (over 7.94 years) |
| Days in a position | 82 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
