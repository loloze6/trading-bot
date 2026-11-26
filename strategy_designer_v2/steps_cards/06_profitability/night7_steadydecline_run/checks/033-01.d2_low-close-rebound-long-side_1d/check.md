---
backtest: 033-01.d2_low-close-rebound-long-side_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7698 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2156 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002251 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6273 | above 0 | yes |
| Calmar | 0.5889 | above 0.75 | no |
| Trades per day | 0.2429 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.349 % |
| Yearly return | +5.0 % (over 7.94 years) |
| Days in a position | 63 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01.d2_low-close-rebound-long-side_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
