---
line: 7.g patterns
backtest: 031-02.b2.a1_deep-fall-rebound-nineteen-coins_1d
idea tested: 031-02.b2.a1_deep-fall-rebound-nineteen-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4551 USD
---
## Findings
- **F1:** The coins' Saturday daily return is the only weekday that stands out from the rest. It averages +0.456 % (t 2.99 over 414 days, coins of one day taken together; Welch t 2.29 against the other days). It is above the other weekdays' mean in 15 of 17 coins (88 %) and is positive in both halves of the windows (+0.59 % in w1–w12, +0.32 % in w13–w24). Still, it is one of 7 weekdays tested, and it is a calendar condition with no grading in it.
- **F2:** Wednesday, Friday and Saturday together beat the other weekdays in 7 of 8 years, by +0.21 % to +1.23 % a day. The one exception is 2022, at −0.05 %. Thursday is the weakest day, at −0.26 % (t −1.14; Welch t −1.79 against the rest).
- **F3:** Inside the tested regime, the 67 cases whose last 30 days fell rose +5.28 % over 30 days, against −1.71 % for the 18 cases whose last 30 days did not fall. Across the 85 cases, the 30-day rise has a Spearman correlation of +0.14 with the 90-day depth, +0.13 with the 30-day depth and −0.21 with the last 7-day return (about t −1.96). None of these stands out given how many angles were looked at.
- **F4:** Ranking the 30-day forward return by each coin's past 7-, 30- or 60-day return quintile gives no ordered pattern; every quintile mean has |t| < 1.9. The 30-day reversal the brief expects is absent: the lowest 30-day-return quintile went on to −6.8 % unusual over 30 days (t −1.69, 39 days). At a 7-day horizon the top 30-day quintile shows only weak momentum, +2.05 % (t 1.83).
- **F5:** Volatility level does not separate the 30-day outcome. By the coin's own 20-day volatility tercile, the low tercile is +6.6 % (t 1.26), the middle −3.9 % (t −1.45) and the high −3.4 % (t −0.85).
- **F6:** The book's gain comes from a few days. Its 10 best days make up 63 % of the summed daily book return. By year, it earned +31.3 % (2020) and +35.4 % (2023) in summed daily returns but lost −10.8 % in 2022, with its daily standard deviation at 1.38 % that year against 0.08 % in 2021 and a worst day of −6.5 %. That 2022 loss is what sinks the Calmar.
- **F7:** Unusual 30-day returns over all grid bars swing with market years, not with any per-coin situation: −18.3 % in 2018 (t −3.88, 13 days) and −8.9 % in 2022 (t −1.78) against +9.8 % in 2020 and +5.6 % in 2023.

## Ideas
- No ideas: The only pattern that stands out after this many angles is a Saturday rise (F1, F2), which is a fixed calendar condition with no grading. Everything graded (forecast parts, past returns, volatility, recent week inside the regime; F3–F5) cannot be told from chance, so no graded, one-direction idea is supported.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
