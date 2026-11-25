---
backtest: 047-01_falling-agitated-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5327 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03693 | above 0 | no |
| Mean daily return, on days in a position | 0.001 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3621 | above 0 | yes |
| Calmar | 0.2998 | above 0.75 | no |
| Trades per day | 0.08344 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.768 % |
| Yearly return | +7.0 % (over 7.94 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/047-01_falling-agitated-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
