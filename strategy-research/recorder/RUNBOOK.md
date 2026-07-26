# Kraken Forward Recorder — RUNBOOK

Phase 2.4 always-on capture daemon. Build spec:
`strategy-research/docs/session_reports/20260726_recorder_build_spec.md`.

---

## 0. What this records, and the one rule about reading it

Verbatim NDJSON from `wss://ws.kraken.com/v2` for the 19 Kraken breadth pairs
(quote **USD**, not USDT):

| Stream | Channel | Notes |
|---|---|---|
| `book_d10/` | `book`, depth 10, snapshot on subscribe | CRC32 covers exactly the top 10, so the whole captured book is verifiable |
| `trades/` | `trade`, snapshot on subscribe | full public trade feed |
| `meta/` | `status`, `instrument`, subscription replies | `instrument` carries the price/qty precision the CRC32 needs |

> ### The data is RESERVED. Do not read it.
> No stage, prescreen, diagnostic or backtest may read **any** window of
> `trading-bot/local_data/recorded_reserved/` until an explicit,
> separately-committed designation releases it. Registered as
> `kraken_ws_forward_recorder` / `status: reserved_undesignated` in
> `strategy-research/config/campaign_data_policy.yaml`.
>
> This is the only *renewable* source of genuinely unseen out-of-sample the
> campaign has — nobody, including us, has looked at it. Reading a window
> spends that property permanently, for the same reason
> `holdout_failure_is_terminal` exists. Deny by default.

Output is excluded from publication by `.gitignore:34` (`trading-bot/local_data/*/`).

Shards roll **hourly** and closed hours are **zstd-compacted** (§8). Layout:

```
{out}/{stream}/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson       <- the open hour
{out}/{stream}/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson.zst   <- every closed hour
```

`recorder.shard_writer.read_shard` reads both and accepts either spelling, so a
consumer never has to know whether compaction has caught up.

---

## 1. Install

```
python -m pip install -r strategy-research/recorder/requirements.txt
```

All commands below are run **from `strategy-research/`**.

---

## 2. Before trusting any deploy — selftest

Connects, subscribes all 19 pairs, requires a book snapshot **per symbol**
within 30 s. Exits non-zero otherwise.

```
python -m recorder.record_kraken_ws selftest
```

Expected: `snapshots received: 19/19` then `SELFTEST PASS`.
Anything less than 19 names the missing pairs — investigate before starting.

---

## 3. Start

Foreground (Ctrl-C stops cleanly, writing `RECORDER_STOP`):

```
python -m recorder.record_kraken_ws run
```

Supervised (restarts on crash; recommended for always-on):

```
powershell -ExecutionPolicy Bypass -File recorder\supervise.ps1
```

For unattended operation, register `supervise.ps1` in Task Scheduler with
trigger *At startup* and *Restart if the task fails*.

### Flags

| Flag | Default | Effect |
|---|---|---|
| `--book-mode delta\|snapshot` | `delta` | book capture cadence — see §3.2 |
| `--snapshot-interval N` | `5` | seconds between synthesised books (snapshot mode only) |
| `--roll hour\|day` | `hour` | shard roll period |
| `--no-compress` | off | keep closed shards raw (measurement / debugging only) |
| `--compress-level N` | `10` | zstd level |
| `--duration N` | `0` | stop after N seconds (0 = forever) |

---

## 3.1 Compaction — what happens to a closed hour

At the hour boundary each `(stream, symbol)` shard is closed and handed to a
single background thread, which:

1. compresses it to `<hour>.ndjson.zst.part`,
2. **decompresses that and byte-compares it against the source**,
3. renames `.part` -> `.zst` only on success, and only then deletes the raw.

If the comparison fails the raw shard is left exactly where it was, the partial
archive is deleted, and the failure is written to the coverage journal as a
`RECONNECT_ATTEMPT` record with `attempt: -2` and a `COMPACTION FAILED` note.
**It is not retried.** A shard that fails verification is evidence of a real
fault (bad block, truncated write, compressor bug); retrying it in place is how
that fault turns into data loss. Investigate the shard by hand.

Why hourly rather than the nightly roll-up the build spec deferred: raw capture
measures ~100.5 kB/s, i.e. ~8.7 GB/day, so a nightly roll leaves up to a full
day of uncompressed data on disk before it compresses anything. Hourly caps the
raw working set near ~360 MB.

Three further properties worth knowing:

* **The open hour is never compacted, including on a clean stop.** A recorder
  restarted inside the same hour appends to the shard it left. Compacting at
  `close()` would strand that shard behind an archive.
* **Startup sweeps orphans.** A shard left raw by a `kill -9` in a previous hour
  is compacted at the next `RECORDER_START`, before capture begins, so a
  verification failure aborts the boot rather than surfacing an hour later.
* **Compaction never runs on the receive path.** An hour of DOGE book deltas is
  ~100 MB; compressing it inline would stall the reader for seconds and trip the
  10 s heartbeat watchdog (§5).
* **Only shards matching the current roll scheme are eligible.** The tree still
  contains daily-named shards (`2026-07-26.ndjson`) from the first deployment.
  An hourly sweep skips them: they are reserved, already-attested captures, and
  rewriting them as a side effect of an unrelated startup would be a silent
  modification of reserved data. Unrecognised shard names are left strictly
  alone rather than compacted on a guess.

Compression is not free of policy: a `.zst` shard is only as good as its
verification, which is why the byte-compare is unconditional and streamed rather
than a size or checksum check.

---

## 3.2 Cadence — `--book-mode`, and why the default is not negotiable

| Mode | What lands on disk | Lossless? |
|---|---|---|
| `delta` (**default**) | every venue book frame, verbatim | yes |
| `snapshot` | one synthesised full depth-10 book per `--snapshot-interval` seconds | **no** |

`snapshot` folds the venue's deltas into a maintained local book and writes only
the book, on a fixed cadence. Trades and meta are **untouched in both modes** —
the full public trade feed is always captured verbatim.

**What snapshot mode destroys, permanently:** everything that happened between
two emissions. Queue position, the ordering of a cancel against a trade,
sub-second book pressure — none of it is recoverable afterwards, because the
deltas were never written. There is no reprocessing path back to delta fidelity.
It buys disk and nothing else.

**What it preserves, deliberately:** the venue's exact decimal strings (never
routed through `float`), and CRC32 verifiability. An emitted snapshot carries the
`checksum` and `timestamp` of the last venue frame folded into it, and because
emission happens between applications rather than during one, that checksum
covers exactly the book emitted. `kraken_crc.verify_book_frame` therefore
verifies a synthesised snapshot as readily as a venue one — measured 152/152
against live frames at build time. Snapshot-mode data is lossy in time, not
unverified.

Synthesised frames are marked, always: `"synthetic": true` in the payload and
`"synth": "book_snapshot"` in the envelope. A capture is a claim about what the
venue sent, and a reconstruction indistinguishable from a verbatim frame would
corrupt that claim for every future consumer.

A frame is emitted every interval **even when nothing moved**, carrying
`updates_applied: 0`. That is snapshot mode's COVERED-AND-QUIET (§7); suppressing
it would make "quiet" and "not captured" indistinguishable again.

Storage cost per mode is measured in
`strategy-research/docs/session_reports/20260726_recorder_cadence_ladder.md`.
**Choosing a cadence is an operator decision.** The default is `delta` and no
code path changes it.

---

## 4. Health check — THE command

Run this. It is the whole check.

```
python -m recorder.liveness
```

**It sleeps ~70 s by design** (it needs two size readings) and exits `0` only
when all three of these hold:

1. **GROWTH** — new bytes were written between the two readings. This is the
   sum of per-file size *increases* plus the full size of files that appeared,
   never the difference of two totals: the hourly roll starts a fresh shard
   while the old one stops growing, and compaction replaces a ~360 MB raw shard
   with a ~40 MB archive, so the total legitimately falls once an hour. A
   shrinking total is expected; an absence of new bytes is the failure.
2. **FRESH** — newest `recv_ts` on disk is < 30 s old, and the newest journal
   record is recent.
3. **COVERAGE** — the journal shows an open coverage interval right now, the
   newest `HEARTBEAT_ROLLUP` is < 150 s old, carries a non-zero heartbeat
   count, and saw all 19 symbols.

Last line is `HEALTHY` or `UNHEALTHY`; exit code matches. Useful flags:
`--window 70` (seconds between readings), `--expect-symbols 19`,
`--max-staleness 30`, `--out <dir>`.

### Why size alone is not the check

Kraken emits a heartbeat ~1/s whenever no other channel update is flowing. A
healthy socket subscribed to 19 pairs therefore **cannot** produce a silent
minute. So:

> **A 0-byte or non-growing shard is a FAILURE, never a quiet market.**

Size can also grow while coverage is broken — one pair silently dropping out of
the subscription still leaves 18 pairs writing hard. That is why check 3 counts
symbols in the journal rather than trusting the byte counter.

---

## 5. What failure looks like

| Symptom | Liveness output | Meaning | Action |
|---|---|---|---|
| Process gone | `no shard files` / journal last record is `RECORDER_STOP` | clean stop | restart (§3) |
| Half-open socket | `shards not growing`, journal tail is old | TCP alive, no data — **the defect this design targets** | the watchdog should have caught it in 10 s; if it did not, kill and restart, then report |
| One pair dropped | `last rollup saw 18 symbols, expected 19` | partial coverage; shards still growing | restart; the journal already bounds the affected span |
| Venue maintenance | journal `STATUS_CHANGE` with `system=maintenance` | venue-side, not us | wait; reconnect backoff handles it |
| Repeated reconnects | many `RECONNECT_ATTEMPT` | flapping link | check the network **before** restarting in a loop — Cloudflare bans ~150 connect attempts per rolling 10 min per IP |
| `torn_tail: true` on `RECORDER_START` | — | predecessor killed mid-write | benign; the torn line is skipped and reported, not silently repaired |

**Silence in the log is never evidence of health.** The recorder logs almost
nothing by design; the journal is the record. Judge by §4, not by the log.

---

## 6. Stop

Ctrl-C in the foreground, or stop the Task Scheduler task. Either way the
`finally` block writes `RECORDER_STOP`, which closes every open coverage
interval. A `kill -9` skips it — that is not data loss, but it does mean the
next `RECORDER_START` records `prev_clean_shutdown: false` and the interval is
closed at the last record the dead process actually attested, leaving the
downtime visibly UNCAPTURED. That is the intended behaviour.

---

## 7. Coverage — what a consumer must do

The venue publishes **no sequence numbers on the book channel**. Nothing in the
data distinguishes "no activity" from "not captured". Coverage is therefore
attested only by `_session.ndjson`, and consumers must ask it:

```python
from recorder.journal import assert_covered      # raises CoverageGapError
assert_covered(journal_path, "BTC/USD", "book", start, end)
```

`assert_covered` **raises** on any unattested instant. It does not warn and it
does not fill — this is `FetchGapError`'s doctrine
(`trading-bot/data/fetchers/base_fetcher.py:42-61`) moved to the read boundary,
because an event stream has no merge step to guard.

Three coverage states, not two:

* **COVERED-AND-QUIET** — inside an attested interval, zero frames, heartbeat
  alive. Real market silence. Usable.
* **UNCAPTURED** — outside every attested interval. Never usable, never
  interpolated.
* **DEGRADED** — `[CHECKSUM_MISMATCH → resnapshot]`. Reserved; produced once
  live CRC32 verification lands (§8).

---

## 8. Known deferrals

* **Live CRC32 verification** — deferred out of MVP (~3 h: needs a maintained
  local book). Recoverable: `checksum` is captured verbatim and
  `recorder.kraken_crc.verify_book_frame` replays it offline. Verified working
  against 19/19 live snapshots at build time. **This is the deferral that
  genuinely weakens §7** — until it lands, a book desync shows up as a silent
  data-quality defect rather than a `DEGRADED` interval. First thing to add.
* ~~**zstd at write**~~ — **LANDED**, as an hourly (not nightly) verified roll.
  See §3.1. Measured ratios per mode are in the cadence ladder report.
* **Trades → OHLCV** — not capture work; do it when a consumer needs it.

## 9. Not available at this venue

**Kraken publishes no public liquidation feed** — spot or futures. The only
`liquidated` field is on the private, authenticated `executions` channel, which
is own-account only. Roadmap 2.4's "live liquidation events" is **INFEASIBLE
here, not deferred**; it requires a different venue (e.g. Binance `forceOrder`)
and that is a separate decision.
