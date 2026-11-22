---
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.01498 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5746 | above 0 | no |
| Mean daily return | 2.862e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.188 | above 0 | no |
| Calmar | -0.006526 | above 0.75 | no |
| Trades per day | 0.04375 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
