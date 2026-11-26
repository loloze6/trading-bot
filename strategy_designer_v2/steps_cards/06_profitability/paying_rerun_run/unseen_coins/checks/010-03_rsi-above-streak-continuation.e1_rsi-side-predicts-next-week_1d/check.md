---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, LTC, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI, XMR, XRP, ZEC as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, LTCUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6105 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03839 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006014 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4248 | above 0 | yes |
| Calmar | 0.4649 | above 0.75 | no |
| Trades per day | 0.4144 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.880 % |
| Yearly return | +16.8 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/paying_rerun_run/unseen_coins/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
