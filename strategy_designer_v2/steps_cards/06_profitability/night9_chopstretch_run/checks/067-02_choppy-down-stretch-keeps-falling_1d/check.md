---
backtest: 067-02_choppy-down-stretch-keeps-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3635 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9177 | above 0 | no |
| Mean daily return, on days in a position | -0.0006351 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5257 | above 0 | no |
| Calmar | -0.1271 | above 0.75 | no |
| Trades per day | 0.06825 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.913 % |
| Yearly return | -7.5 % (over 7.94 years) |
| Days in a position | 27 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02_choppy-down-stretch-keeps-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
