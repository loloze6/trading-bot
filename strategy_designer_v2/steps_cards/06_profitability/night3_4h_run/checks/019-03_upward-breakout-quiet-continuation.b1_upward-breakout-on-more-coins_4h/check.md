---
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9153 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3081 | above 0 | yes |
| Mean daily return | 0.001003 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7046 | above 0 | yes |
| Calmar | 0.8579 | above 0.75 | yes |
| Trades per day | 0.2815 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
