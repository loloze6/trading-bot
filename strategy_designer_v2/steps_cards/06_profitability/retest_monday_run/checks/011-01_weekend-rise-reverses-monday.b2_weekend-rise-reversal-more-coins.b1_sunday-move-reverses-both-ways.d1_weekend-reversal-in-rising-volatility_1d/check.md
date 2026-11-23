---
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9858 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3783 | above 0 | yes |
| Mean daily return, on days in a position | 0.001393 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9165 | above 0 | yes |
| Calmar | 0.7528 | above 0.75 | yes |
| Trades per day | 0.07556 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.617 % |
| Yearly return | +11.6 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
