---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade_1d
idea tested: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6863 USD
---
## Findings
- **F1:** Over the next 2 days, the unusual move after a moderate 5-day fall is negative across all coins and profiles. A fall of -1.5 to -0.5 of the coin's usual 5-day swing is followed by -0.84 % (t -3.41, 910 non-overlapping cases). After a rise of +0.5 to +1.5 swings the next 2 days show +0.41 % (t 1.80), and after one above +1.5 swings +0.74 %. Short-term moves continue rather than revert.
- **F2:** In choppy markets (60-day return between -10 % and +10 %), this 2-day continuation rises step by step with the 5-day move:
- **F3:** In choppy and falling markets together, the falls below -0.5 swings carry it.
- **F4:** In rising markets the same moderate 5-day fall is followed by +0.52 % over 2 days (t 1.06, 199 cases). The continuation of falls belongs to non-rising markets.
- **F5:** The tested situation inside its profile does not stand out at 2 days.
- **F6:** The book's tails are pure short exposure.
- **F7:** After a 5-day rise above 1.5 usual swings the next 10 days gain +8.07 % unusual (t 3.66, 62 cases). It is concentrated in w11 (+17.2 %) and w17 (+16.7 %) and reverses in w14 (-2.9 %). It lives mainly in rising calm markets, where the map already holds 9 long strategies.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d2.d2.g1_choppy-five-day-fall-continues` (from F1, F2, F3, F4): In a choppy market, a coin that has fallen over the last five days, measured against its usual five-day swing, keeps falling over the next two days, and the larger that five-day fall against its swing, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
