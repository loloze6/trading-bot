---
backtest: 059-02_calm-below-high-keeps-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2194 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.789 | above 0 | no |
| Mean daily return, on days in a position | -0.000332 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4099 | above 0 | no |
| Calmar | -0.1361 | above 0.75 | no |
| Trades per day | 0.2384 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.559 % |
| Yearly return | -10.4 % (over 7.94 years) |
| Days in a position | 54 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-02_calm-below-high-keeps-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
