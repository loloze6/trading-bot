---
backtest: 064-01_falling-agitated-heavy-volume-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6618 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.528 | above 0 | no |
| Mean daily return, on days in a position | 0.005127 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0 | above 0 | no |
| Calmar | 7.211 | above 0.75 | yes |
| Trades per day | 0.0005476 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.016 % |
| Yearly return | +0.2 % (over 1.99 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Trades per day
Record: `steps_cards/04_backtest/night8_choppyagitated_run/unseen_2016_2017/backtests/064-01_falling-agitated-heavy-volume-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
