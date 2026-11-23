---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2488 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.356 | above 0 | no |
| Mean daily return, on days in a position | 0.0001899 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.07579 | above 0 | yes |
| Calmar | 0.04353 | above 0.75 | no |
| Trades per day | 0.1582 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.358 % |
| Yearly return | +3.1 % (over 7.94 years) |
| Days in a position | 93 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
