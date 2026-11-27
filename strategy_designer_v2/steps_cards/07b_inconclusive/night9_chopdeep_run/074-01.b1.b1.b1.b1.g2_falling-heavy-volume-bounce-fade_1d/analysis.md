---
line: 7.b inconclusive
backtest: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3895 USD
---
## Findings
- **F1:** In folds B and C, the tested cases split sharply by agitation, with agitation read as the 30-day swing above its running median. In agitated markets the 293 cases where agitation could be read give a short-direction unusual next-day move of +2.21 % (t 2.68, 139 cases on 69 days). In calm markets they give +0.19 % (t 0.35, 154 cases on 82 days), so the inconclusive overall t of 1.74 (+0.60 %, 1119 cases) mixes a clear agitated effect with a null calm one.
- **F2:** The same split holds for every falling-market up day, which shows the fade belongs to up days in agitated falling markets. Agitated up days give +1.15 % (t 2.46, 550 cases) against +0.09 % (t 0.27, 771 cases) for calm ones. All falling-market days split by agitation show nothing like it (agitated +0.03 %, t 0.08; calm +0.27 %, t 1.10).
- **F3:** The fade is in the next day only. On the exploration folds' 470 cases the short-direction unusual move is +0.64 % at 1 day (t 1.50), -0.10 % at 2 days (t -0.18), +0.43 % at 3 days (t 0.60) and +1.00 % at 5 days (t 1.23).
- **F4:** Within the cases the fade grows roughly with the volume excess, though weakly. The unusual move by quartile of the volume ratio is +0.73 %, +0.25 %, +1.06 % and +1.55 % (top quartile t 1.73), and by quartile of |forecast| it is +0.60 %, +0.20 %, +0.52 % and +1.25 %. The correlation of the volume ratio with the next-day move is only 0.09.
- **F5:** The effect is tied to the falling market, as the brief says. Wide, heavy-volume up days outside the falling profile show no fade: -0.03 % (t -0.09, 986 cases on 427 days). Inside it they show +0.77 % (t 1.59, 418 cases).
- **F6:** The test already used every fold and coin available, so more data cannot settle the result. The exploration folds alone give only t 1.50 over 470 cases. Coins also disagree: ETH gives +1.97 % (t 3.25), while LINK gives -1.74 % (t -1.65) and XRP -0.60 % (t -0.45).

## Ideas
- `074-01.b1.b1.b1.b1.g2.b1_agitated-falling-volume-bounce-fade` (from F1, F2, F3, F4, F5, F6): In a falling, agitated market, a wide up day traded on heavy volume against the coin's 20-day average volume is followed by a fall over the next day. The heavier that day's volume against its 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
