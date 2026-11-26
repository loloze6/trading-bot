---
backtest: 031-02.b1_failed-rally-near-yearly-low_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8794 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2977 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003741 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6325 | above 0 | yes |
| Calmar | 0.5778 | above 0.75 | no |
| Trades per day | 0.01778 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.491 % |
| Yearly return | +8.1 % (over 7.94 years) |
| Days in a position | 60 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1_failed-rally-near-yearly-low_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
