---
backtest: 035-02_break-swings-above-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.29 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.224 | above 0 | yes |
| Mean daily return, on days in a position | 0.003829 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3576 | above 0 | yes |
| Calmar | 3.814 | above 0.75 | yes |
| Trades per day | 0.04214 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.814 % |
| Yearly return | +20.8 % (over 0.87 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/035-02_break-swings-above-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
