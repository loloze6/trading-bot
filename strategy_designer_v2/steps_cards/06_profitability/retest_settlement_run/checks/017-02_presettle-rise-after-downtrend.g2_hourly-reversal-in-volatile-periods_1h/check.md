---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -11.93 | above 0 | no |
| Sharpe minus holding's Sharpe | -12.48 | above 0 | no |
| Mean daily return, on days in a position | -0.01074 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -12.26 | above 0 | no |
| Calmar | -0.9807 | above 0.75 | no |
| Trades per day | 20.42 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.700 % |
| Yearly return | -98.1 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
