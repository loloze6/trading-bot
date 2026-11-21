---
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2758 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3351 | above 0 | no |
| Mean daily return | 0.0002856 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.04645 | above 0 | yes |
| Calmar | 0.04239 | above 0.75 | no |
| Trades per day | 0.1708 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
