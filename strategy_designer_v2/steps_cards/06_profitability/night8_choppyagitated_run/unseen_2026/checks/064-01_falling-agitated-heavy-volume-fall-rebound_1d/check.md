---
backtest: 064-01_falling-agitated-heavy-volume-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.182 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1156 | above 0 | yes |
| Mean daily return, on days in a position | 0.00121 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.08756 | above 0 | yes |
| Calmar | 0.224 | above 0.75 | no |
| Trades per day | 0.01935 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.466 % |
| Yearly return | +1.2 % (over 0.87 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/unseen_2026/backtests/064-01_falling-agitated-heavy-volume-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
