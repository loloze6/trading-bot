# Kraken Forward Recorder — RUNBOOK

Phase 2.4 always-on capture daemon. Build spec:
`strategy-research/engineering/sessions/session_reports/20260726_recorder_build_spec.md`.

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
python -m pip install -r strategy-research/tools/recorder/requirements.txt
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
   `tools/recorder/register_scheduled_task.ps1` for the full settings (battery
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
`strategy-research/engineering/sessions/session_reports/20260726_recorder_cadence_ladder.md`.
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

---

## 10. Linux deployment (dispatch W15)

### 10.1 Portability status

The recorder's Python is already Linux-portable: every path uses `pathlib`,
`disk_guard.probe_free_bytes` is `shutil.disk_usage` (works identically on
both OSes), `shard_writer`/`journal`/`compaction` use only `open`/`os.fsync`/
`os.replace`, and `record_kraken_ws.py`'s signal handling
(`getattr(signal, "SIGBREAK", None)`) already degrades gracefully where a
signal doesn't exist — `add_signal_handler` for SIGINT/SIGTERM is in fact
*more* reliable on Linux's default asyncio event loop than on Windows'
ProactorEventLoop, which is why that fallback path exists at all. Nothing in
`whale_features.py`, `whale_persistence.py`, `shard_reader.py`,
`kraken_crc.py`, or `book_state.py` references an OS-specific API.

**What was actually Windows-specific**, entirely confined to two files and
one operational habit:

| Item | File:line | Status |
|---|---|---|
| Restart-supervisor script | `tools/recorder/supervise.ps1` (whole file) | Ported: `tools/recorder/supervise.sh` |
| Detached/reboot-surviving launch | `tools/recorder/register_scheduled_task.ps1` (whole file) | Ported: `tools/recorder/install_systemd_unit.sh` |
| Sleep/suspend mitigation | `RUNBOOK.md` §3.5 `powercfg` commands | Not needed the same way — see 10.2 |
| PowerShell locale-dependent float formatting | `supervise.ps1:90-95` (`Fmt`, invariant-culture) | N/A on Linux — `supervise.sh` never round-trips numbers through a culture-aware formatter |
| ASCII-only requirement (PS5.1 BOM-less `.ps1` read as ANSI) | `tests/test_supervisor.py:132-144` | N/A to bash — no equivalent test needed for `supervise.sh` |

Also confirmed clean: `requirements.txt` (`websockets`, `zstandard`) both ship
`manylinux` wheels — no compilation needed on a standard x86_64 Linux host.

### 10.2 The sleep-suspend root cause doesn't repeat the same way on a server

The 2026-07-26/27 ~35h27m and ~4h06m gaps (SESSION_LOG, `coverage_report`)
were OS-level suspend, not process kills — a laptop-specific failure mode
(`powercfg` exists to fight it). A VPS does not sleep on lid-close or
idle-timeout the way a workstation does; there is no equivalent problem to
mitigate by default. `install_systemd_unit.sh`'s header still tells the
operator to check
`systemctl list-units --type=target --all | grep -E 'sleep|suspend'` and mask
those targets if the chosen image ships any idle-suspend behavior, so this is
verified rather than assumed on cutover.

### 10.3 Supervision — `supervise.sh` + `install_systemd_unit.sh`

Same policy as `supervise.ps1`, ported to Bash and re-verified against the
**same stub-recorder contract** in `tests/test_supervisor_sh.py` (relaunch on
crash + attest the gap; never relaunch on exit 0 or exit 3; restart-rate cap;
backoff-ladder reset after a healthy run) — genuinely executed under Git Bash
during this dispatch, not merely reasoned about; see the W15 session report
for what that does and doesn't prove.

Install (as root, on the capture host):

```
sudo bash tools/recorder/install_systemd_unit.sh \
    --user kraken --python-exe /path/to/venv/bin/python3 \
    --book-mode snapshot --snapshot-interval 1.0 --min-free-gb 5.0
sudo systemctl enable --now kraken-forward-recorder
systemctl status kraken-forward-recorder
python3 -m recorder.liveness
```

Design note: **a systemd `Restart=` ladder was deliberately NOT used to
reimplement the backoff/cap policy.** Native exponential backoff
(`RestartSteps=`/`RestartMaxDelaySec=`) only exists from systemd 254 onward
(missing on, e.g., Ubuntu 22.04's systemd 249) and would make the policy's
behavior depend on the target distro's systemd version — the opposite of the
"same policy, different host" goal. Instead `supervise.sh` owns the *entire*
recorder-restart policy itself, exactly as `supervise.ps1` does, and the
generated unit only adds a second, independent, much coarser layer
(`Restart=on-failure`, `RestartSec=10`, `StartLimitBurst=5`/`10min`) that
catches `supervise.sh` itself dying unexpectedly (OOM kill, bash fault) — a
different and much rarer failure than anything the internal loop handles.
`SuccessExitStatus=3 4` tells systemd that a `DISK_GUARD_ABORT` (3) or a
restart-cap give-up (4) are *both* terminal by policy, same as a clean exit
0 — so nothing above `supervise.sh` retries a stop that was reached on
purpose. Killing the whole cgroup (`KillMode=control-group`, systemd's
default) delivers `systemctl stop`'s SIGTERM to the recorder subprocess too,
which already has a portable SIGTERM handler that journals `RECORDER_STOP`
and exits 0 — so a stop is clean end to end without either script needing to
know about the other.

There is no S4U-style login-session special case to reach for on Linux — a
systemd **system** service (as opposed to a `--user` unit tied to a login
session) is never inside anyone's session in the first place, so "survives
logout" is true by construction rather than something to configure.

### 10.4 What was verified on real Linux semantics vs. reasoned only

No Linux host was available in this environment (Windows dev machine; tests
ran under Git Bash/MSYS). Being explicit about the difference:

**Executed for real (genuine verification, not simulation):**
- `supervise.sh`'s full restart/backoff/cap/attestation loop —
  `tests/test_supervisor_sh.py`, 7/7 passing, same stub-recorder contract as
  the PowerShell version.
- `install_systemd_unit.sh`'s unit-file generation and its systemd-quoting
  (`sdquote`) — smoke-tested against a stubbed `systemctl` and a path
  containing a space; the emitted `ExecStart=` line was inspected and is
  correctly double-quoted per `systemd.service(5)`'s command-line quoting
  rules. **Not** verified: that a real `systemd-analyze verify` or a real
  `systemctl start` accepts the unit — no systemd binary exists in this
  environment.
- `retrieve_shards.py` / `retrieval_manifest.py` — full pull/verify/ledger/
  prune logic against `LocalDirTransport`, 14/14 tests passing, including the
  journal's growing-prefix case and prune's re-verification-before-delete
  guard.

**Reasoned, not executed here (state this plainly rather than claim
verification that didn't happen):**
- `disk_guard.probe_free_bytes` on a real Linux filesystem — it is a bare
  `shutil.disk_usage()` call, which is implemented for POSIX via `statvfs(2)`
  in CPython's own stdlib; this is standard-library behavior, not
  recorder-specific code, so it is trusted on the strength of that rather
  than independently re-tested here.
- `compaction.py`'s `os.replace()` atomicity and the fsync-then-rename
  ordering, under an actual crash, on a real Linux filesystem (ext4/XFS).
  `os.replace` is atomic on POSIX by construction (`rename(2)`), matching
  what the module already relies on. The one **genuine open question** a
  real Linux host would need to answer that Windows/NTFS does not raise the
  same way: whether the **parent directory** also needs an explicit
  `fsync(dirfd)` after the compacted shard's rename, for the new directory
  entry itself to survive a power-loss-at-the-wrong-instant (a known
  POSIX/ext4/XFS subtlety with no NTFS equivalent). The existing per-file
  `fsync` before `os.replace` (`compaction.py:178`) already protects the
  *content*; a directory-entry fsync would harden the *rename becoming
  visible* against the same class of crash. Not implemented in this
  dispatch — flagged here as a real, host-specific hardening item for
  whoever operates this on bare-metal-adjacent Linux storage, not a defect
  in the current code.
- `journal.py`'s per-record `fsync` durability guarantee under Linux's actual
  write-back semantics — the call (`os.fsync(fh.fileno())`) is standard and
  correct; its real-crash behavior on the target VPS's specific storage
  (network-attached block storage vs. local NVMe) was not measured because no
  such host exists yet to measure it against.
- SSH/rsync transport (`SshRsyncTransport` in `retrieve_shards.py`) — the
  logic around it is fully tested via `LocalDirTransport`, but no real SSH
  host was available to exercise the actual subprocess calls to `ssh`/
  `rsync`. Verify with a real host before the first production retrieval;
  `rsync` availability on the analysis machine (Windows) needs Git-for-
  Windows, Cygwin, or WSL — not assumed present.

### 10.5 Data retrieval — `retrieve_shards.py`

Analysis runs locally; capture runs on the server. `tools/recorder/retrieve_shards.py`
pulls compacted shards (`*.ndjson.zst`) and the coverage journal back,
incrementally and resumably, verified against a hash **computed on the
capture host** (`tools/recorder/retrieval_manifest.py`, run over SSH) rather than
trusting the transfer protocol alone.

```
# regular pull (run this on a schedule, e.g. weekly cron)
python -m recorder.retrieve_shards pull \
    --host kraken-vps --remote-out /data/kraken_ws_v2 \
    --local-out trading-bot/local_data/recorded_reserved/kraken_ws_v2 \
    --identity ~/.ssh/kraken_vps

# only once retrieval has been trusted for a while, and only explicitly:
python -m recorder.retrieve_shards prune --yes-delete-confirmed-only \
    --host kraken-vps --remote-out /data/kraken_ws_v2 \
    --local-out trading-bot/local_data/recorded_reserved/kraken_ws_v2
```

Properties (see `retrieve_shards.py`'s module docstring for the full
reasoning):

- **Incremental** — `_retrieval_ledger.json` in the local output root records
  every already-verified path's hash; `pull` only fetches what's new,
  changed, or previously failed. The coverage journal is the one file that
  legitimately keeps growing: it gets a **prefix hash** (first N bytes) in
  the manifest rather than a whole-file hash, so each pull only needs to
  transfer and verify the delta past the last confirmed byte, and a pull
  that lands mid-write of the newest record is safe (a torn final line is
  exactly what `journal.load_records` already tolerates).
- **Resumable** — an interrupted `pull` leaves the ledger showing precisely
  what was and wasn't confirmed; rerunning it picks up cleanly, no manual
  bookkeeping.
- **Integrity-verified** — every pulled file's local hash is checked against
  the manifest's hash before it is added to the ledger; a mismatch is
  reported as failed and retried on the next run, never silently accepted.
- **Never deletes anything not confirmed received** — `pull` never deletes
  anything, on either side, under any circumstance. `prune` is a *separate*,
  explicitly-flagged command that only deletes a remote file if (a) the
  ledger has it confirmed, (b) a **freshly re-fetched** remote manifest still
  shows the same hash (catches the file changing after confirmation, which
  should never happen for an already-compacted shard but is checked rather
  than assumed), and (c) the local copy's hash, re-checked at prune time,
  still matches too. The coverage journal is never eligible for deletion by
  `prune` at all — it is small and there is no storage pressure it relieves.

### 10.6 Sizing and cost

**Measured inputs used below** (no estimates in this paragraph):
cadence-ladder `snapshot@1s` raw rate **20,576 B/s** steady-state (measured,
`engineering/sessions/session_reports/20260726_recorder_cadence_ladder.md` — this is the
currently-deployed mode); real 18-hour production compaction
**11.45x** (622.73 MB raw → 54.39 MB compressed, SESSION_LOG 2026-07-28
hand-off note) — used here in preference to the cadence ladder's own
synthetic 15.41x, which was measured on a 208.7 s sample rather than
real multi-hour production data.

**Refined 12-month compressed projection** (measured raw rate ÷ measured
real-world ratio, continuous capture assumed — the whole point of this
migration):

```
20,576 B/s x 86,400 s/day x 365 days = 648.9 GB/12mo RAW
648.9 GB / 11.45  =  56.7 GB/12mo COMPRESSED
```

This is **~35% higher** than the cadence ladder's own `snapshot@1s`
projection of 42.1 GB/12mo, because that number used the short synthetic
sample's 15.41x ratio rather than the ratio actually observed in production.
**Use 56.7 GB/12mo, not 42.1 GB/12mo, for disk provisioning** — it is the
more conservative figure and it is measured, not the synthetic one.

**Disk**: 56.7 GB data + 5 GB disk-guard floor (unchanged — this dispatch did
not touch it) + ~8 GB OS/venv/logs headroom ≈ **70 GB minimum**; provision
80-100 GB for margin against a more volatile year (the ladder's own §3 notes
book-byte share is dominated by a few tick-dense low-priced pairs — a
volatile DOGEUSD, for example, would push totals up, not down).

**Bandwidth (retrieval)**: 56.7 GB/12mo ÷ 52 ≈ **~1.1 GB/week** compressed
data pulled from server to analysis machine (the ladder's own number gives
~0.8 GB/week — either way, trivial). This is the server's *outbound*
transfer, the side VPS providers meter; inbound (SSH commands, manifest
JSON) is negligible.

**Rough monthly cost — ASSUMPTION, not measured, verify before purchasing.**
A single-vCPU tier with ~80 GB SSD and generous outbound transfer is roughly
**USD 6-10/month** at current (2026) market rates from budget providers
(e.g., Hetzner's `CX32`-class tier: 80 GB SSD, ~20 TB/month outbound,
reported around $8/month post their 2026 price adjustment). This figure came
from a web search of third-party pricing aggregators, not the providers' own
pricing pages, and is explicitly a rough planning number — confirm current
pricing directly with whichever provider is chosen before purchasing. At
that tier, ~1.1 GB/week of retrieval traffic is a rounding error against a
multi-TB/month allowance — no bandwidth overage risk under any provider
considered.

### 10.7 Cutover runbook

**Precondition**: do not stop or reconfigure the Windows capture until the
new host has been verified healthy per below. The Windows recorder keeps
running throughout steps 1-4.

1. **Provision and install** on the new host: clone/rsync this repo,
   `pip install -r tools/recorder/requirements.txt`, confirm `python3 -m
   recorder.record_kraken_ws selftest` passes (RUNBOOK §2).
2. **Install and start supervision**:
   ```
   sudo bash tools/recorder/install_systemd_unit.sh --user kraken \
       --python-exe /path/to/venv/bin/python3 \
       --book-mode snapshot --snapshot-interval 1.0 --min-free-gb 5.0
   sudo systemctl enable --now kraken-forward-recorder
   ```
3. **Verify the new host is healthy before trusting it for anything**:
   ```
   python3 -m recorder.liveness            # must print HEALTHY
   python3 -m recorder.coverage_report --fail-on-gap   # since RECORDER_START on this host
   ```
   Do not proceed past this step on a liveness failure or an unattested gap
   since this host's `RECORDER_START` — that is exactly the class of silent
   failure §3.5/§4 exist to catch, now on a second host.
4. **Confirm attestation, not just "it's running"**: the new host's own
   coverage journal must show `RECORDER_START` → ongoing `HEARTBEAT_ROLLUP`s
   with 19/19 symbols, the same three checks `liveness.py` already runs.
   Only once this has held for a period the operator is comfortable with
   (hours, not minutes — a fresh process can look healthy for a few minutes
   before a config mistake surfaces) should the Windows recorder be stopped.
5. **Stop the Windows recorder without losing the in-flight hour**: send it a
   clean stop signal (Ctrl-C on the console it runs under, or
   `Stop-ScheduledTask -TaskName KrakenForwardRecorder` if it was migrated to
   the scheduled task first) and confirm exit 0 / `RECORDER_STOP` in its
   journal — never `kill -9`/`Stop-Process -Force`, which forfeits the clean-
   shutdown attestation the whole design exists to provide. The **current**
   (not-yet-hour-closed) shard is left exactly where it is; it is not raw
   data at risk, just not yet compacted — `compaction.sweep()`'s startup pass
   picks up anything orphaned by a stop if the process is ever relaunched on
   that machine again, and in any case the shard itself is complete and
   unaffected by which process wrote it.
6. **Retrieve once, promptly, after cutover**: run `retrieve_shards.py pull`
   against the new host to establish the first ledger baseline before
   relying on a weekly cadence.

**Rollback, if the server proves worse** (degraded uptime, host-specific
network issues, anything the whole point of migrating was meant to avoid):
stop the new host's service (`sudo systemctl stop
kraken-forward-recorder`), confirm its journal shows a clean `RECORDER_STOP`,
restart the Windows recorder (§3, `supervise.ps1` or the scheduled task), and
retrieve whatever the server captured before rollback via
`retrieve_shards.py pull` — the ledger and manifest design means a partial or
short-lived server capture is retrieved exactly like any other, with no
special-casing needed. Nothing about rollback requires deleting anything on
either host; `retrieve_shards.py prune` is never required and should not be
run until well after the decision to stay on the new host is final.
