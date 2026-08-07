# CORRECTION NOTICE — p1b_fetch_manifest.md, 2026-07-15

Two corrections applied to the "After (post-backfill)" table and the
"Gap report" section, both concerning `BTCUSDT_funding_8h.csv`:

1. **Row count**: 7,467 → **7,468**.
2. **Gap report prose**: "4 gaps > 12h ... spread across 2021/2022/2023/2026"
   → **"3 gaps > 12h ... in 2022/2023/2026"** (the original text's gap
   count AND its year list were both wrong — there is no 2021 gap in the
   real file, and only three gaps exist, not four).

## How found and verified (forensics on the real file, read-only)

`BTCUSDT_funding_8h.csv` and `ETHUSDT_funding_8h.csv` were read directly
(`trading-bot/local_data/`, not the strategy-research repo — the manifest
documents a fetch into this location). Commands and results:

```
wc -l BTCUSDT_funding_8h.csv   ->  7469 total lines (incl. header) -> 7468 data rows
wc -l ETHUSDT_funding_8h.csv   ->  7235 total lines (incl. header) -> 7234 data rows
```

ETH's data-row count (7,234) already matches the manifest's existing,
unflagged figure — used as a control to confirm the counting method
before trusting it for BTC.

Distinct-timestamp check (Python, `csv` + `datetime`, first/last rows and
every consecutive gap != 8h enumerated):

```
BTC: data rows=7468, distinct timestamps=7468, duplicated timestamps=[]
     first=2019-09-10 08:00:00, last=2026-07-05 08:00:00
     gaps != 8h (3 total):
       2022-06-06 08:00:00.017 -> 2022-06-07 00:00:00.000  (16.0h)
       2023-05-06 00:00:00.009 -> 2023-05-06 16:00:00.000  (16.0h)
       2026-01-27 00:00:00.002 -> 2026-01-27 16:00:00.000  (16.0h)

ETH: data rows=7234, distinct timestamps=7234, duplicated timestamps=[]
     first=2019-11-27 08:00:00, last=2026-07-05 08:00:00
     gaps != 8h (3 total):
       2020-10-25 08:00:00.014 -> 2020-10-26 00:00:00.004  (16.0h)
       2022-08-23 08:00:00.021 -> 2022-08-24 00:00:00.017  (16.0h)
       2026-01-27 00:00:00.002 -> 2026-01-27 16:00:00.000  (16.0h)
```

No duplicated timestamps in either file — the "distinct timestamps"
branch of the decision rule applies (not the "duplicate" branch).

**Reconciliation identity** (theoretical row count at a perfect 8h
cadence, from each symbol's stated start through the shared last
timestamp `2026-07-05 08:00:00`, minus one missed publication per >12h
gap, should equal the file's actual distinct-timestamp count):

- BTC: theoretical 7,471 (start 2019-09-10 08:00, end 2026-07-05 08:00,
  8h cadence) − 3 missed publications = **7,468** = actual distinct count. ✓
- ETH: theoretical 7,237 (start 2019-11-27 08:00, same end) − 3 missed
  publications = **7,234** = actual distinct count (and the manifest's
  existing, correct figure). ✓

The manifest's original "4 gaps"/"2021/2022/2023/2026" claim for BTC was
the actual defect: it does not reconcile against the real file under the
same identity that exactly reproduces ETH's own (correct, unflagged)
figures. The row-count fix (7,467→7,468) and the gap-report fix
(4→3 gaps, dropping the nonexistent 2021 entry) are the same underlying
correction, not two independent ones.
