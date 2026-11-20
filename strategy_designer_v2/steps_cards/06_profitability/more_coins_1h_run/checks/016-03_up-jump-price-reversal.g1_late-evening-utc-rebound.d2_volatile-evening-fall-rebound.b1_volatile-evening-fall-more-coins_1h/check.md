---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9213 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.314 | above 0 | yes |
| Mean daily return | 0.0004852 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8321 | above 0 | yes |
| Calmar | 0.4862 | above 0.75 | no |
| Trades per day | 0.3349 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/more_coins_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
