---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3787 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9325 | above 0 | no |
| Mean daily return, on days in a position | -0.0003171 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5514 | above 0 | no |
| Calmar | -0.1687 | above 0.75 | no |
| Trades per day | 0.8171 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.480 % |
| Yearly return | -13.6 % (over 7.94 years) |
| Days in a position | 93 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
