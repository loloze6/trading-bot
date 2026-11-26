---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6842 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5862 | above 0 | yes |
| Mean daily return, on days in a position | 0.00101 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2003 | above 0 | yes |
| Calmar | 0.4325 | above 0.75 | no |
| Trades per day | 0.06282 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.821 % |
| Yearly return | +24.7 % (over 0.87 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/unseen_2026/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
