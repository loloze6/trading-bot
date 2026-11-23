---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6629 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1091 | above 0 | yes |
| Mean daily return, on days in a position | 0.001298 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5151 | above 0 | yes |
| Calmar | 0.374 | above 0.75 | no |
| Trades per day | 0.5559 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.700 % |
| Yearly return | +22.8 % (over 7.94 years) |
| Days in a position | 72 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
