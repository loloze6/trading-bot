---
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9024 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3183 | above 0 | yes |
| Mean daily return | 0.0004281 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7467 | above 0 | yes |
| Calmar | 0.748 | above 0.75 | no |
| Trades per day | 0.01388 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
