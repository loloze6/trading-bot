---
backtest: 058-01_choppy-agitated-weekly-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5383 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03129 | above 0 | no |
| Mean daily return, on days in a position | 0.001088 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.307 | above 0 | yes |
| Calmar | 0.4194 | above 0.75 | no |
| Trades per day | 0.02389 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.332 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/058-01_choppy-agitated-weekly-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
