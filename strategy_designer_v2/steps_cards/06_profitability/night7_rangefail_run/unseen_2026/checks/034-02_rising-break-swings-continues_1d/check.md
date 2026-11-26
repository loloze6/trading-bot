---
backtest: 034-02_rising-break-swings-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.514 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.447 | above 0 | yes |
| Mean daily return, on days in a position | 0.002038 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5303 | above 0 | yes |
| Calmar | 5.055 | above 0.75 | yes |
| Trades per day | 0.03312 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.404 % |
| Yearly return | +12.1 % (over 0.87 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-02_rising-break-swings-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
