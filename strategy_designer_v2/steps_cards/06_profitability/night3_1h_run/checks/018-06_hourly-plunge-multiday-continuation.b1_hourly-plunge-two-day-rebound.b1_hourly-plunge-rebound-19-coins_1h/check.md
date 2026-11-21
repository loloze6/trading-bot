---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4952 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1121 | above 0 | no |
| Mean daily return | 0.0003314 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3592 | above 0 | yes |
| Calmar | 0.2419 | above 0.75 | no |
| Trades per day | 0.4522 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
