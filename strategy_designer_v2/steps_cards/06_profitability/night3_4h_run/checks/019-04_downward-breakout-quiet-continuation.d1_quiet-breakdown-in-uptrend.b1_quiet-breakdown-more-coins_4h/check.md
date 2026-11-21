---
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3897 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9969 | above 0 | no |
| Mean daily return | -4.728e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5254 | above 0 | no |
| Calmar | -0.08681 | above 0.75 | no |
| Trades per day | 0.04708 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
