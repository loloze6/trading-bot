---
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9235 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.531 | above 0 | no |
| Mean daily return, on days in a position | -0.0005123 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.237 | above 0 | no |
| Calmar | -0.2092 | above 0.75 | no |
| Trades per day | 1.83 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.910 % |
| Yearly return | -16.1 % (over 7.94 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
