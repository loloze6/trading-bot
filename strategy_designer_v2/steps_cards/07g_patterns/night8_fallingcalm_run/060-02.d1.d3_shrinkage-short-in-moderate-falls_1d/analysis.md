---
line: 7.g patterns
backtest: 060-02.d1.d3_shrinkage-short-in-moderate-falls_1d
idea tested: 060-02.d1.d3_shrinkage-short-in-moderate-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4868 USD
---
## Findings
- **F1:** In a falling market (60-day return below -10 %), a one-day rise that is large against the coin's 20-day daily swing is followed by a further fall. On the 3-day grid, the excess return falls as the rise grows: the slope is -0.0149 per unit of scaled rise (t -2.61, n 350, up days only). Up days scaled 1 to 1.5 are followed by -3.9 % (t -2.69, n 28). Up days scaled 1.5 to 2 are followed by -6.6 % (t -3.37, n 16). Up days scaled 1 to 2 together are followed by -4.9 % (t -4.18, n 44). Up days scaled below 0.5 are followed by +0.4 % (n 184).
- **F2:** The failed bounce in F1 holds in calm and agitated markets alike. For rises scaled above 1, the 3-day excess return is -3.1 % when the coin is agitated (t -2.58, n 53) and -4.3 % when it is calm (t -2.50, n 18). It is negative in 2018 (-3.5 %), 2019 (-5.4 %) and 2020 (-5.4 %), and positive in 2021 (+4.8 %, n 8). It is negative in 7 of the 10 windows that have cases, and on 5 of the 6 coins. The effect does not reach the largest rises: rises scaled above 2 are followed by only -0.9 % (t -0.56, n 27). It also fades over 5 days: rises scaled 1 to 1.5 are followed by -1.5 % over 5 days (t -0.57).
- **F3:** In a choppy market (60-day return between -10 % and +10 %), a 5-day fall continues, and the larger the fall against the 20-day swing, the larger the next move down. Over 5 days, the slope of the excess return on the scaled 5-day fall is +0.116 (t 5.09, n 61), and over 3 days it is +0.063 (t 4.09, n 102). Scaled falls of -0.5 to -1.5 are followed by -4.9 % over 3 days (t -3.34, n 39). The quarter of choppy cases with the deepest past-5-day fall is followed by -8.7 % over 5 days (t -3.70, n 32). In the 20-day return quintiles inside choppy markets, the excess return rises steadily: -10.8 %, -3.5 %, -2.0 %, +2.0 %, +3.2 %.
- **F4:** The continuation in F3 is not one year or one kind of market. Choppy cases with a scaled 5-day fall below -0.5 are followed by a negative 5-day excess return in every year (2018 -11.1 %, 2019 -3.1 %, 2020 -20.6 %, 2021 -10.5 %). It is negative in calm markets (-8.4 %, t -2.45, n 15) and in agitated ones (-15.8 %, t -2.35, n 7), and on all 6 coins. Choppy markets hold no short strategy in the agitated profile and only one in the calm profile.
- **F5:** The tested idea's own effect sits in the strongest shrinkage and is not graded. In falling markets, the quarter with the most shrunken 30-day volume is followed by -3.1 % over 5 days (t -2.69, n 101). The other three quarters are followed by -0.6 %, +1.1 % and +0.6 %. Even that strongest quarter turns to +6.8 % in 2020. The book's trades show the same pattern: trades entered on the weakest shrinkage forecasts lost -1.49 % net (n 106), while the other three forecast quartiles earned +1.16 % to +2.17 % (n 106 to 107).
- **F6:** Moderate 20-day falls continue and the deepest ones do not. Over all bars, the second-lowest 20-day-return quintile is followed by -3.0 % over 5 days (t -5.00, n 282), and the lowest quintile by -0.2 % (t -0.26). Inside falling markets the same pattern holds: -3.9 % (n 103) against +0.7 % (n 152). This is the "not yet a crash" part the tested idea already uses.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.d1.d3.g1_falling-market-bounce-fails` (from F1, F2): In a falling market, the larger a coin's one-day rise against its usual daily swing over the past 20 days, the more the coin falls over the next 3 days.
- `060-02.d1.d3.g2_choppy-market-fall-continues` (from F3, F4): In a choppy market, the larger a coin's 5-day fall against its usual daily swing over the past 20 days, the more the coin keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
