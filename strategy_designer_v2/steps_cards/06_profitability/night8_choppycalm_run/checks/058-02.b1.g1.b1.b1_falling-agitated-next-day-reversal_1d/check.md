---
backtest: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.019 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4663 | above 0 | yes |
| Mean daily return, on days in a position | 0.001699 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8263 | above 0 | yes |
| Calmar | 0.9453 | above 0.75 | yes |
| Trades per day | 0.1479 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.578 % |
| Yearly return | +11.2 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
