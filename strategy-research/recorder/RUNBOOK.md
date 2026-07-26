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

---

## 4. Health check — THE command

Run this. It is the whole check.

```
python -m recorder.liveness
```

**It sleeps ~70 s by design** (it needs two size readings) and exits `0` only
when all three of these hold:

1. **GROWTH** — total shard bytes strictly increased between the two readings.
   Zero bytes fails. Flat fails.
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
* **zstd at write** — deferred. Raw d10 + trades is bounded and disk is the
  only exposure. Add a nightly roll-up of closed shards within the first week.
* **Trades → OHLCV** — not capture work; do it when a consumer needs it.

## 9. Not available at this venue

**Kraken publishes no public liquidation feed** — spot or futures. The only
`liquidated` field is on the private, authenticated `executions` channel, which
is own-account only. Roadmap 2.4's "live liquidation events" is **INFEASIBLE
here, not deferred**; it requires a different venue (e.g. Binance `forceOrder`)
and that is a separate decision.
