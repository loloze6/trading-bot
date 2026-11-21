---
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.b1_90-day-breakout-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.179 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5951 | above 0 | yes |
| Mean daily return | 0.0002131 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8885 | above 0 | yes |
| Calmar | 0.9558 | above 0.75 | yes |
| Trades per day | 0.02319 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.b1_90-day-breakout-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
