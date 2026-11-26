# Topic 55: which data each research step uses, and what moves a strategy to the next step

Status: running (a draft for the operator's review; next steps A4)  
Where: every research step, the tests on new data, the combination, the sealed holdout; becomes a shared definition
(`common/`) once agreed  
Opened: 2026-11-26, the operator: "have a full process agreed between fold and currency used, from ideas,
confirmation, combination, test ... standardize this so that we close this topic and it is processed following
guideline, not my decision"; then: "more global around data usage in the various research steps and automated unlock
of the next step"; then: "steps ordered; no acronyms; concrete and not complex".

## The question
At each step, which data may it look at, so that a result is always judged on data that did not help find it, and the
last verdict is given once, on data nobody ever used?

## The data
| Data | Years | Coins |
|---|---|---|
| Research years, first half | 2018 to 2021 | the strategy's coins (6 by default: BTC, ETH, LTC, XMR, XRP, ZEC) |
| Research years, second half | 2022 to 2025 | the same coins |
| New years | 2016-2017 and 2026 | the same coins |
| New coins | 2018 to 2025 | the 13 other coins (ADA, AAVE, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI) |
| Sealed data | written only in `trading-bot/config/campaign_data_policy.yaml` | never opened by any step |

## The steps, in order
| # | Step | What it does | Data it uses | Data it never sees | What sends the strategy to the next step |
|---|---|---|---|---|---|
| 1 | Brief | writes a theory | none | all | always |
| 2 | Ideas | turns the theory into ideas | none | all | the loop picks the next idea by its score |
| 3 | Test plan | writes the strategy's settings | none | all | always |
| 4 | Backtest | runs the strategy | research years (2018 to 2025) | new years, new coins, sealed data | always |
| 5 | Is the effect real? | measures the idea's effect | research years; a "yes" must point the same way on 2022 to 2025 alone | the same | "yes" (confirmed) |
| 6 | Does it pay? | Sharpe, Calmar and the other measures | research years | the same | "pays" |
| 7 | Analysts | read the backtest and propose new ideas (back to step 2) | 2018 to 2021 only | 2022 to 2025, new years, new coins, sealed data | — |
| 8 | Test on new years | the same strategy, unchanged | 2016-2017 and 2026 | sealed data | always run after step 6 says "pays" (information only, never a filter) |
| 9 | Test on new coins | the same strategy, unchanged | the 13 other coins | sealed data | the same |
| 10 | Choose the portfolio | the combination card picks the strategies and their weights | research-years results only | the results of steps 8 and 9 | after each batch run, automatically |
| 11 | Judge the portfolio | does it hold? | new coins, then shown on new years | sealed data | the opening rule below |
| 12 | Final verdict | the portfolio on the sealed data | the sealed data, once | — | end |

## Two rules to add
1. **When a result "holds" on new data.** A strategy alone: its effect keeps the same direction and it earns after
   costs (Sharpe above 0), as today. The portfolio: the same, and it earns more than simply holding the same coins on
   the same days (the operator, 2026-11-26: for the portfolio only). Example: on the new coins, holding earned a Sharpe
   of about 1.0; portfolio v2 earned 1.01.
2. **When the sealed data is opened.** For the first portfolio version that holds on the new coins and on both new
   periods. Before opening, its record is written (the version, its commit, what it is expected to show); the result
   is kept whatever it shows; the sealed data is never used again for another version.

## Open questions for the review
1. The portfolio against holding: compare their Sharpe (proposed), or their yearly return?
2. The new years were already looked at when earlier portfolios (P4, P10b) were built. Should the opening of the sealed
   data still require holding on them, or on the new coins alone?
3. Should the new coins stay unused by any choice for every later version (today no choice reads them)?
