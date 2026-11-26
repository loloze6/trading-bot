---
backtest: 031-01.b1.b1_wide-day-extends-run-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.064 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9976 | above 0 | yes |
| Mean daily return, on days in a position | 0.001174 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.6879 | above 0 | no |
| Calmar | 1.494 | above 0.75 | yes |
| Trades per day | 0.3366 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.443 % |
| Yearly return | +29.3 % (over 0.87 years) |
| Days in a position | 68 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b1_wide-day-extends-run-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
