---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7689 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.1471 | above 0 | no |
| Mean daily return, on days in a position | -0.001538 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9668 | above 0 | no |
| Calmar | -0.9233 | above 0.75 | no |
| Trades per day | 0.31 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.101 % |
| Yearly return | -32.6 % (over 0.87 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_005_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
