---
backtest: 074-01.b1.d2_run-break-fade-steep-slide_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1346 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.2326 | above 0 | no |
| Mean daily return, on days in a position | -0.0001477 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5086 | above 0 | no |
| Calmar | -0.1733 | above 0.75 | no |
| Trades per day | 0.05711 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.239 % |
| Yearly return | -0.7 % (over 0.87 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.d2_run-break-fade-steep-slide_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
