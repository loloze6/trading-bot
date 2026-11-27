---
backtest: 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1424 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.609 | above 0 | no |
| Mean daily return, on days in a position | 0.0003666 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5078 | above 0 | no |
| Calmar | 0.1592 | above 0.75 | no |
| Trades per day | 0.01744 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.163 % |
| Yearly return | +0.4 % (over 1.99 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
