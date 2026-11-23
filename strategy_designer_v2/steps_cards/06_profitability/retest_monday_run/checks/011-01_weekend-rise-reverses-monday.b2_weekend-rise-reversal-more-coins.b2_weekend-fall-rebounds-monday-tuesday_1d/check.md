---
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4685 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.139 | above 0 | no |
| Mean daily return, on days in a position | 0.0006792 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3614 | above 0 | yes |
| Calmar | 0.2839 | above 0.75 | no |
| Trades per day | 0.08976 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.703 % |
| Yearly return | +5.5 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
