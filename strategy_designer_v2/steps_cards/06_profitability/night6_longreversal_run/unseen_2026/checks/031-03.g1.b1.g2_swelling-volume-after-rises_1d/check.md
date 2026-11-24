---
backtest: 031-03.g1.b1.g2_swelling-volume-after-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.271 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2046 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002716 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1681 | above 0 | no |
| Calmar | 0.2444 | above 0.75 | no |
| Trades per day | 0.08313 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.174 % |
| Yearly return | +3.6 % (over 0.87 years) |
| Days in a position | 61 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2026/backtests/031-03.g1.b1.g2_swelling-volume-after-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
