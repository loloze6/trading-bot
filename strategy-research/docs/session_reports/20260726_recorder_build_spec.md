# Forward Recorder — Build Spec (Dispatch D1)

Date: 2026-07-26 · Baseline: `83ba63a` · Read-only dispatch, no code written.
Roadmap Phase 2.4 ("small always-on recorder daemon + storage plan").

---

## 1. Precondition manifest — PASS

| Check | Required | Measured |
|---|---|---|
| `git log --oneline -1` | starts `83ba63a` | `83ba63a Exclude holdout-carrying cache files from publication; register them` |
| `git status --porcelain \| grep -v '^??' \| wc -l` | `0` | `0` |

No tracked file modified or deleted. Untracked `strategy-research/runs/**` and `results/` are
outside the manifest's scope (`^??` filtered) and were not touched.

**Holdout:** this spec concerns data recorded 2026-07-26 forward. `holdout_range` is
`2026-01-01..2026-06-30` (`campaign_data_policy.yaml:18`). No overlap, no seal interaction.
`holdout_sealed/`, `Kraken_batch/q1_26/` and the 7 contaminated root CSVs were not opened.

---

## 2. Reuse vs. new

**One-liner: essentially nothing is reusable as code — the repo has no websocket client, no
daemon and no scheduler — but two *conventions* are directly reusable and must be honoured.**

### What exists

| Thing | Location | Verdict |
|---|---|---|
| Live price path | `data_manager.py:864-890` `_rest_price_fetcher` | **Not reusable.** REST *ticker* polling via `self.client.get_symbol_ticker` (`:895`) — Binance-specific, last-price only, no depth, no trades. |
| Live tick→candle | `data_manager.py:901-927` `live_main_candle_processing_loop`, `:933-947` `_process_live_tick` | Not needed for capture. |
| `CandleBuilder` | `data_manager.py:135-357` | **Reusable later, not now.** Useful only if we derive OHLCV from recorded trades (`add_tick`, `:165`). Out of MVP. |
| Threading shape | `data_manager.py:801-828` `initiate_start_thread` — daemon threads + `queue.Queue`, one poll thread per feed (`:830-862`) | Pattern is fine; ~20 lines. Copy the shape, not the code. |
| `BaseFetcher` | `base_fetcher.py:64+` | **Not reusable, and must not be subclassed.** It is backfill-shaped: fixed `interval_seconds` (`:102`), CSV cache at `data_dir/{cache_key}.csv` (`:234`), `_fetch_remote(start,end)`. Its gap arithmetic (`_gap_intervals`, `:272-291`) assumes a *regular grid* — an event-driven stream has no expected interval, so every guard there misfires. |
| `FetchGapError` | `base_fetcher.py:42-61` | **Reuse the doctrine, not the class.** See §5. |
| Exchange-qualified cache key | `ccxt_fetcher.py:101-121` — `prefix = "" if exchange_id == "binance" else f"{exchange_id}_"` | **Reuse the convention.** Recorder paths must carry `kraken_`. |
| Websocket client / daemon / scheduler | — | **None exists.** `git ls-files | grep -iE 'websocket|daemon|record|stream|scheduler'` matches only docs, `strategy-research/tools/record_schema.py` (an artifact schema, unrelated), and `tools/ingest_kraken_archive.py` (batch CSV ingest). |

### Must be new
Websocket client + subscribe/resubscribe logic; session/coverage journal; shard writer +
rotation; watchdog; liveness self-test; consumer-side coverage loader.

### Universe on disk (19 pairs, confirmed)
`local_data/kraken_<BASE>USD_1h.csv` — BTC ETH XRP SOL ADA SUI ZEC DOGE XMR LTC ONDO NEAR
LINK TAO AVAX TRX AAVE INJ UNI. Quote is **USD, not USDT** (`campaign_data_policy.yaml:88`).
Kraken WS v2 symbols are `BTC/USD` form (not `XBT`); map `BTC/USD` → `BTCUSD` on write.

---

## 3. Kraken venue capabilities

All fetched **2026-07-26**. Endpoint for v2 public market data: `wss://ws.kraken.com/v2`.

| Capability | Finding | Source |
|---|---|---|
| L2 book depths | Exactly five: **10, 25, 100, 500, 1000**. Default 10. | [websocket-v2/book](https://docs.kraken.com/api/docs/websocket-v2/book) |
| L2 semantics | Full **snapshot** on subscribe (`snapshot` param, default `true`), then **incremental updates** carrying only changed levels. "It is possible to have multiple updates to the same price level in a single update message. Updates should always be processed in sequence." | ibid. |
| L2 integrity | **CRC32 checksum over the top 10 bids and asks** on both snapshot and update. Plus RFC3339 `timestamp`. | ibid. |
| **Sequence numbers** | **None on the book channel.** Documented fields are `symbol`, `bids`, `asks`, `checksum`, `timestamp`. The L3 page states outright: "no sequencing is required." **Dropped-message detection is checksum-based, not sequence-based** — this drives §5. | [book](https://docs.kraken.com/api/docs/websocket-v2/book), [level3](https://docs.kraken.com/api/docs/websocket-v2/level3) |
| Trades | Public. `channel: "trade"`, `symbol: [...]`, optional `snapshot` (default **false**; snapshot = most recent 50 trades). Fields: `symbol, side, qty, price, ord_type, trade_id, timestamp`. Multiple trades may share one message. | [websocket-v2/trade](https://docs.kraken.com/api/docs/websocket-v2/trade) |
| Heartbeat | Auto-generated on any subscription, **~1/sec, only when no other channel update is flowing**. Payload is `{"channel":"heartbeat"}`. | [websocket-v2/heartbeat](https://docs.kraken.com/api/docs/websocket-v2/heartbeat) |
| Status | Sent on connect and on engine-state change. Fields `system` (`online`/`maintenance`/`cancel_only`/`post_only`), `api_version`, **`connection_id`**, `version`. | [websocket-v2/status](https://docs.kraken.com/api/docs/websocket-v2/status) |
| L3 (order-by-order) | **Authenticated** — "requires an API token to subscribe." Depths 10/100/1000. Not available as public capture. | [level3](https://docs.kraken.com/api/docs/websocket-v2/level3) |
| **Liquidations** | **NOT publicly available.** The only `liquidated` field is on the **private, authenticated `executions` channel**, which reports "order status and execution events for **this account**" — own-account only, not market-wide. Kraken **Futures** public feeds are trade, book, ticker, ticker_lite, heartbeat — no liquidation feed either. | [executions](https://docs.kraken.com/api/docs/websocket-v2/executions), [Futures WS ticker](https://docs.kraken.com/api/docs/futures-api/websocket/ticker/) |
| Limits | 200 symbols per connection; multiple connections allowed. Cloudflare connection/re-connect cap ≈150 attempts per rolling 10 min per IP → 10-min ban. Reconnect guidance: instant retry a handful of times on a random drop; after maintenance/extended downtime **no faster than once per 5s**. | [WS FAQ](https://support.kraken.com/articles/360022326871-kraken-websocket-api-frequently-asked-questions) — *caveat: the FAQ page as served renders v1 content; the 200-symbol and 150-attempt figures come from Kraken support/doc indexing and should be re-verified against a live connection before relying on them. They are not binding constraints for us: 19 symbols × 2 channels fits one connection with 90% headroom.* |

**Liquidations: no. Not publicly available on Kraken, spot or futures.** If liquidation data is
a research requirement it needs a different venue (e.g. Binance `forceOrder`) — a separate
decision, out of this spec.

---

## 4. Storage sizing

**Assumptions (stated so they can be falsified against the first 24h of real capture):**
- A1. Blended book-update rate across the 19 pairs, 24h average, msg/s/pair:
  d10 **5**, d25 **8**, d100 **15**, d500 **30**, d1000 **45**. Rationale: activity concentrates
  at the touch, so a 100× depth increase buys ~9× message rate, not 100×.
- A2. Avg raw JSON bytes/message: d10 **200**, d25 **210**, d100 **230**, d500 **260**, d1000 **280**
  (deeper subscriptions batch more changed levels per message).
- A3. Trades: blended **0.5 trades/s/pair**, **150 B/trade** amortised over the shared envelope.
- A4. zstd-3 on line-delimited JSON book data: **10×**. Conservative; repeated keys and
  near-identical prices typically give 8–12×.
- A5. 19 pairs, 86,400 s/day, 365-day year.

Arithmetic: `bytes/day = rate × size × 86400 × 19`.

| Stream | B/day/pair | GB/day (19) | 30 d raw | 12 mo raw | **12 mo zstd** |
|---|---|---|---|---|---|
| L2 d10 | 5×200×86400 = 86.4 MB | 1.64 | 49.2 GB | 599 GB | **59.9 GB** |
| L2 d25 | 8×210×86400 = 145.2 MB | 2.76 | 82.7 GB | 1 007 GB | **100.7 GB** |
| L2 d100 | 15×230×86400 = 298.1 MB | 5.66 | 170 GB | 2 067 GB | **206.7 GB** |
| L2 d500 | 30×260×86400 = 673.9 MB | 12.80 | 384 GB | 4 674 GB | **467 GB** |
| L2 d1000 | 45×280×86400 = 1 088.6 MB | 20.68 | 620 GB | 7 550 GB | **755 GB** |
| Trades | 0.5×150×86400 = 6.48 MB | 0.12 | 3.7 GB | 45 GB | **4.5 GB** |

### Recommended capture profile

> **L2 depth = 10 on all 19 pairs + full trades, NDJSON, zstd-rolled nightly.**
> **12-month total ≈ 64 GB** (59.9 + 4.5). Uncompressed working set 1.76 GB/day / 53 GB/month.

Why d10 and not d25 (which at 105 GB narrowly *fails* the 100 GB budget anyway):
- The CRC32 checksum covers **exactly the top 10 levels**. At depth 10 the entire captured book
  is checksum-verifiable; at depth 1000, 99% of it is not.
- It is the API default — no `depth` param, one less thing to get wrong on day one.

**What d10 sacrifices, honestly:** no visibility beyond the top 10 levels per side. Market-impact
and slippage curves are calibratable only for orders that clear within top-10 liquidity; no
deep-book resilience, no book-shape/iceberg work, no depth-weighted imbalance beyond L10. For a
19-pair *breadth* strategy (XS_momentum-class, hourly rebalance) top-10 is the relevant regime;
if a future hypothesis needs deep book, re-subscribing at higher depth is a one-line change —
but the intervening months are unrecoverable at that depth. **This is the real cost and the
director should see it stated: choosing d10 today permanently caps what the 2026-H2 tranche can
answer.** The recommendation stands anyway, because d1000 at 755 GB/yr is not operable on this
machine and "start narrow today" beats "start wide next month."

---

## 5. Gap detection — first-class requirement

**The venue gives us no sequence numbers (§3). Therefore the recorder cannot distinguish
"no activity" from "not captured" from the market-data stream alone. That distinction must be
manufactured by a separately-written coverage journal. This is the single most important
design constraint in this spec.**

### Precedent
`FetchGapError` (`base_fetcher.py:42-61`) exists because Kraken's REST OHLC endpoint silently
ignores `since`, `_fetch_remote`'s `if not candles: break` exits cleanly, `_merge_and_store`
writes, and **the run logs success while leaving a ~173-day hole**. Its own docstring: *"A
wrong-data read that announces itself as success is the worst shape a data defect can take."*
The recorder's exact analogue is a half-open TCP socket: the process stays alive, the log stays
quiet, the file simply stops growing. Same defect shape, same rule.

The guard's second property is also inherited: `_assert_no_new_gap` (`base_fetcher.py:293-330`)
is **differential** — it compares gap intervals before vs. after and fails only on gaps that
escape every pre-existing gap's bounds. The recorder's coverage journal is the "before" set;
only *unattested* time is a defect.

### Design

1. **Coverage journal** — `_session.ndjson`, append-only, `fsync` on every record, written
   *before* the corresponding stream action. Record types:
   `RECORDER_START` / `WS_CONNECT` (carrying `connection_id` from the status channel) /
   `SUBSCRIBE_ACK` (per symbol, per channel) / `HEARTBEAT_ROLLUP` (one record per minute:
   count of frames seen per symbol; a minute with zero frames but a live heartbeat is
   **covered-and-quiet**) / `CHECKSUM_MISMATCH` / `STATUS_CHANGE` (e.g. `system=maintenance`) /
   `WS_DISCONNECT` (close code + reason) / `RECONNECT_ATTEMPT` (n, backoff) / `RESUBSCRIBE` /
   `RECORDER_STOP`. Every record carries UTC wall clock **and** a monotonic counter (wall clock
   alone cannot survive an NTP step or a laptop suspend).
2. **Coverage intervals are the consumer contract.** A loader derives, per symbol,
   `[covered_from, covered_to]` from `SUBSCRIBE_ACK` → `WS_DISCONNECT`/`STOP`. Any wall-clock
   instant outside those intervals is **UNCAPTURED**; inside them with no frames is
   **QUIET**. The loader must **raise** (not warn, not fill) if asked for a window the journal
   does not attest — this is the recorder's `FetchGapError`, at the *read* boundary this time
   because there is no merge step to guard.
3. **Checksum verification.** Maintaining a live local book to verify CRC32 is ~3 h of work and
   is **deferred out of MVP**. Mitigation that costs nothing: the `checksum` field is captured
   verbatim in every line, so verification is fully available as a post-hoc replay pass. Once
   live verification exists, a mismatch → `CHECKSUM_MISMATCH` + forced resubscribe, and the span
   `[mismatch_ts, resnapshot_ts]` is journaled as **DEGRADED** (a third state, distinct from
   uncaptured and quiet).
4. **Heartbeat watchdog — in MVP, non-negotiable.** Heartbeat is ~1/s whenever the stream is
   otherwise idle, so *any* 10-second silence across all channels means the socket is dead, not
   the market. On timeout: close, journal `WS_DISCONNECT(reason=heartbeat_timeout)`, reconnect
   (instant ×3, then 5 s fixed per Kraken guidance, §3). Without this, the half-open socket case
   produces a multi-hour hole with no error anywhere — precisely the defect `FetchGapError`
   was written to make impossible.
5. **Restart is not a gap-eraser.** On restart the recorder writes `RECORDER_START` with the
   previous process's last journal offset, so an operator-invisible crash-restart still shows up
   as a bounded uncaptured interval rather than as continuous coverage.

### Operator liveness check
Per the standing rule that a 0-byte log is a failure, not a quiet market:

- `--selftest` mode: connect, subscribe all 19, require ≥1 snapshot **per symbol** within 30 s,
  exit non-zero otherwise. Run this before trusting any deploy.
- Steady state (one command, run twice ~60 s apart): current shard byte count **must increase**;
  `tail -n 1` of the shard must carry a `recv_ts` within ~5 s of now; distinct symbols in the
  last 60 s of `_session.ndjson` must equal **19**. Any of the three failing = down.
- Zero bytes, or 19 → 18 symbols, is an alert. Silence is never evidence of a quiet market
  because heartbeat guarantees traffic.

---

## 6. Registration entry (specified, NOT written)

New top-level key in `strategy-research/config/campaign_data_policy.yaml`:

- **key**: `kraken_ws_forward_recorder`
- **source_id**: `kraken_ws_v2_l2_book_d10`, `kraken_ws_v2_trades` (two streams, one entry)
- **venue**: `kraken`, spot, quote `USD` — matches `kraken_breadth_19pair` (`:88`), same 19 bases
- **provenance**: `live_websocket_capture` — first-party, real-time. A third provenance class
  distinct from the existing `bulk_archive` (Kraken_batch) and REST `CcxtFetcher` fetch; the
  distinction matters because this one **cannot be re-derived if lost**.
- **cadence**: `event_driven` — explicitly **not** a fixed interval. Must state that
  `BaseFetcher.interval_seconds` gap arithmetic (`base_fetcher.py:272-291`) does not apply and
  that coverage is attested by the session journal (§5), not by grid continuity.
- **recording_started**: `2026-07-26`; **span**: `["2026-07-26", null]` (open-ended)
- **cache_dir**: `local_data/recorded/kraken_ws_v2/{stream}/{SYMBOL}/{YYYY-MM-DD}.ndjson[.zst]`.
  Deliberately **not** `local_data/` root — that flat namespace is the contaminated Binance
  slot (`campaign_data_policy.yaml:194-241`). Filenames keep the `kraken_` exchange
  qualification of `ccxt_fetcher.py:120-121`.
- **era**: requires a **new** entry in the `eras:` list —
  `era_id: era_2026_h2_forward_recorded`, `range: ["2026-07-26", null]`,
  `feeds_available: [l2_book_d10, trades]`. Note plainly that **no prior era has l2_book or
  trades at all**, so any hypothesis using them is inherently un-backtestable before this date.
- **holdout relationship**: `holdout_overlap: none` — capture begins 2026-07-26, after
  `holdout_range` end 2026-06-30 (`:18`). `holdout_range` **UNCHANGED**; no seal interaction.
- **status**: recommend `recorded_reserved_undesignated`.

**Adversarial note on that status, for the director.** Forward-recorded data is the *only*
genuinely uncontaminated out-of-sample this campaign will ever have — nobody, including us, has
seen it. Registering it as walk-forward-eligible on arrival spends that property immediately and
irreversibly, for the same reason `holdout_failure_is_terminal` (`:272`) exists. Recommend it
lands as **recorded, reserved, undesignated**, with the search/holdout split a separate, dated,
ratified decision — ideally taken *before* enough of it accumulates to be tempting.

---

## 7. MINIMAL VIABLE RECORDER

Ordered for time-to-first-byte. Everything below is new code in
`strategy-research/tools/record_kraken_ws.py` unless noted.

| # | Step | Hours |
|---|---|---|
| 1 | Pin a websocket client (`websockets`) into `venv`; verify a bare connect to `wss://ws.kraken.com/v2` returns a `status` frame. | 0.25 |
| 2 | Connect, subscribe `book` (depth 10, snapshot true) + `trade` for all 19 symbols on **one** connection. Write every received frame **verbatim** as one NDJSON line, prefixed with a local `recv_ts`, to a daily-rotated shard per stream. **No parsing, no local book, no schema.** | 2.0 |
| 3 | Session/coverage journal (§5.1): start/connect/status/ack/disconnect/reconnect/stop + per-minute heartbeat rollup, `fsync` per record. | 1.5 |
| 4 | Heartbeat watchdog (§5.4): 10 s silence → close, journal, reconnect with backoff (instant ×3, then 5 s). | 1.0 |
| 5 | `--selftest` + the 3-part steady-state liveness check (§5, operator section). | 0.75 |
| 6 | Run under a restart supervisor (Windows Task Scheduler / NSSM, or a shell restart loop). Confirm it survives a forced kill. | 0.5 |
| 7 | Write the `campaign_data_policy.yaml` entry (§6) + `local_data/recorded/README.md`. | 0.5 |
| | **Total to bytes-on-disk with attested coverage** | **6.5 h** |

**Deferred, with the cost of deferring stated:**
- *zstd at write* (~1 h) — deferred. Raw d10+trades is 1.76 GB/day / 53 GB/month, comfortable
  for weeks. Add a nightly roll-up of yesterday's closed shards **within the first week**;
  before that, disk is the only exposure and it is bounded.
- *Local book + live CRC32 verification* (~3 h) — deferred. Checksums are captured verbatim, so
  this is recoverable as a replay pass. Until it lands, an undetected book desync appears as
  a silent data-quality defect rather than a `CHECKSUM_MISMATCH` interval — the one deferral
  that genuinely weakens §5, and it should be the first thing added after MVP.
- *Trades → OHLCV via `CandleBuilder`* — not capture work; do it when a consumer needs it.
- *The 2026-04-01 → present OHLCV backfill hole* (B1-R) — a separate REST/archive task. **The
  recorder does not fix it and does not shrink it; it only stops it growing.** Every day
  without step 2 running is permanently lost, which is the whole argument for the 6.5 h path
  over anything larger.
