---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4612 USD
---
## Findings
- **F1:** Inside the choppy agitated profile, the 5-day move falls more as the close nears the day's high. The unusual move by close-location quintile goes −1.0 %, +0.6 %, −2.6 %, −3.9 %, −7.8 %, and the top quintile has t −3.18 on 20 cases. Outside the profile, high closes are followed by slight rises: quintiles 3 to 5 show +1.0 %, +1.0 % and +0.8 %, all with t under 1.5. This is the tested idea's own effect. It lives in the brief's profile and adds nothing new.
- **F2:** Within the profile, the fall needs both parts of the situation. With a negative 5-day return and a close in the upper half, the unusual move is −12.1 % (t −3.35, 22 cases). A negative 5-day return with a close in the lower half gives +1.4 % (t 0.68, 22 cases). A positive 5-day return with a close in the upper half gives −2.4 % (t −1.27, 22 cases). So the apparent continuation of 5-day falls in this profile (deepest 5-day-return quintile −8.1 %, t −2.0, 23 cases) is the tested idea itself and nothing more.
- **F3:** The situation is rare, so the book is thin and its profit is concentrated.
- **F4:** The trades' gains come from a few large wins rather than a steady edge.
- **F5:** 20-day-return momentum does not hold steadily.
- **F6:** The narrow-range high-close continuation fails once cases on the same day are pooled. It shows +2.2 % with an ordinary t of 3.27 (353 cases, tercile of range relative to price). With the range ranked against its own past 30 days and the same day's cases pooled, it drops to +1.2 % (t 1.03, 116 days). It is positive in only 6 of 12 windows, ranging from −5.9 % to +14.7 %.
- **F7:** The weekday pattern alternates in sign and does not stand out after the many angles looked at.

## Ideas
- No ideas: The only pattern that stands out is the tested idea's own effect, already in the brief's profile (F1, F2). The other angles were 20-day momentum, range width with close location, volatility level with the last day's sign, weekday, window, coin and trades. Each either drops below t 2 once same-day cases are pooled, changes sign across windows or years, or repeats a calm-rise momentum the profile map already holds (F5, F6, F7).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
