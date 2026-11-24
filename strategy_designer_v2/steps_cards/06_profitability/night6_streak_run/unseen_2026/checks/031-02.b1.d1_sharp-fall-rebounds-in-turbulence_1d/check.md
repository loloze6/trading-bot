---
backtest: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.09 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.188 | above 0 | no |
| Mean daily return, on days in a position | -0.002146 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.336 | above 0 | no |
| Calmar | -1.013 | above 0.75 | no |
| Trades per day | 0.1719 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.476 % |
| Yearly return | -29.4 % (over 0.87 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
