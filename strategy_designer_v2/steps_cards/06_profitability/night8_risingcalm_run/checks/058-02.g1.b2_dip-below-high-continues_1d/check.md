---
backtest: 058-02.g1.b2_dip-below-high-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6704 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.225 | above 0 | no |
| Mean daily return, on days in a position | -0.0009309 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7904 | above 0 | no |
| Calmar | -0.3576 | above 0.75 | no |
| Trades per day | 0.487 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.499 % |
| Yearly return | -35.1 % (over 7.94 years) |
| Days in a position | 94 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.g1.b2_dip-below-high-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
