# Kraken Forward Recorder

Continuously captures L2 order-book and trade data from Kraken's public WebSocket API. Designed to run unattended on a Linux server for months at a time.

## What this captures and why

**The 19 pairs** (by USD quote):
`BTC, ETH, XRP, SOL, ADA, SUI, ZEC, DOGE, XMR, LTC, ONDO, NEAR, LINK, TAO, AVAX, TRX, AAVE, INJ, UNI`

**What's captured per pair:**
- **L2 Order Book (depth 10)** — top 10 bids and asks with every update (delta mode)
- **Full public trade feed** — every trade as it executes
- **Instrument metadata** — price and quantity precision rules (required for book verification)
- **Heartbeats** — every ~1 second when nothing else is flowing (proves the socket is alive)

**Why this data matters:**
- The order book **cannot be fetched from history**. Kraken publishes no historical L2 API. Once it's gone, it's gone forever.
- Trades and OHLCV **can** be re-fetched later.
- This is the only renewable source of genuine unseen out-of-sample data.

## Cadence and sizing

**Snapshot interval:** 1-hour (1s would be redundant; 1h captures enough change to measure behavior)

**Disk growth (measured):**
- Raw (uncompressed): **~20.6 KB/s** steady-state = **~1.78 GB/day** raw
- Compressed (zstd level 10): **~156 KB/day** compressed = **~57 GB/year** compressed
- Provision **80–100 GB** disk; keep at least 5 GB free at all times (the disk guard enforces this)

**Compression ratio:** ~11.45x in production

## How the data is stored

**Layout:**
```
data/kraken_ws_v2/
  book_d10/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson       (open hour, being written)
  book_d10/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson.zst   (closed hours, compressed)
  trades/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson.zst
  meta/_session/{YYYY-MM-DDTHH}.ndjson.zst
  _session.ndjson                                  (coverage journal)
```

**Hourly roll:** At the top of each hour, the previous hour's files are compressed and verified before the raw is deleted.

**Coverage journal (`_session.ndjson`):**
- NDJSON log of every significant event: process start/stop, subscriptions, heartbeat summaries, WebSocket disconnects, and disk-guard events
- **Attestation:** if the journal records a gap, that gap happened and can be quantified
- **Truthful:** silence in the journal (no heartbeat records) means the process itself was not running — not the market was quiet
- **Query with:** `python -m recorder.coverage_report --out data/kraken_ws_v2`

## The supervision policy

**The script `supervise.sh` restarts the recorder on crash, but refuses to restart on:**
- **Exit code 0** (clean stop, operator called `systemctl stop`)
- **Exit code 3** (DISK_GUARD_ABORT — free space fell below 5 GB)

**Restart behavior on any other crash:**
- Bounded exponential backoff: 5s, 10s, 20s, 40s, 80s, 160s, 300s max
- Backoff resets if the process stays up ≥ 10 minutes (healthy)
- Cap: no more than 20 restarts per 60-minute window (indicates a persistent fault)
- **Why?** Kraken bans ~150 connection attempts per 10 minutes per IP. A restart loop would exhaust that ban in minutes.

**Why no restart after exit 3?**
Restarting into a full disk causes a loop that burns the remaining free space and hides the real problem. You must fix the storage, then start again by hand.

## Is it working?

```bash
# One-liner health check (0 = healthy, 1 = problem):
python -m recorder.liveness

# Detailed gap report:
python -m recorder.coverage_report --out data/kraken_ws_v2

# Human-readable word-of-mouth health:
python -m recorder.liveness
# Output:
#  reading 1 @ 2026-07-29T10:00:00.000000Z  bytes=254588536  shards=1092
#  reading 2 @ 2026-07-29T10:01:10.000000Z  bytes=254597844  shards=1092
#  ok    growth 9308 bytes over 70.1s (131.5 B/s)
#  ok    newest recv_ts 2026-07-29T10:01:09.882065+00:00 (0.9s old, limit 30s)
#  ok    journal last record HEARTBEAT_ROLLUP @ 2026-07-29T10:00:47.824819Z (20.9s old)
#  ok    open coverage intervals for 19 symbols (expected 19)
#  ok    rollup @ 2026-07-29T10:00:47.824819Z: 1191 frames, 60 heartbeats, 19/19 symbols
#  HEALTHY
```

**What "HEALTHY" means:**
- Bytes are growing (not stuck)
- Newest data is fresh (within 30 seconds)
- Heartbeats are flowing (proves the socket is alive)
- All 19 pairs are subscribed

**What's NOT healthy:**
- Output: `UNHEALTHY` (something failed)
- Details: `coverage_report` will tell you which pairs have gaps and when

## Troubleshooting

**"UNHEALTHY — no bytes written over 70s"**
- The process is running but not capturing
- Check the supervisor log: `tail -100 recorder.log`
- Kraken's WebSocket endpoint may be down

**"Growth stopped / newest data stale"**
- The socket disconnected and didn't reconnect (network issue or Kraken problem)
- Brief disconnects (seconds) are normal and expected
- Persistent silence (>30s) is a problem
- Restart: `systemctl restart kraken-forward-recorder`

**"Disk full"**
- The guard detected <5 GB free and stopped (exit 3)
- Free up space, then restart: `systemctl start kraken-forward-recorder`
- If disk keeps filling: increase VPS storage, or change the cadence (see docs below)

**"Process won't start"**
- Check supervisor log: `tail -100 recorder.log`
- Check Python and dependencies: `python -m pip install -r requirements.txt`
- Network (DNS, firewall): verify you can reach `wss://ws.kraken.com/v2` from this machine

## How to get the data back

See `OPERATOR_HANDOVER.md` → "Handing data back to analysis".
