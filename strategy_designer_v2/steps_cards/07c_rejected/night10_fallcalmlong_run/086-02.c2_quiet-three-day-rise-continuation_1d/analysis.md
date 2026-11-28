---
line: 7.c no effect
backtest: 086-02.c2_quiet-three-day-rise-continuation_1d
idea tested: 086-02.c2_quiet-three-day-rise-continuation
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4081 USD
---
## Findings
- **F1:** The 3-day version of the tested idea has no effect in falling calm markets, and the problem is not the horizon: 3-day rises split into quartiles of 3-day volume against the prior 20 days do not rank at any horizon. At 5 days the lightest to heaviest quartiles give +4.6 %, −1.4 %, +0.1 % and +0.9 % excess (n 13–14 each). At 10 days the lightest gives −10.1 %. The correlation of 3-day volume with the 5-day excess return is r −0.10 (t −1.1, n 118). This matches step 5's slope t of +0.05 on 184 cases with forecast > 0.
- **F2:** Instead, falling calm bars lag the coin's own drift. Grid cases in the profile earn −0.83 % excess over 5 days (t −1.0, n 146) and −2.7 % over 10 days (t −1.5, n 70), while bars outside the profile earn +0.18 % and +0.55 %. A 3-day rise does not escape this: its 5-day excess by coin runs from −0.5 % (ETH) to +4.6 % (BCH, n 11), and by year from −2.3 % (2019, t −1.8) to +6.8 % (2021, t 3.7), with no steady sign.
- **F3:** On a single up day the tested direction does show at the 5-day horizon. In falling calm markets, the lighter the up day's volume against its prior 20-day average, the larger the 5-day excess return: slope t −2.20 on volume (n 54). The lightest quartile gives +5.4 % (t 1.98) and the other three −1.6 %, −4.8 % and −0.6 %. ETH (t −2.55, n 22) and ZEC (t −2.75, n 11) carry it, and XMR does not (t +0.58). It is absent at 2, 3, 7 and 10 days (t −1.2, −1.7, +0.2, −0.05), so it is a narrow and fragile reading.
- **F4:** The clearest volume effect in falling calm markets is on down days, the mirror of the brief's heavy-volume up day. The heavier a down day's volume against its prior 20-day average, the larger the 5-day excess return: slope t +2.06 (n 67). The heaviest volume tercile gives +2.7 % (t 2.16, n 23), against −3.8 % and −7.1 % for the light and middle terciles. The heaviest tercile also leads at 2 days (−0.3 % against −1.3 % and −2.3 %) and at 10 days (+2.0 % against −4.9 % and −14.2 %).
- **F5:** The down-day effect is strongest after the larger falls. Among down days with a fall larger than the median, heavy volume gives +3.1 % 5-day excess (t 2.68, n 19), against −8.4 % on light volume (t −2.47, n 6). The slope is positive in every year of the explore half: 2018 t 1.35, 2019 t 1.29, 2020 t 0.57, 2021 t 0.12. It is positive in ETH (t 1.95) and ZEC (t 1.76) and flat in BCH and XMR.
- **F6:** Put together as one reading, lightness on up days and heaviness on down days give a 5-day slope t of 3.22 (n 121). It is 1.86 at 2 days and near 0 at 7 days. Both halves are short-lived: a 5-day move per case of a few percent, against a cost of 0.31 % per trade.

## Ideas
- `086-02.c2.c1_quiet-up-day-continuation` (from F3, F1, F6): In a falling, calm market, the lighter a coin's volume on an up day against its prior 20-day average volume, the larger its rise over the next 5 days.
- `086-02.c2.c2_heavy-volume-down-day-absorption` (from F4, F5, F2): In a falling, calm market, the heavier a coin's volume on a down day against its prior 20-day average volume, the larger its rise over the next 5 days, most of all after a larger one-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
