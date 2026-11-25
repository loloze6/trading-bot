---
line: 7.g patterns
backtest: 060-01_falling-agitated-high-close-fade_1d
idea tested: 060-01_falling-agitated-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4271 USD
---
## Findings
- **F1:** In falling agitated bars, a close in the top third of the day's range fades much more on a wide day than on a narrow one. When the day's range is in the top 40 % of the coin's own range relative to its last 20 days, the next day is −1.82 % against the coin's mean (t −3.20, 126 cases). When the range is narrower, it is −0.35 % (t −1.24, 302 cases). The wide-day fade is about 10 times the 0.19 % cost of a trade, while the tested idea's total move per case is 0.16 %.
- **F2:** In falling agitated bars, the next-day fall follows the up day itself, not the close location. Up days with a close in the top third give −0.93 % (t −3.43, n 375), and up days closing lower give −1.05 % (t −2.54, n 238). Down days closing in the top third give +0.25 % (n 53). So the close location adds little once the day's direction is known.
- **F3:** In falling agitated bars, the next-day move is not graded by close location. The 0.8–1.0 band gives −0.49 % (t −1.34, n 231), weaker than the 0.6–0.8 band at −0.84 % (t −2.46, n 270). The lowest band, 0–0.2, rebounds +2.17 % (t 4.97, n 243). The tested gradient comes mostly from that low-close rebound, not from a growing fade toward the high.
- **F4:** The book loses where it is still short after low closes. Its per-bar gain is −0.15 % (t −3.5, n 209) after closes in the 0–0.2 band and −0.14 % (t −2.4, n 301) in the 0.2–0.4 band. It earns +0.37 % (t 2.29, n 270) only in the 0.6–0.8 band, which leaves its mean on days in a position at 0.001 %.
- **F5:** Outside falling agitated, high closes fade only weakly and not where the brief says. Across non-falling-agitated bars, the 0.8–1.0 band gives −0.35 % (t −2.56, n 1558). In bars with a rising 60-day trend, every close band is slightly positive (+0.15 % to +0.44 %, all t < 1.7).
- **F6:** Other patterns stood out but are already held. In falling agitated bars, the largest down days rebound +2.04 % the next day (t 6.21, n 350), and wide low-close days rebound +1.96 % (t 4.18, n 252). Both are already in the profile map's falling agitated long cell (038-01, 047-01, 039-02, 045-01). The Thursday and Friday gains across all bars (+0.41 %, t 2.80; +0.38 %, t 2.74) repeat the held late-week idea 045-01. None of these is a discovery.

## Ideas
- `060-01.g1_wide-day-high-close-fade` (from F1, F3, F5): In a falling, agitated market, a coin that closes near the top of a day whose high-low range is wide against its ranges of the last 20 days falls over the next day. The wider that day's range against its recent ranges, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
