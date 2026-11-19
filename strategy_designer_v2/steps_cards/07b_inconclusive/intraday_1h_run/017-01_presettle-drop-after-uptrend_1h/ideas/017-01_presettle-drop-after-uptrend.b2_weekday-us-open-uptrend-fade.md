---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: On weekdays, for a coin with a strong 3-day run up, the return over the 2 hours after the 13:00 UTC close is negative, and the stronger the 3-day rise, the larger that decline.
Consequence: Around the US session open on weekdays, a trader would fade a coin's 3-day rise in proportion to its size, whatever the funding clock.
Why:
- F5: An equally large drop after a rise appears at hours with no settlement, which points to a session effect rather than funding: the 2 hours from the 13:00 UTC close fall -8.4 bp (t -4.85) and those from the 02:00 close fall -7.2 bp (t -4.90). The 13:00 slope on the 3-day rise has t -9.56 on weekdays but only -0.44 on weekends (n 4,835), even though funding is paid every day.
- F6: The 13:00 UTC drop after a rise is broad: its slope is negative in all six coins (t -1.01 to -7.73), and its mean after a rise is negative in 7 of 8 years (-7.4 to -15.2 bp; only 2020 is +11.2 bp).
