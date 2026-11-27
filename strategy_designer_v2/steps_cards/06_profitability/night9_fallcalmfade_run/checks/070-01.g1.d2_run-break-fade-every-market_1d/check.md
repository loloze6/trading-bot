---
backtest: 070-01.g1.d2_run-break-fade-every-market_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5008 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05342 | above 0 | no |
| Mean daily return, on days in a position | 0.0005519 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3647 | above 0 | yes |
| Calmar | 0.2139 | above 0.75 | no |
| Trades per day | 0.1201 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.510 % |
| Yearly return | +4.5 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d2_run-break-fade-every-market_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
