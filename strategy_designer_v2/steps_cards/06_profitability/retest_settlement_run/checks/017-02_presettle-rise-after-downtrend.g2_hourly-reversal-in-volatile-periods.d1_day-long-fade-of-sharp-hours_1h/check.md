---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1067 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4471 | above 0 | no |
| Mean daily return, on days in a position | 0.000186 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.001982 | above 0 | no |
| Calmar | -0.1361 | above 0.75 | no |
| Trades per day | 0.1423 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.330 % |
| Yearly return | -13.0 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
