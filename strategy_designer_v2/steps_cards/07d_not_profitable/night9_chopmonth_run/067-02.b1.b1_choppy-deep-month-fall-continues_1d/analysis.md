---
line: 7.d confirmed, not profitable
backtest: 067-02.b1.b1_choppy-deep-month-fall-continues_1d
idea tested: 067-02.b1.b1_choppy-deep-month-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4314 USD
---
## Findings
- **F1:** The idea's move lives almost entirely in the deepest monthly falls. On the 7-day grid in a choppy market, falls beyond 30 % and falls of 20 to 30 % were followed by raw 7-day returns of -9.27 % (t -2.16, 12 cases on 8 days) and -7.20 % (t -3.46, 25 cases on 16 days). Falls of 10 to 20 % and of 0 to 5 % were followed by -0.56 % (t -0.18, 23 cases) and +0.75 % (t 0.41, 34 cases). The book shorts every fall, so most of its shorts carry a total move near zero, below the 0.22 % cost of a trade.
- **F2:** The gain fails because the shorts fight the coins' upward drift. The unusual move is +1.13 % per case, but the drift in the short's direction is -1.13 %, leaving a total of -0.01 %. The 594 short trades lost 2.40 % net on average (median -2.38 %).
- **F3:** The book loses in the windows where the coins rose and gains where they fell, which is why it fails with one window left out. In w10, w11, w8 and w17 the summed coin daily returns were +67 %, +229 %, +38 % and +39 %, and the book's summed daily returns were -8.9 %, -3.9 %, -5.0 % and -4.5 %. In w14, w9 and w7 the coins' sums were -52 %, -30 % and -58 %, and the book's were +6.5 %, +8.9 % and +1.0 %.
- **F4:** Inside the choppy market, monthly falls continue only when the coin is agitated (its 30-day swing above its median; the record's window median, as a stand-in for the profile's past-year median).
- **F5:** Agitation alone is not the effect, though it carries part of it, so it can only enter as the idea's profile. Agitated choppy bars after a monthly rise (no signal) were followed by -3.49 % raw (t -1.17, 16 cases on 15 days), against -6.52 % (t -3.61) when agitation and a fall hold together.
- **F6:** The deep-fall continuation persists over a longer horizon, but on few cases. Over 14 days, falls of 20 to 30 % were followed by -7.45 % raw (excess -14.2 %, t -3.46, 10 cases on 7 days), and over 21 days by -18.3 % (3 cases on 2 days). Over 14 days the shallow falls of 0 to 5 % gave +16.1 % (t 1.35, 15 cases on 11 days).
- **F7:** The same table shows the brief's opposite side continuing in calm choppy markets. Calm choppy monthly rises were followed by +5.09 % raw over 7 days (t 3.45, 88 cases on 38 days). Rises of 5 to 20 % were followed by +4.25 % and +6.27 % (t 1.86 and 2.19).

## Ideas
- `067-02.b1.b1.d1_choppy-deepest-month-falls-continue` (from F1, F2, F6): In a choppy market, the further a coin's close sits below its close of 30 days earlier, measured as a plain percent of that earlier close, the more it falls over the next 7 days, with the decline growing faster than the depth so that the falls deepest among the month's moves carry nearly all of it and shallow falls carry almost none.
- `067-02.b1.b1.d2_agitated-choppy-month-fall-continues` (from F4, F5, F3): In a choppy, agitated market, the further a coin's close sits below its close of 30 days earlier, measured as a plain percent of that earlier close, the more it falls over the next 7 days.
- `067-02.b1.b1.d3_calm-choppy-month-rise-continues` (from F7, F2, F3): In a choppy, calm market, the further a coin's close sits above its close of 30 days earlier, measured as a plain percent of that earlier close, the more it rises over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
