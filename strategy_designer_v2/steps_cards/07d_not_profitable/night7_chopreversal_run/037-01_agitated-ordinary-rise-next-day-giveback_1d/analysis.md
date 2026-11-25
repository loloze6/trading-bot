---
line: 7.d confirmed, not profitable
backtest: 037-01_agitated-ordinary-rise-next-day-giveback_1d
idea tested: 037-01_agitated-ordinary-rise-next-day-giveback
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3636 USD
---
## Findings
- **F1:** The tested signal only works in agitated markets whose 60-day trend is falling. There, after a rise within the usual swing, the next-day excess return in the short direction is +1.11 % (t 3.78, 282 cases). In agitated rising markets it is -0.17 % (t -0.58, 271 cases), so the losing half of the book sits in rising markets.
- **F2:** The book's gain splits the same way. Short positions taken in the mean_reversion regime summed +0.577 in falling markets (232 position bars, +0.25 % per bar) and +0.229 in choppy markets (42 bars). They summed -0.276 in rising markets (237 bars, -0.12 % per bar). The rising-market bars erase about half of the gain and leave the book with a mean daily return of -3.6e-05 on days in a position and a Sharpe of -0.06.
- **F3:** The falling trend is not an effect of its own in the short direction. On agitated falling bars without the signal, the next-day short excess return is -1.01 % (t -3.76, 456 cases): the coin rebounds. With the signal it is +1.11 %. So the give-back belongs to the ordinary rise inside a falling, agitated market. This fits the brief's theory: in a falling, agitated market, an up day is short-covering and stop-outs that carry no news.
- **F4:** The choppy condition cannot be used for a repair. Agitated choppy bars without the signal earn +1.88 % short (t 1.72, 76 cases), about as much as with it (+1.97 %, t 1.78, 44 cases), so there the condition carries the move rather than the idea.
- **F5:** Agitation is needed inside the falling trend. In calm falling markets the same signal gives only +0.17 % short (t 0.73, 423 cases), against +1.11 % when agitated. This is the brief's own distinction between calm and agitated markets.
- **F6:** Inside agitated falling markets the effect is roughly graded by the size of the rise and is steady over time.
- **F7:** The move against the cost of a trade:

## Ideas
- `037-01.d1_falling-agitated-rise-giveback` (from F1, F2, F3, F5, F6, F7): In a falling, agitated market, the larger a coin's one-day rise relative to its 30-day daily swing, while staying within that usual swing, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
