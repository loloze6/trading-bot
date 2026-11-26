---
backtest: 058-01.g2.g1_agitated-decline-upper-wick-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4723 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.09735 | above 0 | no |
| Mean daily return, on days in a position | 0.0005676 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2547 | above 0 | yes |
| Calmar | 0.2431 | above 0.75 | no |
| Trades per day | 0.05005 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.219 % |
| Yearly return | +1.9 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1_agitated-decline-upper-wick-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
