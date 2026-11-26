---
backtest: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.01547 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05092 | above 0 | no |
| Mean daily return, on days in a position | 3.055e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2424 | above 0 | no |
| Calmar | -0.05902 | above 0.75 | no |
| Trades per day | 0.1236 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.572 % |
| Yearly return | -0.4 % (over 0.87 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
