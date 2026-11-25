---
backtest: 058-02.b1.b2.b1.b2_calm-market-range-position_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.06 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5072 | above 0 | yes |
| Mean daily return, on days in a position | 0.001281 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9385 | above 0 | yes |
| Calmar | 1.145 | above 0.75 | yes |
| Trades per day | 0.3044 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.345 % |
| Yearly return | +27.1 % (over 7.94 years) |
| Days in a position | 58 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2_calm-market-range-position_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
