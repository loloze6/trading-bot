---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.661 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.215 | above 0 | no |
| Mean daily return, on days in a position | -0.002118 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.855 | above 0 | no |
| Calmar | -0.5581 | above 0.75 | no |
| Trades per day | 11.87 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.517 % |
| Yearly return | -55.7 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
