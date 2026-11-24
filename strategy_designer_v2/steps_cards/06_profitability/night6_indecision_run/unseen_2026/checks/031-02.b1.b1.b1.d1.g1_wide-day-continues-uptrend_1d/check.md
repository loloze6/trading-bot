---
backtest: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.321 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.254 | above 0 | yes |
| Mean daily return, on days in a position | 0.00222 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.6775 | above 0 | no |
| Calmar | 2.383 | above 0.75 | yes |
| Trades per day | 0.09001 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.834 % |
| Yearly return | +21.9 % (over 0.87 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
