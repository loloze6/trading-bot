---
backtest: 058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.073 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5206 | above 0 | yes |
| Mean daily return, on days in a position | 0.001506 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9389 | above 0 | yes |
| Calmar | 1.163 | above 0.75 | yes |
| Trades per day | 0.2685 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.541 % |
| Yearly return | +31.4 % (over 7.94 years) |
| Days in a position | 57 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
