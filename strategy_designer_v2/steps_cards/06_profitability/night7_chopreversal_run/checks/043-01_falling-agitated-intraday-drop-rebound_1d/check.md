---
backtest: 043-01_falling-agitated-intraday-drop-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.104 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.534 | above 0 | yes |
| Mean daily return, on days in a position | 0.002708 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.888 | above 0 | yes |
| Calmar | 0.797 | above 0.75 | yes |
| Trades per day | 0.0733 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.660 % |
| Yearly return | +14.0 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/043-01_falling-agitated-intraday-drop-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
