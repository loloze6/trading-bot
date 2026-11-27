---
line: 7.d confirmed, not profitable
backtest: 074-01.b1_falling-deep-run-break-fade_1d
idea tested: 074-01.b1_falling-deep-run-break-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4285 USD
---
## Findings
- **F1:** The check failed on Calmar (0.459, with a yearly return of +6.5 %), and the book's deepest falls came on squeeze days, when the coins rose sharply the day after a bounce. The worst book day was −6.3 % on a day the coins rose +12.2 %; that was in w9, whose own deepest fall was −10.6 %. In w14 the book lost −3.2 % and −3.1 % on days the coins rose +11.0 % and +12.5 %. The 40 worst cases had a median next-day rise of +7.1 %, a median position of −0.61 and a median forecast of −14, against −0.24 and −6.4 over all 937 cases.
- **F2:** The effect depends on how agitated the coin has been recently, which the falling profile alone does not capture. By the ratio of the coin's 10-day swing to its 60-day swing, the cases' drift-adjusted short gain was:
- **F3:** Agitation is not a short effect of its own; it points the other way. On falling-market days without the signal, the top quartile of the 10-day/60-day swing ratio was followed by a coin rise beyond drift: short gain −1.01 %, t −3.2, 377 days. Agitated non-signal falling days (30-day swing rank above 0.5) gave −0.81 % (227 days). So in agitated downtrends, only the trapped-holder bounce is followed by a fall, which fits the brief's waiting-supply theory.
- **F4:** Gross of fees, the book on all cases had a Calmar of 1.63 (deepest fall −9.4 %, yearly +15.3 %, Sharpe 1.42). Two restrictions cut the deepest fall while keeping the Sharpe:
- **F5:** The effect grows with the depth of the coin's 20-day fall:
- **F6:** The gain is concentrated in w7 (+1.48 % per case, 141 cases) and w14 (+2.28 %, 145 cases). w10, w11, w12 and w17 lost (−0.53 % to −1.57 % per case), but on only 9, 6, 34 and 27 cases. It holds across coins: from +0.55 % per case (XRP) to +1.27 % (ETH).
- **F7:** In the shallowest forecast quartile the cases still gained +0.85 % (t 2.7, 234 cases), but the mean position was −0.03, so the book made −0.03 in summed P&L after a 0.19 % trade cost. Its gain comes from the deep-forecast quartile: +1.68 %, t 5.4, mean position −0.73, summed P&L 2.82.

## Ideas
- `074-01.b1.d1_run-break-fade-widening-swing` (from F1, F2, F3, F4): In a falling market, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day. The deeper the run's fall, measured as the coin's return over the run's down days against its usual daily swing over the last 30 days, the larger that fall, and it is larger still the more the coin's swing over the last 10 days exceeds its swing over the last 60 days.
- `074-01.b1.d2_run-break-fade-steep-slide` (from F4, F5, F7): In a falling market, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day. The deeper the run's fall against its usual daily swing over the last 30 days, and the deeper the coin's 20-day return, the larger that fall.
- `074-01.b1.d3_agitated-falling-run-break-fade` (from F2, F3, F1): In a falling, agitated market, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day. The deeper the run's fall, measured as the coin's return over the run's down days against its usual daily swing over the last 30 days, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
