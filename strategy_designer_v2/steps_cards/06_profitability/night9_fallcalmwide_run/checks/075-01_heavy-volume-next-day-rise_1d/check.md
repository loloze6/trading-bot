---
backtest: 075-01_heavy-volume-next-day-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5045 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.103 | above 0 | no |
| Mean daily return, on days in a position | 0.0003884 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3521 | above 0 | yes |
| Calmar | 0.2908 | above 0.75 | no |
| Trades per day | 0.7649 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.469 % |
| Yearly return | +10.7 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01_heavy-volume-next-day-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
