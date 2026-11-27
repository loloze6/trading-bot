---
backtest: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4029 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.4693 | above 0 | no |
| Mean daily return, on days in a position | -0.0003158 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8194 | above 0 | no |
| Calmar | -0.37 | above 0.75 | no |
| Trades per day | 0.07723 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.223 % |
| Yearly return | -1.8 % (over 0.87 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2026/backtests/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
