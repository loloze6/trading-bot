---
backtest: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.09716 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.093 | above 0 | no |
| Mean daily return, on days in a position | 0.0002639 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2121 | above 0 | no |
| Calmar | 0.07953 | above 0.75 | no |
| Trades per day | 0.01752 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.119 % |
| Yearly return | +0.2 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
