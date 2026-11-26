---
backtest: 039-02_agitated-range-fall-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9254 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3558 | above 0 | yes |
| Mean daily return, on days in a position | 0.001528 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8202 | above 0 | yes |
| Calmar | 0.798 | above 0.75 | yes |
| Trades per day | 0.1767 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.077 % |
| Yearly return | +18.4 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/039-02_agitated-range-fall-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
