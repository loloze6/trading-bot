---
backtest: 067-01_choppy-up-stretch-keeps-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.05696 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4972 | above 0 | no |
| Mean daily return, on days in a position | 8.131e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.09695 | above 0 | no |
| Calmar | -0.0211 | above 0.75 | no |
| Trades per day | 0.1061 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.187 % |
| Yearly return | -1.3 % (over 7.94 years) |
| Days in a position | 44 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01_choppy-up-stretch-keeps-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
