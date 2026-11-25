---
backtest: 033-01_close-near-low-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1976 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3566 | above 0 | no |
| Mean daily return, on days in a position | 4.684e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.05482 | above 0 | yes |
| Calmar | 0.07773 | above 0.75 | no |
| Trades per day | 0.6547 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.451 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01_close-near-low-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
