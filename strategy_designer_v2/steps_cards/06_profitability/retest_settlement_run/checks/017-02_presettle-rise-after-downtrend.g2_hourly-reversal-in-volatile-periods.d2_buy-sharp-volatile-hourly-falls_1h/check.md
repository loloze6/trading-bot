---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6299 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07613 | above 0 | yes |
| Mean daily return, on days in a position | 0.001053 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4911 | above 0 | yes |
| Calmar | 0.3274 | above 0.75 | no |
| Trades per day | 0.9199 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.165 % |
| Yearly return | +21.4 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
