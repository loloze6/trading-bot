---
backtest: 058-02.b1.g1.b1_falling-rally-fades-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.0722 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6797 | above 0 | no |
| Mean daily return, on days in a position | -8.552e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2486 | above 0 | no |
| Calmar | -0.0578 | above 0.75 | no |
| Trades per day | 0.1432 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.566 % |
| Yearly return | -1.4 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1_falling-rally-fades-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
