---
backtest: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1935 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7477 | above 0 | no |
| Mean daily return, on days in a position | -0.0002904 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4385 | above 0 | no |
| Calmar | -0.1008 | above 0.75 | no |
| Trades per day | 0.1197 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.927 % |
| Yearly return | -4.8 % (over 7.94 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
