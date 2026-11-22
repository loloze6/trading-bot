---
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.713 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1057 | above 0 | yes |
| Mean daily return | 0.001375 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5068 | above 0 | yes |
| Calmar | 0.3757 | above 0.75 | no |
| Trades per day | 0.04866 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
