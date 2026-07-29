# Operator Handover

Install, run, and maintain the recorder on a Linux VPS.

**Which machine am I on?** Every command in this document runs 🖥️ **on the
capture VPS** unless it is explicitly labelled 💻 **ON THE ANALYSIS HOST**.
Only the "Handing data back to analysis" section mixes the two, and every
code block there is labelled.

## Installing on a Linux server

**Prerequisites:**
- Ubuntu 22.04+ or similar Linux (x86_64)
- Python 3.8+
- Bash
- `systemd` (standard on Ubuntu, CentOS, Debian, etc.)
- ~100 GB disk (provisioned, not necessarily full)
- Outbound HTTPS (port 443) to `ws.kraken.com`

**Steps (as root or with `sudo`):**

```bash
# 1. Clone or extract this bundle to your server
git clone https://github.com/YOUR_ORG/kraken_recorder /opt/kraken_recorder
cd /opt/kraken_recorder

# 2. Install Python dependencies
python3 -m pip install -r requirements.txt

# 3. Verify the setup
python3 -m recorder.record_kraken_ws selftest
# Output: should say "PASS" or "OK"

# 4. Register and start the systemd service
sudo bash install_systemd_unit.sh \
    --user kraken \
    --python-exe /usr/bin/python3 \
    --book-mode snapshot \
    --snapshot-interval 1.0 \
    --min-free-gb 5.0

# 5. Enable and start
sudo systemctl enable kraken-forward-recorder
sudo systemctl start kraken-forward-recorder

# 6. Verify it's running
systemctl status kraken-forward-recorder
python3 -m recorder.liveness
```

**What `install_systemd_unit.sh` does:**
- Writes `/etc/systemd/system/kraken-forward-recorder.service` (systemd unit)
- Configures the service to auto-start after reboot
- Restarts on crash (with exponential backoff) using `supervise.sh`
- Does NOT start the service yet — you do that in step 5

**Parameters:**
- `--user kraken` — the Linux user the service runs as (create with `useradd -r kraken` if needed)
- `--python-exe` — path to Python 3 binary
- `--book-mode snapshot` — the cadence mode (snapshot = 1 per hour; see README for alternatives)
- `--min-free-gb 5.0` — minimum free space before stopping (protect the OS)

## Cutover — bringing this host into service

If this recorder is replacing one already running somewhere else, the old one
keeps running through steps 1–4. Do not stop it early: an overlap costs
nothing but duplicate shards, and a gap cannot be backfilled — this is a
forward recording with no upstream to re-fetch from.

1. **Install and selftest.** `python3 -m pip install -r requirements.txt`,
   then `python3 -m recorder.record_kraken_ws selftest` must pass.
2. **Install and start supervision** (see "Installing on a Linux server"
   above): `install_systemd_unit.sh`, then
   `sudo systemctl enable --now kraken-forward-recorder`.
3. **Verify healthy before trusting it for anything:**
   ```bash
   python3 -m recorder.liveness                       # must print HEALTHY
   python3 -m recorder.coverage_report --fail-on-gap  # since this host's RECORDER_START
   ```
   Do not proceed on a liveness failure or on an unattested gap. That is
   precisely the silent-failure class this design exists to catch.
4. **Confirm attestation, not just "it's running".** This host's own coverage
   journal must show `RECORDER_START` followed by ongoing `HEARTBEAT_ROLLUP`s
   covering all expected symbols. Let that hold for **hours, not minutes** — a
   fresh process can look healthy for a few minutes before a config mistake
   surfaces. Only then stop the old recorder.
5. **Stop the old recorder cleanly.** Send it a clean stop (`systemctl stop`,
   or Ctrl-C on its console) and confirm exit 0 and a `RECORDER_STOP` record
   in its journal. Never `kill -9` — that forfeits the clean-shutdown
   attestation the whole design exists to produce. The current, not-yet-closed
   hour is not at risk; it is simply not yet compacted, and a later run's
   startup compaction sweep picks up anything orphaned.
6. **Retrieve once, promptly**, to establish the first ledger baseline before
   settling into a routine cadence. See "Handing data back to analysis".

**Rollback**, if this host proves worse: `sudo systemctl stop
kraken-forward-recorder`, confirm a clean `RECORDER_STOP` in the journal,
restart the previous recorder, and retrieve whatever this host captured. A
short-lived capture is retrieved exactly like any other — the manifest and
ledger need no special-casing. Rollback never requires deleting anything on
either host, and `retrieve_shards prune` should not be run until the decision
to stay on this host is final.

## What to monitor

**Health check every 30 minutes:**
```bash
python3 -m recorder.liveness
# Exit 0 = HEALTHY, exit 1 = problem
```

**It sleeps ~70 s by design** — it needs two size readings to tell growth from
stillness. It exits 0 only when all three of these hold:

1. **GROWTH** — new bytes were written between the two readings. This is the
   sum of per-file size *increases* plus the full size of files that appeared,
   never the difference of two totals. The hourly roll starts a fresh shard
   while the old one stops growing, and compaction replaces a large raw shard
   with a much smaller archive, so the total legitimately *falls* once an
   hour. A shrinking total is expected; an absence of new bytes is the
   failure.
2. **FRESH** — the newest record on disk is under 30 s old, and the newest
   journal record is recent.
3. **COVERAGE** — the journal shows an open coverage interval right now, and
   the newest `HEARTBEAT_ROLLUP` is under 150 s old, carries a non-zero
   heartbeat count, and saw every expected symbol.

The last line is `HEALTHY` or `UNHEALTHY` and the exit code matches. Useful
flags: `--window 70` (seconds between readings), `--expect-symbols N`,
`--max-staleness 30`, `--out <dir>`.

**Why file size alone is not the check:** a half-open socket leaves the
process alive, the log quiet, and the shard simply not growing. Size looks
plausible; nothing announces the failure. That is why liveness checks
attestation in the journal, not just bytes on disk.

**What was actually missed, once:** a ~4 h capture hole where the process was
never killed — the OS stopped scheduling it (suspend/freeze) and later resumed
it. There was no crash, no restart, and no closing record, so an
attestation-free model read the whole hole as "continuously covered". A VPS is
far less prone to this than a laptop, but it is the reason
`install_systemd_unit.sh` tells you to check for idle-suspend targets.

**If unhealthy:**
1. Check supervisor log: `tail -50 recorder.log` in the bundle root
2. Check service status: `systemctl status kraken-forward-recorder`
3. Restart if transient: `systemctl restart kraken-forward-recorder`
4. If it persists: see Troubleshooting below

**What was MISSED, as opposed to what is running now:**
```bash
python3 -m recorder.coverage_report --out data/kraken_ws_v2
python3 -m recorder.coverage_report --out data/kraken_ws_v2 --fail-on-gap  # exit 1 on any gap
```
`liveness` answers "is it capturing right now". This answers "what did we
lose", which is the question nobody asks until it is too late to fix.

**Expected behavior:**
- Process is always running (unless you stopped it)
- Socket reconnects within seconds of a disconnect
- New compressed shards appear every hour in `data/kraken_ws_v2/book_d10/` and `trades/`
- Coverage report shows no gaps >10s (brief reconnects are normal)

## Handing data back to analysis

> **Read the machine labels on every code block in this section.**
> Two different machines are involved and the commands are not
> interchangeable:
>
> | Label | Machine | Who runs it |
> |---|---|---|
> | 🖥️ **ON THE CAPTURE VPS** | the server you installed the recorder on | you, the operator |
> | 💻 **ON THE ANALYSIS HOST** | the machine that analyses the data (may be macOS, Linux, or Windows+WSL) | whoever receives the data |
>
> Everything in the rest of this document that is not labelled runs
> 🖥️ **ON THE CAPTURE VPS**. The retrieval tooling
> (`recorder.retrieve_shards`) is an SSH *client*: it is only ever run
> 💻 **ON THE ANALYSIS HOST**, never on the VPS. It ships in this bundle
> only so both ends are known to be the same version.

### Step 1 — create the retrieval user

🖥️ **ON THE CAPTURE VPS**

Retrieval gets its own unprivileged account. It is not `root`, and it is not
the account you log in with.

```bash
# Reuse the same unprivileged user the service already runs as
# (`--user kraken` from the install step). If it does not exist yet:
sudo useradd -r -m -d /home/kraken -s /bin/bash kraken

# It needs to read what the recorder wrote, and nothing else:
sudo chown -R kraken:kraken /opt/kraken_recorder/data

sudo -u kraken mkdir -p /home/kraken/.ssh
sudo -u kraken chmod 700 /home/kraken/.ssh
```

### Step 2 — generate the retrieval key

💻 **ON THE ANALYSIS HOST**

```bash
ssh-keygen -t ed25519 -f ~/.ssh/kraken_vps -C "kraken-retrieval"
cat ~/.ssh/kraken_vps.pub
```

Send the **public** half (`kraken_vps.pub`) to the operator. The private half
never leaves the analysis host.

### Step 3 — install the key, restricted to retrieval only

🖥️ **ON THE CAPTURE VPS**

The key is pinned to `retrieval_command.sh`, the forced command shipped in
this bundle. `command=` means sshd runs *that* no matter what the client
asks for, so this key cannot open a shell, forward a port, or touch anything
outside the capture directory — even if the private key is stolen.

```bash
sudo chmod +x /opt/kraken_recorder/retrieval_command.sh

# Paste the analysis host's PUBLIC key at the end of this single line.
# Note: it is ONE line. The restrictions apply only if they are on the same
# line as the key.
sudo -u kraken tee -a /home/kraken/.ssh/authorized_keys >/dev/null <<'EOF'
command="/opt/kraken_recorder/retrieval_command.sh",no-pty,no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-user-rc ssh-ed25519 AAAA... kraken-retrieval
EOF

sudo -u kraken chmod 600 /home/kraken/.ssh/authorized_keys
```

If the capture directory is not the bundle default
(`/opt/kraken_recorder/data/kraken_ws_v2`), tell the wrapper where it is by
exporting `KRAKEN_RECORDER_OUT` in `/home/kraken/.ssh/environment` (and
setting `PermitUserEnvironment yes` in `sshd_config`), or by editing
`OUT_DIR` at the top of `retrieval_command.sh`.

**What the key is allowed to do — the entire list:**
1. `recorder.retrieval_manifest` against the capture directory
2. `rsync --server --sender` (send only — it cannot write to the VPS)
3. `rm -f` of a **single** `.ndjson.zst` shard inside the capture directory

Anything else — a shell, a different directory, `rm -rf`, deleting the
coverage journal, path traversal — is refused with a logged reason.

### Step 4 — verify access

💻 **ON THE ANALYSIS HOST**

```bash
ssh -i ~/.ssh/kraken_vps kraken@<VPS_IP_OR_DNS> \
    "python3 -m recorder.retrieval_manifest --out /opt/kraken_recorder/data/kraken_ws_v2" | head -c 100
# Expect: the first ~100 characters of a JSON manifest.

# And confirm the restriction actually bites — this MUST fail:
ssh -i ~/.ssh/kraken_vps kraken@<VPS_IP_OR_DNS> "id"
# Expect: "retrieval key: REFUSED (command not on the retrieval whitelist)"
```

If `id` succeeds, the `command=` restriction is not in effect — recheck that
the whole `command="...",no-pty,... ssh-ed25519 AAAA...` entry is on one line.

### Step 5 — pull the data

💻 **ON THE ANALYSIS HOST**

```bash
python3 -m recorder.retrieve_shards pull \
    --host kraken@<VPS_IP_OR_DNS> \
    --remote-out /opt/kraken_recorder/data/kraken_ws_v2 \
    --local-out /path/to/analysis/kraken_ws_v2 \
    --identity ~/.ssh/kraken_vps

# Output:
# pulled 123, verified 123, failed 0, already-confirmed 456
```

Do **not** pass `--remote-module-root` with a restricted key: it makes the
client send `cd ... && ...`, which the forced command refuses. The wrapper
already changes to the bundle root itself.

**What it does:**
- Fetches a manifest of all compacted shards from the server
- Downloads any shards not already confirmed received
- Verifies each shard's SHA256 against the remote manifest
- Records confirmed shards in a local ledger (in `/path/to/analysis/.../_retrieval_ledger.json`)
- Never deletes anything on the server side

### Step 6 — cleanup, only after the pull verified

💻 **ON THE ANALYSIS HOST**

```bash
# Only after data has been safely analyzed and stored elsewhere:
python3 -m recorder.retrieve_shards prune --yes-delete-confirmed-only \
    --host kraken@<VPS_IP_OR_DNS> \
    --remote-out /opt/kraken_recorder/data/kraken_ws_v2 \
    --local-out /path/to/analysis/kraken_ws_v2

# Output:
# deleted 123, skipped (not confirmed) 0, skipped (changed) 0, skipped (local mismatch) 0
```

This deletes shards **on the VPS**, but only ones it re-verifies as already
received intact. The forced command enforces the same boundary independently
on the server side.

## Troubleshooting

### Disk is full (or close)

**The recorder stops at <5 GB free (exit 3).**

```bash
# Check current usage:
df -h /opt/kraken_recorder/data/

# Remove old compressed shards (only if synced elsewhere):
cd /opt/kraken_recorder/data/kraken_ws_v2
find . -name "*.ndjson.zst" -mtime +30 -delete  # shards older than 30 days

# Restart:
systemctl start kraken-forward-recorder

# Or expand the VPS disk and restart
# (VPS provider's console or API)
```

### Process won't start

**Check the supervisor log:**
```bash
tail -100 /opt/kraken_recorder/recorder.log
```

**Common issues:**
- Python/websockets not installed: `python3 -m pip install -r requirements.txt`
- Port 443 blocked: `curl https://ws.kraken.com/v2 2>&1 | head`
- Permissions (if not running as root): `chown -R kraken:kraken /opt/kraken_recorder/data`
- Disk full: `df -h` and `systemctl status kraken-forward-recorder`

### Socket keeps disconnecting

**Brief disconnects (2–10 seconds) are expected and normal.** The recorder reconnects automatically.

**If >1 disconnect per minute:**
- Check network from the VPS: `ping kraken.com` or `curl -v https://wss.kraken.com/v2` (may timeout, that's ok)
- Check if Kraken's service is up: https://status.kraken.com/
- Restart once to see if it's transient: `systemctl restart kraken-forward-recorder`

### systemd service won't enable/start

**Check if systemd is available:**
```bash
systemctl --version
```

**Check service file:**
```bash
cat /etc/systemd/system/kraken-forward-recorder.service
```

**Reload and try again:**
```bash
sudo systemctl daemon-reload
sudo systemctl start kraken-forward-recorder
sudo systemctl status kraken-forward-recorder
```

### No questions — it just stops recording silently

**This should never happen with the supervision policy in place.** If it does:

```bash
# Check if the process is running:
ps aux | grep record_kraken_ws

# If not running:
# 1. Check supervisor log and systemd journal:
journalctl -u kraken-forward-recorder -n 50
tail -100 /opt/kraken_recorder/recorder.log

# 2. Check disk and free space:
df -h /opt/kraken_recorder/data/

# 3. Restart:
systemctl restart kraken-forward-recorder
python3 -m recorder.liveness
```

## Maintenance

**Weekly:**
- `python3 -m recorder.liveness` → should be HEALTHY
- `python3 -m recorder.coverage_report --out data/kraken_ws_v2 | tail -5` → check gap count

**Monthly:**
- Retrieve shard updates (if analyzing)
- Monitor disk: `du -sh data/kraken_ws_v2/`

**Annually:**
- Plan for storage growth: 57 GB/year × 3 years ≈ 171 GB needed
- Review Kraken API changes: https://docs.kraken.com/websockets-v2

## Stopping or pausing

**Clean stop (no data loss):**
```bash
systemctl stop kraken-forward-recorder
```
- Waits for the current hour to close (up to ~1 minute)
- Flushes all open files
- Closes the socket gracefully

**Prevent auto-restart after a crash (for debugging):**
```bash
systemctl set-property kraken-forward-recorder StartLimitAction=none
systemctl stop kraken-forward-recorder
# ... debug ...
systemctl reset-failed kraken-forward-recorder
systemctl start kraken-forward-recorder
```

**Restart after a reboot:**
```bash
systemctl status kraken-forward-recorder
# If not running: systemctl start kraken-forward-recorder
```
