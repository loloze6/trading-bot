---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.59 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.144 | above 0 | no |
| Mean daily return | -0.0005131 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7275 | above 0 | no |
| Calmar | -0.238 | above 0.75 | no |
| Trades per bar | 0.2322 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
