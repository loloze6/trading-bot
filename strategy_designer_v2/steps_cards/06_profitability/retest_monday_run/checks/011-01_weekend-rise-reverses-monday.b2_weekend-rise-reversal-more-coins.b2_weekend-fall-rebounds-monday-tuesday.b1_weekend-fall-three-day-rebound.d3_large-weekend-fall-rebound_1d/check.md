---
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5558 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05166 | above 0 | no |
| Mean daily return, on days in a position | 0.001018 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4012 | above 0 | yes |
| Calmar | 0.2057 | above 0.75 | no |
| Trades per day | 0.06461 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.907 % |
| Yearly return | +8.4 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
