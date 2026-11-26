---
backtest: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.289 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.901 | above 0 | no |
| Mean daily return, on days in a position | 0.00243 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8534 | above 0 | yes |
| Calmar | 1.661 | above 0.75 | yes |
| Trades per day | 0.2103 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.241 % |
| Yearly return | +32.0 % (over 1.99 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
