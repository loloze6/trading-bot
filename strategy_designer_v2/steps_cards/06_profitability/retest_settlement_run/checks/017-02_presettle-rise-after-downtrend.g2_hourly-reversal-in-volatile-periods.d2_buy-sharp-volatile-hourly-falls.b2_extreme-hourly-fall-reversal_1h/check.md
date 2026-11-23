---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.665 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1112 | above 0 | yes |
| Mean daily return, on days in a position | 0.001144 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.518 | above 0 | yes |
| Calmar | 0.346 | above 0.75 | no |
| Trades per day | 0.7155 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.266 % |
| Yearly return | +24.2 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
