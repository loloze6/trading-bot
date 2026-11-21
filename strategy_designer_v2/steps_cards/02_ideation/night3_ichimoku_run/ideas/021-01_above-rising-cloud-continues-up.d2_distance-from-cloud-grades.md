---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 26 days is larger the farther its daily close stands above the top of its Ichimoku cloud, and smaller the farther it stands below it. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.
Consequence: A trader would lean long in proportion to how far a coin trades above its cloud, and lean away from coins trading below it.
Why:
- F6: The close's signed distance from the cloud top grades the move over all grid bars. Its quintiles of 28 to 29 cases (mean distance −37 %, −18 %, −4 %, +7 %, +36 %) give excess returns of −0.8 %, −10.3 %, +2.1 %, +10.5 % and +12.8 %. Inside the active cases alone the same distance does not grade (rho −0.14).
- F3: The idea's situation does separate. On the non-overlapping 26-day grid, the 149 cases above a rising cloud return +8.6 % (excess +4.8 %, t of the raw return 2.30). The 427 other grid cases return +2.5 % (excess −1.7 %).
- F7: The Calmar fails on one long fall. The book's deepest fall is 60 %, over 702 days from window 15 to window 21, while holding the coins lost only 7.8 % over the same stretch, with a mean position of 0.28. In window 16 the book lost 27 % while the coins rose 36 %. In window 18 the book lost 23 % while the coins fell 22 %. The book was long in rises that reversed, and these losses were not caused by the coins' own fall.
