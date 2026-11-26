---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, LTC, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI, XMR, XRP, ZEC as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, LTCUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.352 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1935 | above 0 | no |
| Mean daily return, on days in a position | 0.0006768 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1854 | above 0 | yes |
| Calmar | 0.1196 | above 0.75 | no |
| Trades per day | 0.1577 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.861 % |
| Yearly return | +4.5 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/paying_rerun_run/unseen_coins/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
