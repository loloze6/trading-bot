---
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3514 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2558 | above 0 | no |
| Mean daily return, on days in a position | 0.000347 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1967 | above 0 | yes |
| Calmar | 0.1186 | above 0.75 | no |
| Trades per day | 0.7347 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.468 % |
| Yearly return | +6.0 % (over 7.94 years) |
| Days in a position | 78 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
