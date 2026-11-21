---
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2972 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9045 | above 0 | no |
| Mean daily return | -0.0001432 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6034 | above 0 | no |
| Calmar | -0.1296 | above 0.75 | no |
| Trades per day | 0.07242 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
