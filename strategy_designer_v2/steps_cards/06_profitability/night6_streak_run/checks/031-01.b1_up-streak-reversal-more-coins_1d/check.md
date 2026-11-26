---
backtest: 031-01.b1_up-streak-reversal-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7645 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.345 | above 0 | no |
| Mean daily return, on days in a position | -0.001114 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9235 | above 0 | no |
| Calmar | -0.4121 | above 0.75 | no |
| Trades per day | 0.2471 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.690 % |
| Yearly return | -40.9 % (over 7.94 years) |
| Days in a position | 97 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b1_up-streak-reversal-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
