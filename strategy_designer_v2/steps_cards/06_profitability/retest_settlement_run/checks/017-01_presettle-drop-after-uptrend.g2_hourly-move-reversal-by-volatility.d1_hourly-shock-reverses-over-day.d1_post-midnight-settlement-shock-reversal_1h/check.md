---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7642 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2104 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007182 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6362 | above 0 | yes |
| Calmar | 0.4722 | above 0.75 | no |
| Trades per day | 1.65 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.761 % |
| Yearly return | +22.2 % (over 7.94 years) |
| Days in a position | 98 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
