# Operator Handover

Install, run, and maintain the recorder on a Linux VPS.

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

## What to monitor

**Health check every 30 minutes:**
```bash
python3 -m recorder.liveness
# Exit 0 = HEALTHY, exit 1 = problem
```

**If unhealthy:**
1. Check supervisor log: `tail -50 data/kraken_ws_v2/../../../recorder.log`
2. Check service status: `systemctl status kraken-forward-recorder`
3. Restart if transient: `systemctl restart kraken-forward-recorder`
4. If it persists: see Troubleshooting below

**Expected behavior:**
- Process is always running (unless you stopped it)
- Socket reconnects within seconds of a disconnect
- New compressed shards appear every hour in `data/kraken_ws_v2/book_d10/` and `trades/`
- Coverage report shows no gaps >10s (brief reconnects are normal)

## Handing data back to analysis

**Extract compressed shards (automated, on your analysis machine):**

Once the recorder has been running for a while and you want to analyze the data:

```bash
# On the analysis machine (macOS, Linux, Windows with WSL):
python3 -m recorder.retrieve_shards pull \
    --host <VPS_IP_OR_DNS> \
    --remote-out /opt/kraken_recorder/data/kraken_ws_v2 \
    --local-out /path/to/analysis/kraken_ws_v2 \
    --identity ~/.ssh/kraken_vps

# Output:
# pulled 123, verified 123, failed 0, already-confirmed 456
```

**What it does:**
- Fetches a manifest of all compacted shards from the server
- Downloads any shards not already confirmed received
- Verifies each shard's SHA256 against the remote manifest
- Records confirmed shards in a local ledger (in `/path/to/analysis/.../\_retrieval_ledger.json`)
- Never deletes anything on the server side

**Cleanup (after verified OK):**

```bash
# Only after data has been safely analyzed and stored elsewhere:
python3 -m recorder.retrieve_shards prune --yes-delete-confirmed-only \
    --host <VPS_IP_OR_DNS> \
    --remote-out /opt/kraken_recorder/data/kraken_ws_v2 \
    --local-out /path/to/analysis/kraken_ws_v2

# Output:
# deleted 123, skipped (not confirmed) 0, skipped (changed) 0, skipped (local mismatch) 0
```

**Setup SSH key for automation:**
```bash
# On the VPS, as root:
mkdir -p /root/.ssh
cat >> /root/.ssh/authorized_keys <<EOF
ssh-rsa AAAA... analysis_host_public_key
EOF
chmod 600 /root/.ssh/authorized_keys

# On the analysis machine, verify access:
ssh -i ~/.ssh/kraken_vps root@<VPS_IP> "python3 -m recorder.retrieval_manifest --out /opt/kraken_recorder/data/kraken_ws_v2" | head -c 100
```

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
