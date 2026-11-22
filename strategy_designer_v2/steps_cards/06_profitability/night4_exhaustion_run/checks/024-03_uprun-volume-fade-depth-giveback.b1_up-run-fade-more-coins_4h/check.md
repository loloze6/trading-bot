---
backtest: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9103 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.517 | above 0 | no |
| Mean daily return | -0.002033 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.064 | above 0 | no |
| Calmar | -0.66 | above 0.75 | no |
| Trades per day | 0.1211 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
