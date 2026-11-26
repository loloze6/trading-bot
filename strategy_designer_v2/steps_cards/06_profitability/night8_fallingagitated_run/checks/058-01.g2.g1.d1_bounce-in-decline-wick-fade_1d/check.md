---
backtest: 058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6727 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1031 | above 0 | yes |
| Mean daily return, on days in a position | 0.001426 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4877 | above 0 | yes |
| Calmar | 0.6193 | above 0.75 | no |
| Trades per day | 0.02051 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.162 % |
| Yearly return | +2.1 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
