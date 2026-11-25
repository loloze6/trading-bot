---
backtest: 037-02_falling-market-range-jump-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.283 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8372 | above 0 | no |
| Mean daily return, on days in a position | -0.001092 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.419 | above 0 | no |
| Calmar | -0.1105 | above 0.75 | no |
| Trades per day | 0.04702 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.881 % |
| Yearly return | -6.0 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/037-02_falling-market-range-jump-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
