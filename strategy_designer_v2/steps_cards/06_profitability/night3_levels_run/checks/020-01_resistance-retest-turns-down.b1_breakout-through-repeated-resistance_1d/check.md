---
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7649 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2107 | above 0 | yes |
| Mean daily return | 0.0006015 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5771 | above 0 | yes |
| Calmar | 0.5333 | above 0.75 | no |
| Trades per day | 0.1012 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
