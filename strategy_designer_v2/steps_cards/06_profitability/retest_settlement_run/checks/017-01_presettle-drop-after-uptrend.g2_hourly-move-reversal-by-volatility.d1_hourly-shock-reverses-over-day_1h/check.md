---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1873 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3664 | above 0 | no |
| Mean daily return, on days in a position | 0.0003409 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.0823 | above 0 | yes |
| Calmar | -0.09903 | above 0.75 | no |
| Trades per day | 0.07321 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.477 % |
| Yearly return | -9.6 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
