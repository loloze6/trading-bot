---
backtest: 058-02.g1.b1_choppy-agitated-fall-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2008 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3469 | above 0 | no |
| Mean daily return, on days in a position | 0.0005719 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1471 | above 0 | no |
| Calmar | 0.12 | above 0.75 | no |
| Trades per day | 0.02602 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.410 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.g1.b1_choppy-agitated-fall-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
