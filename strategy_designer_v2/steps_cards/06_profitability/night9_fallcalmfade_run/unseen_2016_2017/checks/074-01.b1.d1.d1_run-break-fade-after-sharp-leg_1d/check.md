---
backtest: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4738 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.277 | above 0 | no |
| Mean daily return, on days in a position | 0.001548 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1775 | above 0 | no |
| Calmar | 0.742 | above 0.75 | no |
| Trades per day | 0.01026 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.128 % |
| Yearly return | +1.1 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
