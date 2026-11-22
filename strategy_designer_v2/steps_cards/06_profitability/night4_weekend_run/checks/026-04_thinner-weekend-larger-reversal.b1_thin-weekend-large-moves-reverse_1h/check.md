---
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1844 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7382 | above 0 | no |
| Mean daily return | -8.718e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3087 | above 0 | no |
| Calmar | -0.0803 | above 0.75 | no |
| Trades per day | 0.1862 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
