---
backtest: 031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2355 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4069 | above 0 | no |
| Mean daily return, on days in a position | 0.0009234 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.5204 | above 0 | no |
| Calmar | 0.04236 | above 0.75 | no |
| Trades per day | 0.03501 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.811 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
