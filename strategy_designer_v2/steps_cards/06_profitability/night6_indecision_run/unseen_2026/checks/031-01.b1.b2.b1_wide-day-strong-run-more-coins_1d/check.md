---
backtest: 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.126 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.06 | above 0 | yes |
| Mean daily return, on days in a position | 0.001385 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.3325 | above 0 | no |
| Calmar | 1.666 | above 0.75 | yes |
| Trades per day | 0.2618 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.542 % |
| Yearly return | +33.6 % (over 0.87 years) |
| Days in a position | 66 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
