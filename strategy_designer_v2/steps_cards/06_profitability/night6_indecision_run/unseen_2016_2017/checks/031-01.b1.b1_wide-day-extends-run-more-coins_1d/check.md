---
backtest: 031-01.b1.b1_wide-day-extends-run-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.086 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6647 | above 0 | no |
| Mean daily return, on days in a position | 0.003595 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.636 | above 0 | yes |
| Calmar | 6.94 | above 0.75 | yes |
| Trades per day | 0.4036 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.789 % |
| Yearly return | +170.9 % (over 1.99 years) |
| Days in a position | 80 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.b1.b1_wide-day-extends-run-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
