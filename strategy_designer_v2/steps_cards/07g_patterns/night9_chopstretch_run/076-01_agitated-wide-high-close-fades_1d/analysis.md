---
line: 7.g patterns
backtest: 076-01_agitated-wide-high-close-fades_1d
idea tested: 076-01_agitated-wide-high-close-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3966 USD
---
## Findings
- **F1:** In folds B and C, inside a 60-day falling, agitated market, the next-day move after the day is graded by the day's own return scaled by its 20-day swing. Days below −1.5 swings rise 4.5 % more than the drift (t 1.94, 38 cases, 24 days), and days from −1.5 to −0.5 rise 1.5 % more (t 2.18, 179 cases). Days from +0.5 to +1.5 fall 1.1 % (t −1.98, 132 cases), and days above +1.5 fall 2.0 % (t −1.39, 40 cases). This is the next-day reversal that 058-02.b1.g1.b1.b1 (falling agitated, both) and the falling-agitated rebound family already hold.
- **F2:** The up-day fall in F1 (days above +0.5 swings) has a negative mean in each of the 4 years (−1.9 %, −1.8 %, −0.9 %, −0.7 %; t −1.52, −2.76, −1.03, −0.80) and on each of the 6 coins (t −1.19 to −2.46). Within those up days, however, the size of the day's rise does not grade the fall (correlation −0.014, 172 cases).
- **F3:** For the tested pattern itself, among agitated days of any trend, very wide days (range above 1.7 times the 20-day mean) closing in the top fifth fall 1.8 % the next day (t −1.88). The same width closing in the bottom fifth rises 3.0 % (t 1.25), and rising markets, where most of these days fall, give only t −1.01 (53 cases, 42 days). The wide-and-high-close product is barely related to the next day (correlation −0.037), and close location alone gives −0.083.
- **F4:** In a 30-day choppy, agitated market, the next day's move grades with the close location. Closes in the bottom third rise 0.67 % (t 1.19, 123 cases), the middle third falls 0.67 % (t −1.12), and the top third falls 0.99 % (t −1.94, 181 cases, 124 days). Under the profile's own 60-day trend, choppy agitated days are few (120 cases, 84 days).
- **F5:** The book's short forecast does not grade its outcome. The most negative quarter of the forecast falls 1.06 % (t −2.09, 172 cases), but the least negative quarter falls about as much (1.10 %, t −1.41), and the third quarter rises 0.43 % (t 0.79).
- **F6:** Weekday shows nothing in agitated markets: t ranges from −0.75 to +0.84. The 5-day scaled return grades nothing in either regime: |t| is below 1.82 in every quintile.

## Ideas
- No ideas: Across the many angles examined (close location by width, the day's and the 5-day scaled return by trend and agitation, weekday, year, coin, forecast quarters), only the falling-agitated next-day reversal (F1, F2) stands out. It is already held by 058-02.b1.g1.b1.b1 and the falling-agitated rebound family. The candidate for the empty choppy-agitated short cell (F4, t −1.94) and the tested wide-high-close fade (F3, t −1.88) do not clear the bar that this many looks require.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
