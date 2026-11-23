---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8721 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.426 | above 0 | no |
| Mean daily return, on days in a position | -0.001333 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.006 | above 0 | no |
| Calmar | -0.3364 | above 0.75 | no |
| Trades per day | 0.6474 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.958 % |
| Yearly return | -33.0 % (over 7.94 years) |
| Days in a position | 67 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
