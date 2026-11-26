---
backtest: 066-02_falling-agitated-year-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8137 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.376 | above 0 | no |
| Mean daily return, on days in a position | 0.001461 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1067 | above 0 | yes |
| Calmar | 1.349 | above 0.75 | yes |
| Trades per day | 0.004929 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.032 % |
| Yearly return | +0.5 % (over 1.99 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Trades per day
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/066-02_falling-agitated-year-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
