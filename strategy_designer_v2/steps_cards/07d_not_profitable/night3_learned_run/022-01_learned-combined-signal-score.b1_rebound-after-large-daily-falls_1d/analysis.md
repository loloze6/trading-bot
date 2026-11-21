---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
idea tested: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3472 USD
---
## Findings
- **F1:** The book fails on Calmar (0.73 against 0.75) because its falls are as deep as a year's gain: its deepest fall is 27.0 % against a yearly return of 19.8 %, and its six deepest falls all run from 21 % to 27 %. Four of them happen while the coins' average fell 22 % to 68 % over the same stretch (-40 %, -68 %, -47 %, -29 %), so the book keeps buying falls inside long declines.
- **F2:** The rebound after a fall depends on whether the coin is in a burst of volatility. Among the book's long bars, split by the ratio of the coin's 7-day to its 30-day volatility, the top quarter's next-day excess return is +0.73 % (t 5.35, 1603 bars) and earns 9.15 of the 13.4 summed gain. The bottom quarter's is -0.12 % (t -1.12) and loses 1.11, though the book still holds 0.24 of its value there.
- **F3:** The losing bars are the falls that come without a volatility burst. Bars with a low 7-day against 30-day volatility and a middling 30-day return have a next-day excess of -0.47 % (t -3.49, 734 bars). Bars with a high ratio gain in every 30-day state: +0.88 % (t 3.49) when the 30-day return is low, +0.23 % when it is middling, +0.64 % (t 3.46) when it is high.
- **F4:** The book's deepest fall comes from the calm-regime bars. In the deepest fall of a book rebuilt from position × next return (187 days), bars with a low ratio lost 13.7 % and bars with a middling ratio lost 15.6 %, while high-ratio bars lost only 1.0 %. Without the low-ratio bars, the rebuilt book's deepest fall shrinks from 28.9 % to 20.5 % and its Calmar rises from 1.11 to 1.85. The rebuilt book sums gains without fees, so its levels sit above the real book's.
- **F5:** The rebound is larger after the coin has already moved far over the month, in either direction. By the coin's 30-day return, the next-day excess is +0.45 % (t 3.18) in the lowest quarter and +0.35 % (t 2.76) in the highest, against +0.00 % and -0.11 % in the two middle quarters. The 7-day return shows the same U-shape: +0.37 % and +0.54 % at its ends, -0.17 % and -0.04 % in its middle.
- **F6:** The idea as a whole is barely large enough for its cost, but its volatility-burst part is large. Its unusual move per case is +0.24 %, only 1.2 times the 0.19 % round trip. The top quarter by volatility ratio carries +0.73 % per bar, about 3.8 times the cost, which matches the earlier finding (F11) that only ideas covering their cost pay.

## Ideas
- `022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d1_fall-rebound-in-volatility-bursts` (from F1, F2, F3, F4, F6): The larger a coin's 1-day fall compared with its 30-day volatility, the higher its return over the next 1 day, the more so the higher its 7-day volatility stands against its 30-day volatility.
- `022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d2_fall-rebound-after-strong-months` (from F3, F5): The larger a coin's 1-day fall compared with its 30-day volatility, the higher its return over the next 1 day, the more so the larger the size of its 30-day return, whether that return was a rise or a fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
