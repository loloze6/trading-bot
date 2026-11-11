---
backtest: 001-02_rsi-low-extreme-reversal-up_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.915 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.98 | above 0 | no |
| Mean daily return | -0.004665 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.106 | above 0 | no |
| Calmar | -0.8695 | above 0.75 | no |
| Trades per bar | 0.2191 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- The book: BTCUSD, ETHUSD, equal weight; 6 windows, 724 days (1.98 years); 7677 trades on 35038 bars
- Holding's Sharpe: 0.06572; yearly return: -0.8493; deepest fall: 0.9768; window whose removal lowers the Sharpe most: w6
Record: `steps_cards/04_backtest/hourly_run/backtests/001-02_rsi-low-extreme-reversal-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
