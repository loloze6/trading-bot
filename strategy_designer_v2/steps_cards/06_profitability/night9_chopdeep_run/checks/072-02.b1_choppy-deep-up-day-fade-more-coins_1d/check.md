---
backtest: 072-02.b1_choppy-deep-up-day-fade-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1486 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4589 | above 0 | no |
| Mean daily return, on days in a position | 0.0001877 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.0292 | above 0 | no |
| Calmar | 0.03804 | above 0.75 | no |
| Trades per day | 0.06775 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.335 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-02.b1_choppy-deep-up-day-fade-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
