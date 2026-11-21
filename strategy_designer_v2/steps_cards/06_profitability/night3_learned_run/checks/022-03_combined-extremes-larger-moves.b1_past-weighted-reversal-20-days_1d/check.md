---
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4348 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9676 | above 0 | no |
| Mean daily return | -0.0007817 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5316 | above 0 | no |
| Calmar | -0.9724 | above 0.75 | no |
| Trades per day | 0.06069 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
