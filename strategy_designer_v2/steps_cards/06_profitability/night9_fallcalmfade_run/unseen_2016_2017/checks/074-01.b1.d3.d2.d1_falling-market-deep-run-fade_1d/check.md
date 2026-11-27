---
backtest: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08654 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.838 | above 0 | no |
| Mean daily return, on days in a position | -0.0001668 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7721 | above 0 | no |
| Calmar | -0.08329 | above 0.75 | no |
| Trades per day | 0.0171 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.126 % |
| Yearly return | -0.2 % (over 1.99 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
