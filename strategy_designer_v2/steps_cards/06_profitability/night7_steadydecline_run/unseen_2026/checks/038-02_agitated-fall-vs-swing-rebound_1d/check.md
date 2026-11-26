---
backtest: 038-02_agitated-fall-vs-swing-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.05978 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.1578 | above 0 | no |
| Mean daily return, on days in a position | -0.0001598 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.288 | above 0 | no |
| Calmar | -0.2038 | above 0.75 | no |
| Trades per day | 0.08671 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.963 % |
| Yearly return | -2.7 % (over 0.87 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2026/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
