---
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7773 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1699 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009303 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6333 | above 0 | yes |
| Calmar | 0.3691 | above 0.75 | no |
| Trades per day | 0.1983 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.252 % |
| Yearly return | +17.0 % (over 7.94 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
