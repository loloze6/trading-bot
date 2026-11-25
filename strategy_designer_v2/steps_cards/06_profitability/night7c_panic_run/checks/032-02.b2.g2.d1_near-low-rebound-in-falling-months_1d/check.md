---
backtest: 032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5492 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.004965 | above 0 | no |
| Mean daily return, on days in a position | 0.0009999 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4939 | above 0 | yes |
| Calmar | 0.3447 | above 0.75 | no |
| Trades per day | 0.132 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.762 % |
| Yearly return | +7.2 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
