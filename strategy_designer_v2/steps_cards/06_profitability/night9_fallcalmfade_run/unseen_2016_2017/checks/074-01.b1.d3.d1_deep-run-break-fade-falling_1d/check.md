---
backtest: 074-01.b1.d3.d1_deep-run-break-fade-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1304 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.621 | above 0 | no |
| Mean daily return, on days in a position | 0.0004221 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5739 | above 0 | no |
| Calmar | 0.1191 | above 0.75 | no |
| Trades per day | 0.009576 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.118 % |
| Yearly return | +0.3 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d3.d1_deep-run-break-fade-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
