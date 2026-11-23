---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close return, measured in its usual daily moves over the past 20 days, is followed over the next 3 days (Monday to Wednesday) by a move against the coin's normal drift in the opposite direction. The larger the Sunday move, the larger the reversal, both after Sunday rises and after Sunday falls.
Consequence: Lean against Sunday's move in either direction for the first three weekdays, fading Sunday rises as well as buying Sunday falls, and lean harder the larger the Sunday move.
Why:
- F1: On Sunday bars the coin's next 3-day return against its drift, in usual 3-day moves, falls with the Sunday return in usual daily moves (slope -0.106, t -6.2, 4320 Sunday cases 7 bars apart), while every other weekday shows no reversal or a continuation (Monday -0.019 t -1.35, Tuesday -0.006 t -0.37, Wednesday +0.031 t 2.30, Thursday -0.011 t -0.83, Friday +0.042 t 3.36, Saturday +0.038 t 2.13).
- F2: The Sunday reversal is graded and works on both sides of zero, with moderate moves. The next 3-day excess return, in usual 3-day moves, is +0.27 after Sunday z in (-1.5,-1] (n 232), +0.16 in (-1,-0.5] (n 691), +0.06 in (-0.5,0] (n 1066), -0.10 in (0,0.5] (n 1040), -0.10 in (0.5,1] (n 637) and -0.16 in (1,1.5] (n 284). So Sunday rises are faded as much as Sunday falls rebound, and the tested idea is long-only and leaves that side out.
- F4: Only Sunday's own day reverses. The two-day Saturday-to-Sunday return in usual moves has no slope on the next 3 days (-0.014, t -0.76, n 4320), and the Saturday bar's move continues (+0.038, t 2.13).
