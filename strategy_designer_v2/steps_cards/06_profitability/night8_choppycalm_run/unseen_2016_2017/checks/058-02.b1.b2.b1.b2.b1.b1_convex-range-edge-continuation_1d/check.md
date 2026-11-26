---
backtest: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.212 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02226 | above 0 | yes |
| Mean daily return, on days in a position | 0.009503 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.047 | above 0 | yes |
| Calmar | 6.486 | above 0.75 | yes |
| Trades per day | 0.05586 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.442 % |
| Yearly return | +133.2 % (over 1.99 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
