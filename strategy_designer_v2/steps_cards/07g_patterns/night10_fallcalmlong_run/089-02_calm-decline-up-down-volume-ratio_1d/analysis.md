---
line: 7.g patterns
backtest: 089-02_calm-decline-up-down-volume-ratio_1d
idea tested: 089-02_calm-decline-up-down-volume-ratio
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3822 USD
---
## Findings
- **F1:** The tested lean points the wrong way inside falling calm. The raw log up/down volume ratio has a Spearman of -0.133 (p 0.11, 146 cases) against the 5-day excess return, and its top tercile ends -2.38 % against +1.22 % for its bottom tercile (Welch t -1.86). Its day-clustered rank-slope t is -1.78 at 5 days and -1.91 at 3 days. Neither stands out from chance, which matches step 5's no effect (unusual move -0.56 %, t -1.04).
- **F2:** Inside falling calm, a coin's distance above its 20-day low, scaled by its 20-day swing, predicts the next 5 days. The rank correlation is 0.242 (p 0.008, 121 cases) and the day-clustered rank-slope t is 2.44. The unscaled distance gives 0.212 and t 2.29, and the 10-day version gives t 2.42. Outside the profile the same measure gives 0.035 and t 0.80 on 572 cases, so the relation lives in falling calm markets.
- **F3:** Split into terciles of the distance above the 20-day low (inside falling calm), the 5-day excess return climbs steadily: -3.81 %, -2.28 % and +1.27 % (40, 40 and 41 cases; the mean distance is 4 %, 11 % and 26 %).
- **F4:** The effect is short-lived and needs a recent low.
- **F5:** The 5-day return relates the same way inside falling calm: Spearman 0.175 and clustered t 2.03 at 5 days, 0.154 and t 2.02 at 3 days, against t 0.55 outside the profile. A coin that has already lifted off a calm decline keeps going; one still pressed near its low keeps sliding (-3.8 % excess in F3's bottom tercile).
- **F6:** The tested book lost in the earlier years: in-profile cases ended -3.8 % excess in 2018 and -2.9 % in 2019, against +3.1 % and +3.4 % in 2020 and 2021. Only BCH (+1.7 %) of the four coins was positive. The trades lost a mean -6.2 % on ETH and -3.6 % on ZEC.
- **F7:** I looked at about 15 bar measures, three horizons, inside and outside the profile, with weekday and year splits. Only the distance above a recent low (F2, F3) stands out with consistent signs across coins and years. Weekday means swing from -5.0 % to +4.1 % on 14 to 26 cases each, which is noise.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `089-02.g1_calm-decline-lift-off-low` (from F2, F3, F4, F7): In a falling, calm market, the further a coin's close has risen above its lowest low of the last 20 days, measured against its usual daily swing over those days, the more the coin rises over the next 5 days.
- `089-02.g2_calm-decline-short-push-continues` (from F5, F3, F7): In a falling, calm market, the larger a coin's 5-day return measured against its usual daily swing, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
