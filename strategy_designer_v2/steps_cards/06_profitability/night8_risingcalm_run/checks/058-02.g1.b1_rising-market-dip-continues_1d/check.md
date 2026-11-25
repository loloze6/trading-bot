---
backtest: 058-02.g1.b1_rising-market-dip-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7383 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.292 | above 0 | no |
| Mean daily return, on days in a position | -0.001478 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8858 | above 0 | no |
| Calmar | -0.2541 | above 0.75 | no |
| Trades per day | 0.186 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.540 % |
| Yearly return | -22.9 % (over 7.94 years) |
| Days in a position | 40 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.g1.b1_rising-market-dip-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
