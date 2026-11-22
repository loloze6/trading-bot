---
backtest: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3337 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2735 | above 0 | no |
| Mean daily return | 0.0004692 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.228 | above 0 | yes |
| Calmar | 0.0588 | above 0.75 | no |
| Trades per day | 0.07175 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
