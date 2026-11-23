---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5547 USD
---
## Findings
- **F1:** The tested rebound is real when pooled but uneven over time. Sunday falls are followed by a 3-day excess of +0.97 % (t 4.67 over 2125 cases, counted per coin and Sunday). Measured per date, no single year reaches |t| 1.4, and the yearly mean ranges from −1.98 % in 2018 (29 dates) to +2.39 % in 2021 (36 dates).
- **F2:** The years where the rebound failed are the years where the coins fell, and they are where the book lost its Calmar. In 2018, 2022 and 2025 the coins' mean daily return was −0.35 %, −0.26 % and −0.03 %, and the Sunday-fall excess was −1.98 %, −0.44 % and −0.12 %. In 2020, 2021 and 2024, with coin means of +0.47 %, +0.64 % and +0.28 %, it was +1.24 %, +2.39 % and +1.17 %; 2023 is the exception at −0.32 % with a +0.32 % coin mean. The book lost −0.077 % a day in 2018 and −0.069 % a day in 2022, with mean trade returns of −0.60 % and +0.11 % (184 and 643 trades), against +2.7 % to +6.1 % in 2019–2021.
- **F3:** The coin's 20-day volatility, more than the weekday, carries the rebound. After Sunday falls larger than one daily volatility, the 3-day excess by volatility tercile is −0.14 %, +1.39 % and +3.83 % (126, 146 and 105 cases). Non-Sunday falls of that size in the top tercile also show +1.73 % (t 1.51 over 101 dates, sampled on the non-overlapping grid).
- **F4:** Sunday rises also reverse when pooled, but it does not hold up. The pooled reversal is +1.02 % (t 5.48 over 2186 cases). Measured per date, the four size quartiles give t of only 1.18 to 2.10 over 172–214 dates each. The effect does not grow with the size of the rise (slope t 0.52, and the largest quartile is the weakest at +0.76 %). It is positive in 5 of 8 years.
- **F5:** Saturday falls appear to continue, but this cannot be told apart from chance. Pooled, the 3-day excess after them is −0.68 % (t −3.39 over 1961 cases), but measured per date the four quartiles give t of 0.37 to 1.83, and the years split 5 against 3.
- **F6:** The volume claim in the brief does not show; if anything it points the other way. The Sunday-rise reversal grows with that day's volume relative to the last 20 days rather than with thinness: +0.52 %, +0.94 % and +1.06 % for low, mid and high volume (t 0.95, 1.77 and 1.93 per date). None of these can be told apart from chance.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound.g1_weekend-fall-rebound-in-uptrends` (from F1, F2, F3): In a coin whose own 60-day return is positive, a Sunday fall (the Sunday close-to-close return) is followed by a rise over the next 3 days. The rise is larger the larger the fall times the coin's 20-day volatility of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
