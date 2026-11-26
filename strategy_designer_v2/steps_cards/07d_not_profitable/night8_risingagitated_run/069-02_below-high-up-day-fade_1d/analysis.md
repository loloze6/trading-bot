---
line: 7.d confirmed, not profitable
backtest: 069-02_below-high-up-day-fade_1d
idea tested: 069-02_below-high-up-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3826 USD
---
## Findings
- **F1:** The book's gain covers its costs barely: its position earned a mean of 0.064 % per coin-day against about 0.046 % of turnover cost (mean turnover × 0.19 %). The idea's next-day move is concentrated in the deepest up-day closes. Up days in the deepest fifth of distance below the 20-day high were followed by a next-day excess return of −1.02 % (t −4.7, 734 cases). The shallowest fifth was followed by +0.29 % (t 1.3, 734 cases). The book shorts nearly every up day (4,077 held up-days at a mean position of −0.40), so it also pays costs on up days that carry little or no move.
- **F2:** In a rising market (60-day return above +10 %) the up-day short loses. Up days there were followed by a next-day excess return of +0.36 % (t 2.0, 908 cases). Even the deepest two fifths gave +0.40 % (t 1.3, 202 cases). The book's position earned −0.063 % per coin-day in rising states, against +0.14 % in falling and +0.15 % in choppy states. This is the market state where the gain is lost.
- **F3:** In a falling market the fade is strong. All up days were followed by a next-day excess return of −0.58 % (t −3.5, 973 cases), and the deepest two fifths by −0.85 % (t −3.7, 571 cases). A falling market alone is not the effect: down days in a falling market were followed by +0.25 % (t 1.6, 1,090 cases), the opposite side. This fits the theory that trapped holders above the price sell into a rise.
- **F4:** The effect is larger in an agitated market, read here as the 30-day swing above its own running median. Deepest-fifth up days were followed by −1.61 % (t −2.8, 147 cases) when agitated and −0.49 % (t −1.5, 355 cases) when calm. Other up days gave −0.54 % (t −3.1) when agitated and −0.06 % when calm. Agitation alone is not the effect: agitated down days were followed by +0.55 % (t 2.6, 965 cases).
- **F5:** The giveback keeps going past one day, so a longer holding spreads the cost over a larger move. On non-overlapping 2-day grids, up days in the deepest fifth fell −1.17 % in excess (t −1.85, 250 cases) and the next fifth −0.92 % (t −2.3, 301 cases). The shallowest fifth rose +0.59 % (t 2.0, 586 cases). On 3-day grids the deepest fifth fell −1.52 % (t −1.9, 180 cases). These moves are 3 to 8 times the 0.19 % cost of a trade, against 1.1 to 1.7 times on the one-day horizon.
- **F6:** The result is uneven across windows. The deepest up days were followed by negative excess returns in 9 of 12 windows; for example w7 −1.21 % (t −3.4), w13 −1.36 % (t −2.3) and w14 −1.19 % (t −2.5). The positive windows were w11 (+1.37 %), w8 (+0.36 %) and w17 (+0.31 %). w11 is also the window with the coins' highest mean daily return (+1.26 %) and the book's worst position gain (−0.17 % per coin-day), which matches the rising-market losses of F2.

## Ideas
- `069-02.d1_falling-market-below-high-up-day-fade` (from F1, F2, F3, F6): In a falling market, when a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.
- `069-02.d2_agitated-below-high-up-day-fade` (from F1, F4): In an agitated market, when a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.
- `069-02.d3_below-high-up-day-two-day-fade` (from F1, F5): When a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
