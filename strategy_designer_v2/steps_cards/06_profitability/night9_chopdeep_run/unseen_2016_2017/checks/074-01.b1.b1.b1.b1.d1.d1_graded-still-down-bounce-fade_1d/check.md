---
backtest: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2985 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.05 | above 0 | no |
| Mean daily return, on days in a position | -0.0005632 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9311 | above 0 | no |
| Calmar | -0.2112 | above 0.75 | no |
| Trades per day | 0.02326 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.165 % |
| Yearly return | -1.0 % (over 1.99 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
