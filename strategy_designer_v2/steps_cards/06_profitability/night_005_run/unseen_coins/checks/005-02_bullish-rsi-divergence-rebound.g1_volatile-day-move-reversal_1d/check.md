---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, LTC, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI, XMR, XRP, ZEC as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, LTCUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5358 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.009731 | above 0 | no |
| Mean daily return, on days in a position | 0.0007599 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3683 | above 0 | yes |
| Calmar | 0.1932 | above 0.75 | no |
| Trades per day | 0.3904 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.311 % |
| Yearly return | +10.8 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night_005_run/unseen_coins/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
