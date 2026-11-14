---
backtest: 001-02_rsi-low-extreme-reversal-up_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.915 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.98 | above 0 | no |
| Mean daily return | -0.001597 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.106 | above 0 | no |
| Calmar | -0.6484 | above 0.75 | no |
| Trades per bar | 0.2191 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/001-02_rsi-low-extreme-reversal-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
