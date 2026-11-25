---
line: 7.b inconclusive
backtest: 036-02_fall-vs-range-next-day-rebound_1d
idea tested: 036-02_fall-vs-range-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2188 USD
---
## Findings
- **F1:** On the folds shown (B, C), the plan's measure on the next day is positive but short of the bar: the mean next-day excess return is +1.07 % with t 1.83 over 124 case days (344 cases) and Spearman +0.13; on all folds step 5 has +1.73 % with t 1.93 over 365 case days and Spearman +0.06. The effect is on the predicted side, and the evidence is too thin to clear t 2.
- **F2:** The effect is not confined to one coin. Every one of the six coins has a positive next-day excess return, from +0.57 % (BTC) to +1.55 % (XRP). Each coin alone has a t of only 1.0 to 1.6 on 53 to 62 days. More coins add independent evidence, where narrowing would remove it.
- **F3:** The effect is not confined to one period either. All four years shown are positive (2018 +0.98 %, 2019 +0.29 %, 2020 +2.25 %, 2021 +0.76 %), and 10 of the 12 windows are positive (w9 −0.62 % and w11 −0.42 % are the exceptions). It is steady across periods, and each period's count is small.
- **F4:** The rebound is graded with the fall's size relative to the range, as the idea says. The top quartile of the ratio gains +2.77 % (t 1.77, 38 days) against +0.52 %, −0.02 % and +0.99 % for quartiles 1 to 3. The largest falls carry the effect, and they are the rarest cases.
- **F5:** The plan's 1-day horizon is where the effect shows. The excess return fades from +1.07 % (t 1.83) at 1 day to +0.77 % (t 1.21) at 2 days and +0.93 % (t 1.17) at 3 days, then −0.07 % (t −0.06) at 5 days. Another horizon would not sharpen the test.
- **F6:** The mean is not driven by a few outliers. The median case's next-day excess return is +1.16 %, and 64 % of cases are positive. The weak t comes from the noise of a 4.78 % usual daily move against an unusual move of +0.46 % per case (strength 0.089).
- **F7:** No trend profile isolates the effect. Falling markets show +1.56 % (t 1.15, 42 days) and rising markets +1.31 % (t 1.60, 43 days), against +0.19 % in choppy ones (28 days). Splitting by profile only shrinks the sample. I could not read the agitation profile here: each window is shorter than the 365-day baseline it needs.
- **F8:** The book's total move per case (+0.58 %) is 3.0 times the 0.19 % cost of a trade, so the effect is large enough to pay once it is shown to be real.

## Ideas
- `036-02.b1_outsized-fall-rebound-more-coins` (from F1, F2, F3, F4, F6, F8): The further a coin's one-day close-to-close fall exceeds its average daily high-to-low range over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
