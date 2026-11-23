---
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8856 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2784 | above 0 | yes |
| Mean daily return, on days in a position | 0.001048 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7502 | above 0 | yes |
| Calmar | 0.6666 | above 0.75 | no |
| Trades per day | 0.5677 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.273 % |
| Yearly return | +20.4 % (over 7.94 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
