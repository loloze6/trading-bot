---
backtest: 032-02_volatile-decline-low-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4581 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1115 | above 0 | no |
| Mean daily return, on days in a position | 0.0005981 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3074 | above 0 | yes |
| Calmar | 0.405 | above 0.75 | no |
| Trades per day | 0.003671 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.167 % |
| Yearly return | +1.4 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02_volatile-decline-low-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
