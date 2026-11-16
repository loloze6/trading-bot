---
backtest: 002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5589 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.006145 | above 0 | yes |
| Mean daily return | 0.0004007 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2613 | above 0 | yes |
| Calmar | 0.2326 | above 0.75 | no |
| Trades per bar | 0.03105 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
