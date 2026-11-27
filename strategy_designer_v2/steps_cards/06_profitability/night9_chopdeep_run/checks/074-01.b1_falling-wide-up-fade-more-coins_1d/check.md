---
backtest: 074-01.b1_falling-wide-up-fade-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1639 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4436 | above 0 | no |
| Mean daily return, on days in a position | 0.0004005 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.08577 | above 0 | no |
| Calmar | 0.06712 | above 0.75 | no |
| Trades per day | 0.04888 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.446 % |
| Yearly return | +1.0 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1_falling-wide-up-fade-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
