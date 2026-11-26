---
backtest: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7656 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.196 | above 0 | yes |
| Mean daily return, on days in a position | 0.001156 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5358 | above 0 | yes |
| Calmar | 0.6245 | above 0.75 | no |
| Trades per day | 0.03036 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.176 % |
| Yearly return | +2.5 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
