---
backtest: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.982 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.8 | above 0 | no |
| Mean daily return, on days in a position | 0.002502 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.457 | above 0 | yes |
| Calmar | 3.048 | above 0.75 | yes |
| Trades per day | 0.1944 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.207 % |
| Yearly return | +53.8 % (over 1.99 years) |
| Days in a position | 50 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
