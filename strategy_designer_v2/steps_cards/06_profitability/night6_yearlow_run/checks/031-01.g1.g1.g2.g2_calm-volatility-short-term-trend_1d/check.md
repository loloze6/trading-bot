---
backtest: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7862 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.232 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006651 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6645 | above 0 | yes |
| Calmar | 0.5187 | above 0.75 | no |
| Trades per day | 0.3008 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.030 % |
| Yearly return | +14.5 % (over 7.94 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
