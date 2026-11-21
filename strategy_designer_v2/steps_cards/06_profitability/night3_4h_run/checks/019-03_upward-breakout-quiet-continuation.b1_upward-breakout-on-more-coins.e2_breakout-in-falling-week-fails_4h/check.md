---
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1518 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4554 | above 0 | no |
| Mean daily return | 3.689e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.02354 | above 0 | no |
| Calmar | 0.04627 | above 0.75 | no |
| Trades per day | 0.08812 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
