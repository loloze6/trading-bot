---
backtest: 044-01_agitated-wide-range-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1572 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.0592 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002758 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5082 | above 0 | no |
| Calmar | 0.06502 | above 0.75 | no |
| Trades per day | 0.161 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.121 % |
| Yearly return | +1.1 % (over 0.87 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/044-01_agitated-wide-range-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
