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

### THE OPERATOR LAUNCH COMMAND

This is the supervised, snapshot-cadence, guard-armed capture registered as
`kraken_ws_forward_recorder.capture_configuration` in `campaign_data_policy.yaml`.
Run it from `strategy-research/`:

```
powershell -ExecutionPolicy Bypass -File recorder\supervise.ps1 -BookMode snapshot -SnapshotInterval 1.0 -MinFreeGb 5.0
```

The cadence and the floor are passed **explicitly**. The recorder's compiled-in
default is still `--book-mode delta`, and no code path changes it — the registry
declares intent, the command line sets it (§3.2).

Foreground, unsupervised (Ctrl-C stops cleanly, writing `RECORDER_STOP`):

```
python -m recorder.record_kraken_ws run --book-mode snapshot --snapshot-interval 1.0 --min-free-gb 5.0
```

For unattended operation, register the supervised command in Task Scheduler with
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
| **`--min-free-gb N`** | `5.0` | **free-space floor, decimal GB — §3.3** |
| `--disk-check-interval N` | `30` | seconds between free-space checks |
| `--log-file PATH` | — | append operational logging here as well as stderr |

Supervisor parameters: `-MinFreeGb`, `-BookMode`, `-SnapshotInterval`,
`-Duration`, `-Out`, `-LogFile`, `-MaxRestarts` (default 20),
`-RestartWindowMinutes` (60), `-BackoffInitialSeconds` (5),
`-BackoffMaxSeconds` (300), `-HealthyRunSeconds` (600).

---

## 3.3 The disk guard, and what `DISK_GUARD_ABORT` looks like

The recorder enforces its own free-space floor — **on a timer, for the whole
run**, not only at startup. A startup-only check answers the wrong question: the
disk is not full when a twelve-month capture begins, it becomes full some weeks
in, possibly because of something else entirely on the same volume.

On breach the ordering is fixed: **flush and fsync the open shards, then attest,
then exit.** Attesting first would have the journal claiming coverage for data
that is not yet durable.

**Free space that cannot be determined is a breach.** An unmeasurable disk is
the state in which continuing to write is least defensible, and a guard that
fails open is not a guard.

The stop lands in the coverage journal as its own record type, so it can never
be confused with a crash or with an operator's Ctrl-C:

```json
{"jseq":8412,"run_id":"...","ts":"2026-07-27T04:11:09.882431Z","mono":57312.4,
 "type":"DISK_GUARD_ABORT","path":"...\\kraken_ws_v2","free_bytes":4711234560,
 "free_gb":4.711,"min_free_bytes":5000000000,"min_free_gb":5.0,
 "reason":"free space below configured floor","determinable":true}
```

An undeterminable-space abort is the same record with `"free_bytes":null`,
`"determinable":false` and `"reason":"free space could not be determined (deny
by default)"`.

`DISK_GUARD_ABORT` **closes every open coverage interval** and is the last
record the process writes — there is deliberately no `RECORDER_STOP` on top of
it. The process exits **3**, and `supervise.ps1` treats that code as *do not
relaunch*: restarting into a full disk is a loop that burns the remaining space
and hides the real fault. Free space on the volume, then start again by hand.

Exit codes: `0` clean stop, `3` guard abort, `4` supervisor hit its restart cap,
anything else a crash (relaunched).

---

## 3.4 Auto-restart — the most valuable thing in this deploy

> **Book gaps are permanently unrecoverable. Trades gaps are backfillable.**
>
> Kraken publishes no historical L2 — there is no endpoint, at any price, that
> returns the order book as it stood while this process was down. A minute of
> downtime is a minute of book that does not exist and never will. The public
> trade history endpoint *can* fill a trades gap, and OHLCV is fetchable, so a
> restart failure costs the book and only the book. That asymmetry is why the
> supervisor matters more than the cadence.

`supervise.ps1` relaunches on **any non-zero exit except 3**, with exponential
backoff (5 s doubling to a 300 s ceiling), and resets the ladder once a process
has stayed up for 10 minutes. It refuses to relaunch after exit `0` (an operator
pressed Ctrl-C and meant it) and after exit `3` (§3.3). A rolling cap of 20
restarts per hour turns a crash-loop into a loud stop rather than 150 connect
attempts in ten minutes, which is where Cloudflare starts banning the IP.

Every relaunch is logged with its reason **and** writes a `RESTART_BOUNDARY`
record into the coverage journal carrying the dead process's exit code. That is
what makes the downtime *attested* rather than inferred: `coverage_report`
labels the gap `restart` with that exit code instead of `unknown`. The dead
run's intervals are closed at **its own last record**, never at the boundary
marker — closing at the marker would claim coverage across the outage.

---

## 3.5 Console survival — running detached from any interactive session

**Finding (2026-07-27 capture-health audit, dispatch W8).** The capture
deployed 2026-07-27 13:43 UTC was NOT running under `supervise.ps1` at all —
live process inspection found a bare
`python -m recorder.record_kraken_ws run --book-mode snapshot
--snapshot-interval 1.0 --min-free-gb 5.0`, parented directly by a VS Code
integrated-terminal PowerShell host, itself parented by the VS Code process.
Closing that terminal, closing the VS Code window, or logging off any of them
kills the recorder with **no supervisor to relaunch it** — there is no
`RESTART_BOUNDARY`, no backoff, nothing; the next `RECORDER_START` would show
`prev_clean_shutdown: false` and the gap would report as `crash` at best,
`unknown` if the journal write is itself interrupted.

**A separate, larger gap was found in the same audit that this section does
NOT fix.** Between 2026-07-27T16:42:20Z and 20:48:45Z (~4h06m) the journal
recorded zero `HEARTBEAT_ROLLUP` records — heartbeats are a local timer task
independent of the network, so their total absence means the process was not
scheduled by the OS at all, not merely disconnected — and then the *same*
process (identical PID and `run_id`, no successor `RECORDER_START`) resumed on
its own. A kill cannot produce that signature; a system sleep/suspend can.
`coverage_report` did not surface this at all (see §4.1 caveat below) because
nothing closed the coverage interval — no `WS_DISCONNECT` fires until the
process actually resumes and its own recv-timeout notices the connection is
dead, which is also why the `WS_DISCONNECT` record for this event undersold
the gap (fixed in the same commit that added this section: `silent_s` is now
measured from `time.monotonic()`, not the fixed 10 s watchdog threshold).

**Two independent failures, two independent fixes:**

1. *Console/logoff kills the process* → run it as a Windows Scheduled Task
   instead of an interactive/terminal child process. A task registered with
   `LogonType S4U` runs in its own session, detached from any interactive
   logon or console, and an `AtStartup` trigger relaunches it after a reboot
   with no operator action:

   ```
   powershell -ExecutionPolicy Bypass -File recorder\register_scheduled_task.ps1 `
       -BookMode snapshot -SnapshotInterval 1.0 -MinFreeGb 5.0
   ```

   This registers the task; it does **not** start capturing until the
   operator stops whatever is currently running and starts the task by hand
   (`Start-ScheduledTask -TaskName KrakenForwardRecorder`) or reboots. The
   task launches `supervise.ps1` unchanged, so the existing disk guard,
   exit-code-3 no-relaunch rule, and `RESTART_BOUNDARY` journal marks all
   still apply — the task registration only changes *what keeps
   `supervise.ps1` itself alive*, not anything inside it. See
   `recorder/register_scheduled_task.ps1` for the full settings (battery
   behaviour, restart-on-task-failure, no execution time limit) and why each
   one is set.

2. *System sleep suspends the process regardless of how it was launched* →
   no Scheduled Task setting keeps a running task's process ticking through
   S3/modern-standby sleep. Disable sleep on AC power on the capture machine:

   ```
   powercfg /change standby-timeout-ac 0
   powercfg /change hibernate-timeout-ac 0
   ```

   Skipping this step means the Scheduled Task migration alone does not
   prevent a repeat of the 4-hour gap above — it only prevents the
   console/logoff failure mode, which is a different mechanism.

Neither command touches a currently running capture; the operator decides
when to cut over.

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

### 4.1 Coverage gap report — what was MISSED

`liveness` answers "is it running right now". This answers "what did we lose",
which is the question nobody asks until it is too late to fix:

```
python -m recorder.coverage_report
```

It reads the coverage journal and prints every interval that is **not**
attested, each with start, end, duration and the cause the journal actually
records — `disk_guard_abort`, `clean_stop`, `ws_disconnect`, `restart` (with
the dead process's exit code), `crash`, `not_yet_started`, or `unknown` — then
the total captured vs elapsed as a percentage.

`unknown` is a real answer, not a failure of the report: a gap whose cause the
journal cannot name is exactly what an operator needs to see.

An instant counts as **captured only when every (symbol, channel) pair is
attested**. 19 subscribed and 18 delivering is a partial-coverage defect, not a
rounding error — the same rule as check 3 above. Use `--symbol BTC/USD` /
`--channel book` for the per-pair view, `--start`/`--end` to bound the window,
and `--fail-on-gap` to make it exit non-zero for an unattended check.

> **Known blind spot (found 2026-07-27, dispatch W8).** A coverage interval is
> opened by `SUBSCRIBE_ACK` and closed only by `WS_DISCONNECT`, `RECORDER_STOP`,
> `DISK_GUARD_ABORT`, or a successor's `RECORDER_START` (`journal.py`
> `coverage_intervals`) — there is deliberately no requirement that
> `HEARTBEAT_ROLLUP` records keep landing inside that interval, because a quiet
> market legitimately produces zero-frame rollups (COVERED-AND-QUIET, §7). That
> design cannot distinguish "quiet market, process fine" from "process
> suspended by the OS and not scheduled at all" — both look identical to this
> report: an open interval with no closing record. A real ~4h06m gap
> (2026-07-27T16:42:20Z–20:48:45Z, confirmed by zero `HEARTBEAT_ROLLUP` records
> and zero shard files for three full hours across all 19 symbols) reported as
> fully CAPTURED here. **Cross-check `coverage_report`'s captured percentage
> against actual shard presence (§0 layout) when in doubt — do not trust either
> signal alone.** Not fixed in this pass (`coverage_report`/`journal.py` are
> shared read-path code — see §3.5 for the fix to the underlying cause).

Without this, downtime stays invisible until somebody reconstructs it from shard
file sizes — guesswork about the one stream that can never be re-fetched.

### 4.2 The log

`recorder.log` now has content in it. The `run` path logs boot (with the guard
reading), subscription completion, one heartbeat line per minute carrying frames,
symbols, bytes written and free space, guard state changes, disconnects,
reconnect attempts, restarts and the clean stop. Low volume by design.

It is still **not** the health check. Judge by §4, not by the log — see below.

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
| Journal ends in `DISK_GUARD_ABORT`, exit 3 | supervisor logged `NOT relaunching` | free-space floor breached, or free space undeterminable | free space on the volume, then start again by hand (§3.3). **The supervisor will not do this for you, on purpose.** |
| Supervisor exit 4 | `GIVING UP: N restarts in the last M min` | persistent fault, not a flap | investigate before restarting — Cloudflare bans ~150 connect attempts per rolling 10 min per IP |
| Gaps labelled `unknown` in the coverage report | — | process died with no attestation and no successor marker | check whether the supervisor was actually running; an unsupervised crash cannot be labelled |

**Silence in the log is never evidence of health.** The log now carries a
heartbeat line per minute (§4.2), which makes its *absence* informative — but a
present, cheerful log still proves nothing about coverage. The journal is the
record. Judge by §4, not by the log.

---

## 6. Stop

Ctrl-C in the foreground, or stop the Task Scheduler task. Either way the
`finally` block writes `RECORDER_STOP`, which closes every open coverage
interval, and the process exits `0` — which the supervisor reads as *the
operator meant this* and does not relaunch. A `kill -9` skips it — that is not
data loss, but it does mean the next `RECORDER_START` records
`prev_clean_shutdown: false` and the interval is closed at the last record the
dead process actually attested, leaving the downtime visibly UNCAPTURED. That is
the intended behaviour.

A `DISK_GUARD_ABORT` (§3.3) is also an *attested* stop, not a crash: the
successor records `prev_clean_shutdown: true`, because nothing was lost to a
crash — the disk ran out and the recorder shut down in order.

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

For the operator-facing view of the same journal — every uncaptured interval
with its attested cause, and the captured/elapsed percentage — see §4.1.

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
