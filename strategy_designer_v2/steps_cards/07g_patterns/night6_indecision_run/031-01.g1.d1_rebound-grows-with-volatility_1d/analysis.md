---
line: 7.g patterns
backtest: 031-01.g1.d1_rebound-grows-with-volatility_1d
idea tested: 031-01.g1.d1_rebound-grows-with-volatility
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3897 USD
---
## Findings
- **F1:** Low-close days rebound only when the coin's volatility is high. Days closing in the bottom quarter of their range gain +1.28 % on the next day, above the coin's average, when the 20-day volatility over its 60-day mean is in its top third (692 cases, t 3.59). In the middle third they gain +0.15 % (708 cases, t 0.67), and in the bottom third −0.07 % (782 cases, t −0.27). Across all days the same thirds give only −0.18 %, 0.00 % and +0.12 % (t −1.25 to 0.75).
- **F2:** Inside that high-volatility third, the rebound does not need the plan's 1.5× range. Low-close days with a range of only 1.0 to 1.5 times the 20-day mean range gain +1.75 % (208 cases, t 3.99), and those beyond 2.5 times gain +8.50 % (27 cases, t 2.41). The same range bands in the low-volatility third give +0.07 % to +0.50 % (all t < 0.9).
- **F3:** Across all low-close days, the next-day excess return grows with the day's range against its 20-day mean:
- **F4:** On wide days (range ≥ 1.5× the 20-day mean), the next-day excess return falls steadily as the close moves up the day's range:
- **F5:** Large down days in volatility units (a 1-day return at or below −1.5 times the prior 20-day volatility) also rebound only when volatility is high: +1.76 % the next day in the top third of the volatility ratio (221 cases, t 2.08), against −0.51 % in the bottom third (267 cases, t −1.18). Over all days, the largest down-return decile gains +0.69 % the next day (1720 cases, t 2.45).
- **F6:** On the signal days, the next-day excess return rises with the volatility ratio:
- **F7:** The book's gain is concentrated. Its 10 best (window, day) days sum to +0.538 of a total summed daily return of +0.785, while its 10 worst sum to −0.317. Its 99th daily percentile is +1.36 % against a 1st percentile of −0.65 %.
- **F8:** No other angle stood out given how many angles were examined:

## Ideas
- `031-01.g1.d1.g1_low-close-rebounds-when-volatile` (from F1, F2, F6): When a coin's 20-day daily volatility is high against its own 60-day average, a day that closes near its low is followed by a rise over the next 1 day. That rise is larger the higher this volatility ratio is, and it holds whether or not the day's range was unusually wide.
- `031-01.g1.d1.g2_rebound-grows-with-range-width` (from F3, F2, F4): After a day that closes near its low, the coin rises over the next 1 day by more the wider that day's high-low range is against its average daily range over the past 20 days, growing steadily from ordinary-range days to the widest ones.
- `031-01.g1.d1.g3_volatile-sharp-drops-rebound-next` (from F5, F1): When a coin's 20-day daily volatility is high against its own 60-day average, the larger the day's fall measured in units of its prior 20-day volatility, the larger the coin's rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
