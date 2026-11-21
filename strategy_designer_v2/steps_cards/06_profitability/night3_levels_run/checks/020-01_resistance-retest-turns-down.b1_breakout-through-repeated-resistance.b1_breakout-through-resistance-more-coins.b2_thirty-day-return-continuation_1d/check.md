---
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8607 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2532 | above 0 | yes |
| Mean daily return | 0.0008191 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7065 | above 0 | yes |
| Calmar | 0.7346 | above 0.75 | no |
| Trades per day | 0.2877 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
