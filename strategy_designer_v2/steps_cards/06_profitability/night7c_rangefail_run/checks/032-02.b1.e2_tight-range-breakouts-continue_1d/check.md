---
backtest: 032-02.b1.e2_tight-range-breakouts-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8568 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3026 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008604 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6546 | above 0 | yes |
| Calmar | 0.6356 | above 0.75 | no |
| Trades per day | 0.01484 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.354 % |
| Yearly return | +5.7 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e2_tight-range-breakouts-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
