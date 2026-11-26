---
backtest: 058-01.b1_calm-downtrend-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1926 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3602 | above 0 | no |
| Mean daily return, on days in a position | 0.0003895 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.03193 | above 0 | yes |
| Calmar | 0.09422 | above 0.75 | no |
| Trades per day | 0.07063 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.781 % |
| Yearly return | +1.8 % (over 7.94 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b1_calm-downtrend-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
