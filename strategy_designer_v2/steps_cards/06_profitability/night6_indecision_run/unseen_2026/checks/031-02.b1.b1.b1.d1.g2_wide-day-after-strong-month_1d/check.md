---
backtest: 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.415 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.348 | above 0 | yes |
| Mean daily return, on days in a position | 0.002588 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.09019 | above 0 | no |
| Calmar | 2.509 | above 0.75 | yes |
| Trades per day | 0.07821 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.878 % |
| Yearly return | +25.1 % (over 0.87 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
