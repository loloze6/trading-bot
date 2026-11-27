---
backtest: 074-01.b1.d2_run-break-fade-steep-slide_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.0416 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.793 | above 0 | no |
| Mean daily return, on days in a position | -9.119e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8695 | above 0 | no |
| Calmar | -0.06319 | above 0.75 | no |
| Trades per day | 0.01847 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.155 % |
| Yearly return | -0.2 % (over 1.99 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d2_run-break-fade-steep-slide_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
