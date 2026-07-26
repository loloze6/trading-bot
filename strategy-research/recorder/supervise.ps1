# Restart supervisor for the Kraken forward recorder.
#
# The recorder handles socket-level failures itself (heartbeat watchdog +
# reconnect backoff). This loop exists for the level above that: an unhandled
# crash, an OOM kill, a Python-level fault. Restarting is safe and does NOT
# erase the gap — the successor process writes RECORDER_START carrying its
# predecessor's last journal position and clean/unclean status, so the downtime
# surfaces as a bounded UNCAPTURED interval rather than as continuous coverage
# (see journal.py, and the `test_unclean_restart_closes_at_last_dead_record`
# test).
#
# Usage (from strategy-research/):
#   powershell -ExecutionPolicy Bypass -File recorder\supervise.ps1
#
# For an unattended deploy, wrap this in Task Scheduler with trigger "At startup"
# and "Restart if the task fails".

$ErrorActionPreference = "Continue"
$logDir = Join-Path $PSScriptRoot "..\..\trading-bot\local_data\recorded_reserved"
$log = Join-Path $logDir "recorder.log"
$backoff = 5

while ($true) {
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Add-Content -Path $log -Value "[$stamp] supervisor: starting recorder" -Encoding utf8
    python -m recorder.record_kraken_ws run 2>&1 | Add-Content -Path $log -Encoding utf8
    $code = $LASTEXITCODE
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Add-Content -Path $log -Value "[$stamp] supervisor: recorder exited ($code); restarting in ${backoff}s" -Encoding utf8
    # Fixed, not exponential: Cloudflare bans ~150 connect attempts per rolling
    # 10 min per IP, and 5s is Kraken's own floor after extended downtime.
    Start-Sleep -Seconds $backoff
}
