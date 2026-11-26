---
backtest: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.869 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.882 | above 0 | no |
| Mean daily return, on days in a position | 0.006514 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.572 | above 0 | yes |
| Calmar | 2.635 | above 0.75 | yes |
| Trades per day | 0.02941 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.754 % |
| Yearly return | +29.5 % (over 1.99 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
