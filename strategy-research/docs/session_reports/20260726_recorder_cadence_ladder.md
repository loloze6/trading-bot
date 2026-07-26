# Recorder cadence ladder — measured storage rates

**Date:** 2026-07-26
**Scope:** storage sizing only. No research decision, no verdict, no change to the
recorder's default mode (`delta` remains the default everywhere).
**Raw measurements:** `data/20260726_ladder_output.txt`, `data/20260726_ladder_results.json`
(copied out of `%TEMP%\r1_measure` and `%TEMP%\r1_ladder` so they survive a TEMP clear).

---

## 1. Authoritative base rate

**101,392 B/s** — Kraken WS v2, L2-d10 + trades, 19 pairs, `delta` mode.

Derived from the reserved capture at
`trading-bot/local_data/recorded_reserved/kraken_ws_v2/`:

| Quantity | Value |
|---|---|
| Shard bytes (39 `.ndjson`, excl. journal) | 60,905,054 |
| Coverage journal bytes (`_session.ndjson`) | 12,605 |
| **Total bytes on disk** | **60,917,659** |
| Journal-attested span | **600.811 s** |
| **Base rate** | **101,392.4 B/s** |
| Projection | 8.760 GB/day raw · 3,197 GB/12mo raw |

The 600.811 s denominator is the recorder's own journal, not a stopwatch:

- `RECORDER_START` @ `2026-07-26T02:05:37.832563Z` (jseq 1)
- last `HEARTBEAT_ROLLUP` @ `2026-07-26T02:15:38.643757Z` (jseq 52)
- difference = **600.811 s**

Numerator and denominator are matched on purpose: *every byte the recorder wrote*
(shards **and** journal) over *the whole time the process was running*. That is the
quantity that governs disk provisioning.

### Two other spans exist — don't mix them with this numerator

| Span | Definition | Rate vs. the matching numerator |
|---|---|---|
| 600.811 s | `RECORDER_START` → last journal record | 101,392.4 B/s (total incl. journal) — **authoritative** |
| 598.548 s | first `SUBSCRIBE_ACK` → last attested instant (coverage-interval span) | 101,754.6 B/s (shards only) |
| — | as above, excluding the 751,579-byte subscription snapshot burst | 100,498.9 B/s |

All 38 (symbol, channel) coverage intervals closed as `OPEN_TAIL` — there is no
`RECORDER_STOP` in this journal, so coverage is attested only to the last heartbeat.
The 2.263 s difference between the two spans is recorder start-up plus WS connect
(`RECORDER_START` → `WS_CONNECT` = 2.230 s).

Frame accounting for this capture: **177,955** = 177,903 shard frames + 52 journal
records.

### Retired figure: 100,754 B/s

The previously circulated **100,754 B/s has no derivable denominator and is retired.**
No span present in the journal reproduces it against any numerator on disk. The
denominators it would imply are:

| Numerator | Implied span at 100,754 B/s | Matches a journal instant? |
|---|---|---|
| 60,905,054 (shards) | 604.49 s | no |
| 60,917,659 (shards + journal) | 604.62 s | no |
| 60,153,475 (shards, burst excluded) | 596.98 s | no |

It happens to land within ~1 % of the correct rate, which is why it survived as long
as it did. Use 101,392 B/s.

---

## 2. The four-rung cadence ladder

Four live captures, one per mode, `DURATION = 240 s` each, compaction **off**, same
19-pair subscription. Compressed figures are a **measured** zstd level-10 ratio on the
steady-state slice, not an assumed one.

| Mode | Steady span (s) | Raw B/s | Compressed B/s | Measured zstd ratio | GB/day (comp) | GB/12mo (comp) | vs. delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| `delta` | 208.7 | 108,007 | 9,444 | 11.44× | 0.816 | 297.8 | 1.000× |
| `snapshot` @ 1 s | 208.7 | 20,576 | 1,335 | 15.41× | 0.115 | 42.1 | 0.141× |
| `snapshot` @ 5 s | 206.3 | 4,358 | 476 | 9.16× | 0.041 | 15.0 | 0.050× |
| `snapshot` @ 10 s | 207.8 | 2,245 | 301 | 7.45× | 0.026 | 9.5 | 0.032× |

GB/day = rate × 86,400 / 1e9; GB/12mo = GB/day × 365.

Note the compression ratio is **not** monotonic in cadence. It peaks at snapshot @ 1 s
(15.41×) and falls to 7.45× at 10 s. Sparser snapshots carry less inter-frame
redundancy for zstd to exploit, and the fixed-size trades stream becomes a larger share
of a shrinking total — so halving the frame rate does **not** halve the compressed
bytes. Any projection that assumes a constant ratio across rungs will be wrong; these
ratios are measured per rung for exactly that reason.

### Reconciling the delta rung with the base rate

The delta rung reads 108,007 B/s raw against the authoritative 101,392 B/s — **+6.5 %**.
These are not in conflict; they measure different windows:

- base rate: 600.811 s, whole process, all bytes including journal;
- delta rung: a 208.7 s steady-state slice of a separate 240 s capture, shards only.

Market activity differs between the two windows. **For sizing, use the base rate.**
Applying the measured 11.44× delta ratio to it gives the figure to provision against:

> 8.760 GB/day raw ÷ 11.44 = **0.766 GB/day compressed ≈ 280 GB/12mo** for `delta`.

### 30 s burst-skip methodology

On subscribe, Kraken sends a full book snapshot per (pair, channel). That burst is a
one-off cost of connecting and would inflate a short capture's steady-state rate, so
each rung is measured as follows (`ladder.py`):

1. Capture for 240 s with `--no-compress` into a throwaway directory.
2. Find `t_first` = earliest `recv_ts` across all shards; set `cutoff = t_first + 30 s`
   (`BURST_SKIP_S = 30.0`).
3. Discard every frame with `recv_ts < cutoff`.
4. Measure raw bytes over the surviving frames; span = `last_recv_ts − cutoff`, so the
   denominator covers the same window as the numerator (a quiet tail is charged, not
   silently dropped).
5. zstd-compress the retained slice at level 10 per stream → measured ratio.

Scale of what is being excluded: in the 600.811 s reserved capture the subscription
burst is **39 frames / 751,579 bytes = 1.23 %** of all shard bytes — small over ten
minutes, but ~6 % of a 240 s window's book bytes, hence the skip.

Disk guard: each rung aborts if free space on C: drops below 5 GB. Free space moved
17.785 → 17.782 GB across the whole ladder; all captures were deleted by `cleanup.py`.

---

## 3. Per-pair book bytes (`book_d10`, 600.811 s reserved capture)

Book total 60,013,467 B across 177,486 frames, 19 pairs, 1 subscription snapshot each.

| Pair | Bytes | Msgs | % of book |
|---|---:|---:|---:|
| DOGEUSD | 17,652,319 | 50,016 | 29.41 % |
| ADAUSD | 6,088,700 | 18,001 | 10.15 % |
| ZECUSD | 4,809,692 | 13,991 | 8.01 % |
| ETHUSD | 3,904,304 | 11,517 | 6.51 % |
| TAOUSD | 3,487,110 | 10,487 | 5.81 % |
| LINKUSD | 2,889,202 | 8,500 | 4.81 % |
| XMRUSD | 2,785,229 | 8,204 | 4.64 % |
| XRPUSD | 2,471,414 | 7,429 | 4.12 % |
| ONDOUSD | 2,257,310 | 6,900 | 3.76 % |
| BTCUSD | 2,222,396 | 6,783 | 3.70 % |
| AVAXUSD | 1,914,517 | 5,928 | 3.19 % |
| SOLUSD | 1,537,872 | 4,938 | 2.56 % |
| TRXUSD | 1,433,591 | 4,142 | 2.39 % |
| UNIUSD | 1,329,506 | 4,108 | 2.22 % |
| NEARUSD | 1,210,455 | 3,734 | 2.02 % |
| INJUSD | 1,171,813 | 3,744 | 1.95 % |
| AAVEUSD | 992,902 | 3,150 | 1.65 % |
| SUIUSD | 928,088 | 2,952 | 1.55 % |
| LTCUSD | 927,047 | 2,962 | 1.54 % |

Per-stream totals for the same capture:

| Stream | Bytes | Messages | of which snapshot |
|---|---:|---:|---:|
| `book_d10` | 60,013,467 | 177,486 | 18,676 B / 19 frames |
| `meta` | 601,213 | 41 | 588,857 B / 1 frame |
| `trades` | 290,374 | 376 | 144,046 B / 19 frames |
| **TOTAL** | **60,905,054** | **177,903** | 751,579 B / 39 frames |

The distribution is heavily skewed: **DOGEUSD alone is 29.4 % of all book bytes**, and
the top three pairs are 47.6 %. Cost is driven by tick-dense low-priced pairs, not by
notional. This is recorded as a measurement only — no pair is being dropped, and no
recommendation follows from it here.

---

## 4. What this does and does not settle

- Settled: the byte rates above, measured, with matched numerators and denominators.
- Settled: 100,754 B/s is retired in favour of 101,392 B/s.
- **Not** settled and out of scope here: whether snapshot cadence is acceptable for any
  downstream use. The ladder prices the options; it does not choose one. The recorder's
  default is unchanged (`delta`).
