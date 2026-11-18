---
backtest: 005-02_bullish-rsi-divergence-rebound_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.04352 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6831 | above 0 | no |
| Mean daily return | -3.402e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2283 | above 0 | no |
| Calmar | -0.02749 | above 0.75 | no |
| Trades per bar | 0.01096 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
