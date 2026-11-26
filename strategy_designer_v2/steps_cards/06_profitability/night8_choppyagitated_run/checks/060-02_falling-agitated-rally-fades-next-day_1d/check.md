---
backtest: 060-02_falling-agitated-rally-fades-next-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3799 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1729 | above 0 | no |
| Mean daily return, on days in a position | 0.0005945 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2331 | above 0 | yes |
| Calmar | 0.3348 | above 0.75 | no |
| Trades per day | 0.06288 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.331 % |
| Yearly return | +2.2 % (over 7.94 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-02_falling-agitated-rally-fades-next-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
