---
backtest: 058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3554 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1973 | above 0 | no |
| Mean daily return, on days in a position | 0.0004586 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1661 | above 0 | yes |
| Calmar | 0.1653 | above 0.75 | no |
| Trades per day | 0.1097 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.632 % |
| Yearly return | +3.6 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
