---
backtest: 058-01.b2.b1_quiet-calm-fall-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.07331 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5072 | above 0 | no |
| Mean daily return, on days in a position | 0.0001584 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.0416 | above 0 | no |
| Calmar | 0.002061 | above 0.75 | no |
| Trades per day | 0.03668 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.723 % |
| Yearly return | +0.1 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b2.b1_quiet-calm-fall-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
