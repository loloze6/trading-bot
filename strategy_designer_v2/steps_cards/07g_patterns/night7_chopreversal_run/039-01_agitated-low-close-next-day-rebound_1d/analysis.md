---
line: 7.g patterns
backtest: 039-01_agitated-low-close-next-day-rebound_1d
idea tested: 039-01_agitated-low-close-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3472 USD
---
## Findings
- **F1:** In agitated bars the close-location effect is concentrated on days whose range is wide against the coin's last 20 days. In the widest third, next-day excess return is +1.40 % (t 4.34, 440 bars) after closes in the lowest third of the range and −1.13 % (t −3.08, 389 bars) after closes in the highest third. In the narrowest third the same spread is only −0.06 % against −0.46 %. The cross term "close location × log relative range" has t 2.83 (3,333 bars, 963 days), against t 1.24 in calm bars.
- **F2:** The book already earns most where ranges are wide. Its mean gain per agitated coin-bar is 9.99 bp in the widest third of relative range, against 2.55 and 2.84 bp in the other two thirds (about 1,110 bars each). Its average position is only slightly larger there: 0.108 against 0.077 and 0.092.
- **F3:** Measured in price terms (close location centred at mid-range × range as a share of the close), the effect is strong in agitated bars: slope 0.266, day-clustered t 4.05, 3,691 bars over 1,051 days. In calm bars it is half as large: slope 0.129, t 2.13.
- **F4:** The close location adds nothing beyond the day's own return in agitated bars. With the day's return in the same regression, the close-location t drops from 3.45 to 0.11. The day's return alone has slope −0.106 (t −2.68, 1,042 days). The brief's claim that the location carries information "beyond the net change" is not supported.
- **F5:** The day's own return reverses the next day, and more strongly in agitated bars. In the bottom fifth of the day's return, next-day excess is +0.91 % (t 3.95, 947 bars) in agitated bars against +0.54 % (t 2.86, 706 bars) in calm bars. In agitated bars the fourth fifth gives −0.75 % (t −3.64, 653 bars).
- **F6:** The effect holds steadily across coins and years and lasts one day only. In agitated bars the correlation of close location with next-day excess return is 0.063 to 0.162 on all six coins and 0.050 to 0.117 in every year 2018 to 2021, rising to 0.104 to 0.205 in each year on wide-range days. Over 3 days (non-overlapping) the quintiles show no monotone pattern: lowest-close quintile +0.64 %, t 1.02.

## Ideas
- `039-01.g1_wide-day-low-close-rebound` (from F1, F2, F6): In an agitated market, the lower a coin closes within its day's high-low range, the larger its rise over the next day, and the more so the wider that day's range is compared with the coin's ranges over the previous 20 days.
- `039-01.g2_price-distance-below-mid-range` (from F3, F1): In an agitated market, the further a coin's close sits below the middle of its day's high-low range, measured as a share of the price, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `039-01.g3_agitated-one-day-return-reversal` (from F4, F5, F6): In an agitated market, the larger a coin's fall over one day, the larger its rise over the next day, and the larger its one-day rise, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
