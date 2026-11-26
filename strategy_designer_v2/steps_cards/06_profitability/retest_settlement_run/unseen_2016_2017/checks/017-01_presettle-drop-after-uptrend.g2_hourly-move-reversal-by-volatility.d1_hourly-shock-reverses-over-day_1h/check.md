---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.963 | above 0 | no |
| Sharpe minus holding's Sharpe | -5.198 | above 0 | no |
| Mean daily return, on days in a position | -0.004172 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.66 | above 0 | no |
| Calmar | -0.8561 | above 0.75 | no |
| Trades per day | 0.169 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 4.061 % |
| Yearly return | -84.2 % (over 1.99 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/unseen_2016_2017/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
