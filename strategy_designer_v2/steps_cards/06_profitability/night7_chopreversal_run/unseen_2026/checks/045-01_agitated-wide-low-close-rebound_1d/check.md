---
backtest: 045-01_agitated-wide-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.101 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.1991 | above 0 | no |
| Mean daily return, on days in a position | -0.000151 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4418 | above 0 | no |
| Calmar | -0.2448 | above 0.75 | no |
| Trades per day | 0.2876 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.235 % |
| Yearly return | -5.0 % (over 0.87 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/045-01_agitated-wide-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
