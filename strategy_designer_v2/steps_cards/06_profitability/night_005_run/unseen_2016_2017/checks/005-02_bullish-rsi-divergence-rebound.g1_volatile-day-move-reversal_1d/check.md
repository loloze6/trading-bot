---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.099 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.814 | above 0 | no |
| Mean daily return, on days in a position | -0.001748 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.456 | above 0 | no |
| Calmar | -0.5772 | above 0.75 | no |
| Trades per day | 0.4227 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.091 % |
| Yearly return | -40.6 % (over 1.99 years) |
| Days in a position | 69 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_005_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
