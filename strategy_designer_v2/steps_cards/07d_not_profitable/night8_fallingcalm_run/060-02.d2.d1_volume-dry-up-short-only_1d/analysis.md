---
line: 7.d confirmed, not profitable
backtest: 060-02.d2.d1_volume-dry-up-short-only_1d
idea tested: 060-02.d2.d1_volume-dry-up-short-only
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5900 USD
---
## Findings
- **F1:** The deepest fall of the book (-14.2 %, lasting 284 days, from a peak in w16 to a trough in w18) came while the coins rose (the coins' mean daily returns summed to +0.87 over those days); the shorts held then had a weaker forecast than elsewhere (mean -4.8 against -9.3), the 29 cases opened inside it lost (mean unusual short move -4.5 % against +2.7 % over the 324 cases outside it), and it was spread across every coin (LTC -6.7 %, BTC -2.6 %, ETH -2.5 % of the book).
- **F2:** The effect lives in the strong part of the shrinkage: by thirds of the forecast, the strongest third (-20 to -13.5) had a mean unusual 5-day short move of +4.9 % (t 5.29, 118 cases), the middle third +1.5 % (t 1.74, 117 cases) and the weakest third -0.06 % (t -0.06, 118 cases); the held days' mean gain was 0.56 %, 0.10 % and 0.02 % by the same bands.
- **F3:** The weak shorts carry the fall: 14 % of the held days with a forecast weaker than -6.5 fall inside the deepest fall, against 3 % for those stronger than -13.5; an approximate book that keeps only forecasts of -6.5 or stronger keeps almost all the gain (summed gain 0.486 against 0.508) and cuts the deepest fall from -14.0 % to -6.0 %, which raises gain over fall from 3.6 to 8.1; keeping only -13.5 or stronger gives 0.418 and -5.8 %.
- **F4:** The falling regime alone does not carry the effect, so the strong shrinkage is not a separate condition: in-regime 5-day grid cells with no short signal had a mean unusual short move of -2.1 % (t -1.90, 171 cases), and those with volume steady or growing -0.9 % (107 cases); the deepest 10-day falls without the signal rebounded (-4.7 %, t -2.65, 55 cases), while the same situation with the signal fell further.
- **F5:** Neither recent agitation nor the distance from the 30-day low sorts the cases, so neither explains the fall. By the 10-day against 60-day swing, the unusual move per case was +4.3 %, +3.3 % and +3.7 % by thirds. By the distance above the 30-day low it was +3.4 %, +1.3 % and +3.8 %. The deepest 60-day falls gave +5.1 % (t 4.75), but the middle third gave only +2.2 % (t 1.47), so that sort is not monotone either.

## Ideas
- `060-02.d2.d1.d1_deep-volume-dry-up-shorts` (from F2, F3, F1, F4): In a falling market, while the coin's 10-day return is still negative, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, the fall growing faster than the shrinkage, so that a deep dry-up brings several times the fall of a mild one, and a mild one brings almost none.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
