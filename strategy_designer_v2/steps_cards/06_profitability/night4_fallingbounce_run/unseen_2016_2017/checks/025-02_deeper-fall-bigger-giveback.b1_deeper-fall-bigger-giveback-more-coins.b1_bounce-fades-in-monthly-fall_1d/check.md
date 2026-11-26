---
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6915 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.473 | above 0 | no |
| Mean daily return, on days in a position | -0.01667 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7832 | above 0 | no |
| Calmar | -0.4906 | above 0.75 | no |
| Trades per day | 0.00107 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.099 % |
| Yearly return | -1.3 % (over 1.99 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
