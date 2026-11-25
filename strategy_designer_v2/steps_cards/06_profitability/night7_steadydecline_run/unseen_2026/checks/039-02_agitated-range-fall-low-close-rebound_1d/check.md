---
backtest: 039-02_agitated-range-fall-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.01297 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.111 | above 0 | no |
| Mean daily return, on days in a position | -2.273e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.619 | above 0 | no |
| Calmar | -0.1477 | above 0.75 | no |
| Trades per day | 0.1698 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.132 % |
| Yearly return | -2.5 % (over 0.87 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2026/backtests/039-02_agitated-range-fall-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
