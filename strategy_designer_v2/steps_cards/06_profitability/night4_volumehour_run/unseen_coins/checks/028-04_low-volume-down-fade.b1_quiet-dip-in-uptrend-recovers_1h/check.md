---
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, LTC, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI, XMR, XRP, ZEC as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, LTCUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2117 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7838 | above 0 | no |
| Mean daily return, on days in a position | -0.0002218 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4078 | above 0 | no |
| Calmar | -0.1368 | above 0.75 | no |
| Trades per day | 1.255 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.839 % |
| Yearly return | -4.6 % (over 7.94 years) |
| Days in a position | 42 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/unseen_coins/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
