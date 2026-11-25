---
backtest: 039-02.d1_wide-range-low-close-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.976 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4064 | above 0 | yes |
| Mean daily return, on days in a position | 0.001101 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8441 | above 0 | yes |
| Calmar | 1.158 | above 0.75 | yes |
| Trades per day | 0.2988 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.197 % |
| Yearly return | +21.8 % (over 7.94 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
