---
backtest: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2335 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1671 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009245 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.007572 | above 0 | yes |
| Calmar | 0.3142 | above 0.75 | no |
| Trades per day | 0.03591 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.492 % |
| Yearly return | +1.8 % (over 0.87 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
