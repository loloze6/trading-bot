---
backtest: 058-01.b2_quiet-volume-calm-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2299 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3274 | above 0 | no |
| Mean daily return, on days in a position | 0.0005463 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.0405 | above 0 | yes |
| Calmar | 0.08521 | above 0.75 | no |
| Trades per day | 0.0322 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.704 % |
| Yearly return | +2.2 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b2_quiet-volume-calm-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
