---
backtest: 074-01_falling-market-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6855 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1313 | above 0 | yes |
| Mean daily return, on days in a position | 0.00137 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5111 | above 0 | yes |
| Calmar | 0.3691 | above 0.75 | no |
| Trades per day | 0.04685 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.362 % |
| Yearly return | +4.6 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01_falling-market-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
