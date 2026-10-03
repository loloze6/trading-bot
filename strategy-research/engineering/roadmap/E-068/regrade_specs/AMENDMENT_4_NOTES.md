# Amendment 4: notes from the Opus review (committed before any gate result)

Written 2026-10-03 while the amendment-4 gate was running and **before any of
its results existed**. These notes correct and complete the wording of
AMENDMENT_4.md. They do not change the method, the gate or the decision rule.

1. **"The code says the same" was too strong.** A8.5.1a's pre-registration
   (AMENDMENTS_01-06.md, A8.5.1a-spec rule 1) and the code *comment* both say
   "48 bars @ 1h ≈ 2 days". The pipeline's *code*
   (`tools/run_protocol.py::_a851a_episode_significance`) does something
   different: it scales `block_size` by timeframe but deliberately passes
   `gap_bars` as a bar count. Amendment 4 follows the pre-registration's stated
   duration, not that code.

2. **Caveat: the horizons are longer than the gap.**
   - On hourly data, A8.5.1a's 48-bar gap was much longer than the 1-bar
     forward return it was built for.
   - On daily data with a 2-day gap, horizons 4-5 are longer than the gap. So
     neighbouring episodes can share forward-return days, which could make
     p-values too small.
   - The calibration gate is the guard against this, but its simulated prices
     have no trend persistence.
   - The report must state this caveat next to any verdict.

3. **Ties at the clip.** In probes, 40-53% of breakout events sit exactly at
   the ±20 clip. Average ranks keep the IC valid, but much of it is then a
   "clipped vs not clipped" contrast. The report must say this next to any
   verdict.

4. **Implementing section 4 ("a failed signal's variants are not graded"):**
   - Variants without a passed gate for their signal are listed as not graded
     and left out of the claim-level combination. They must not mask the
     graded variants' verdicts.
   - "N tests run" is each test on each graded variant.
   - These are code fixes that make the tool do what amendment 4 already says.

5. **Seeds.** The new method's simulations use new seed indices. "Seeds for
   period 20 identical to the earlier gate" holds only for the two older
   methods. The gate design is unchanged.
