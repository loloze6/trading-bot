---
line: 7.b inconclusive
backtest: 012-01_liquidation-flush-rebound_1d
idea tested: 012-01_liquidation-flush-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3672 USD
---
## Findings
- **F1:** The pooled flush-bar result is on the side the idea predicts, a 3-day excess return of +0.0163 (t 2.11, 158 cases, hit rate 55.7%), but it rests on the volume burst alone, because the wick works against the grading: the Spearman correlation of the 3-day excess return is +0.157 with volume ratio, +0.014 with the fall and −0.061 with the wick, so the combined forecast correlation is −0.009.
- **F2:** Across all 1,041 non-overlapping falls of at least one usual move, the 3-day excess return rises with the volume ratio (Spearman +0.073, p 0.018), from −0.0090 (t −1.62) in the lowest volume quintile to +0.0181 (t 2.51) in the highest, while it does not rise with the wick (Spearman −0.061, p 0.050; top wick quintile +0.0001 against +0.0090 in the lowest).
- **F3:** The long wick adds nothing beyond the volume burst: high-volume falls (volume at least 2x the 30-day mean) gain +0.0197 over 3 days (t 2.42, 178 cases) against −0.0008 for other falls (Welch t 2.40), and flush bars (+0.0117) do no better than high-volume falls without the wick condition (+0.0229, 127 cases, Welch t −0.63).
- **F4:** Inside the flush bars, the effect is present only in the largest volume bursts and the weakest prior trend, so it is mixed: the top volume-ratio quartile gains +0.0359 (t 2.69, 28 cases) while the other three quartiles range from −0.0045 to +0.0141 with |t| < 0.8, and forecast quartiles show no order (+0.0020, +0.0216, +0.0276, +0.0145).
- **F5:** The effect varies widely from year to year and coin to coin: flush 3-day excess is −0.0243 (t −2.05) in 2019 and −0.0202 (t −1.42) in 2021 but +0.0687 in 2020 and +0.0395 (t 2.68) in 2024, and no single coin reaches t 2 (BTC +0.0204, t 1.82; ZEC +0.0046, t 0.22).
- **F6:** The predicted rebound does not show at 1 day after flush bars (−0.0009, t −0.18), and it is no stronger at 5 to 10 days (t 1.22 to 1.48), so 3 days is where it shows; ordinary sharp falls, by contrast, rebound most at 1 day (+0.0062, t 4.76, 1,709 cases).

## Ideas
- `012-01_liquidation-flush-rebound.b1_volume-graded-rebound-after-falls` (from F1, F2, F3, F4): When a bar closes sharply lower, price rises over the next 3 days, and the further that bar's volume stands above its own 30-day average volume, the larger the rise.
- `012-01_liquidation-flush-rebound.b2_liquidation-flush-rebound-wider` (from F1, F5): When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days. The more extreme the volume burst and the longer the wick, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
