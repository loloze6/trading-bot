---
line: 7.d confirmed, not profitable
backtest: 032-02.b2.g1.d1_close-location-on-wide-days_1d
idea tested: 032-02.b2.g1.d1_close-location-on-wide-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3783 USD
---
## Findings
- **F1:** The effect lives only on wide days. On the two widest fifths of days (range 0.95 to 1.34 and above 1.34 times the 20-day average), the signal's direction earns +0.87 % (t 4.0, n 663) and +0.91 % (t 3.8, n 697) on the long side the next day. On the two narrowest fifths (range under 0.72 times the average), it earns −0.19 %, −0.04 %, −0.33 % and +0.28 % across both sides, none with |t| above 1.9.
- **F2:** The book trades every day, including the quiet days where there is no effect. It held a position on 100 % of coin-days and turned over 0.55 of the book per bar, so about 0.053 % per bar went to costs (at 0.19 % a round trip) against a gross position gain of 0.124 %. On the narrowest fifth of days its gross gain was −0.007 % per bar, at 0.32 turnover and a 0.15 mean position, so those days only paid fees.
- **F3:** The short side carries almost nothing. Book bars held short earned +0.029 % against +0.237 % for bars held long (3915 against 3325 bars), and the short positions were the larger ones (mean position 0.40 against 0.36).
- **F4:** Shorts lose in a rising coin, which is why the book falls behind holding. After a high close in a coin whose 20-day return is up or flat, the next day earns −0.03 % in the short direction (t −0.31, n 2145). After a high close in a coin whose 20-day return is negative, it earns +0.63 % (t 4.9, n 1780). The book lost in w11 and w17, where holding gained +1.26 % and +0.42 % a day, with book returns of −0.08 % and −0.13 %.
- **F5:** The long side works best in a rising coin. A low close in a coin whose 20-day return is not negative is followed by +0.61 % (t 4.6, n 1424), against +0.17 % (t 1.3, n 1900) in a falling coin.
- **F6:** The 20-day trend alone is weaker than the signal inside it. Averaging the long and short cases gives a rough next-day bias of about +0.28 % after a rising month and about −0.23 % after a falling one, against ±0.6 % when the close location agrees with the trend. The trend is therefore a regime in which the reversal pays, not the effect itself. In the theory, it is the side where forced exits come before a continuation rather than a cascade.
- **F7:** A wide day on its own carries an upward bias, but close location still grades the move within it. Mid-range closes on the widest fifth of days are followed by +0.64 %. Low closes are followed by +1.56 % and high closes by −0.60 %, a spread of 2.16 % against about 0.06 % on the quietest fifth.
- **F8:** For wide-day low closes, the move keeps building on the second day. Over 2 days on a non-overlapping grid, the long side earns +1.87 % (t 3.9, n 338) in the second-widest fifth and +1.22 % (t 2.7, n 362) in the widest, against +0.87 % and +0.91 % over 1 day. Over 3 days the result is mixed (−0.58 % and +1.33 %).

## Ideas
- `032-02.b2.g1.d1.d1_close-location-wide-days-only` (from F1, F2, F7): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 1 day, and the higher the close sits, the more it falls. This holds only on days whose range is wider than the coin's average daily range over the previous 20 days, and the effect grows with how much wider the day was.
- `032-02.b2.g1.d1.d2_close-reversal-with-the-trend` (from F3, F4, F5, F6): The lower a coin's daily close sits within a wide day's high-low range, the more the coin rises over the next 1 day, but only while its 20-day return is up. The higher the close sits, the more it falls over the next 1 day, but only while its 20-day return is down. In both cases the effect grows with how wide the day was against the previous 20 days' average range.
- `032-02.b2.g1.d1.d3_wide-day-low-close-two-days` (from F1, F3, F8): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 2 days, and this rise grows with how wide that day was against the coin's average daily range over the previous 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
