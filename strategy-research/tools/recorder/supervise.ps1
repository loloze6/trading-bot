# Restart supervisor for the Kraken forward recorder.
#
# WHY THIS IS THE HIGHEST-VALUE PIECE OF THE DEPLOY
#   Book-stream gaps are PERMANENTLY UNRECOVERABLE. Kraken publishes no
#   historical L2; there is no endpoint, at any price, that can return the order
#   book as it stood while this process was down. Trades are backfillable, OHLCV
#   is backfillable, the book is not. Every minute of downtime is a minute that
#   does not exist and never will. So the supervisor's job is not tidiness -- it
#   is the difference between a twelve-month capture and a twelve-month capture
#   with holes in it.
#
# WHAT IT DOES *NOT* DO
#   It does not restart after a DISK_GUARD_ABORT (exit 3). That exit means the
#   recorder proved the volume is under its free-space floor and stopped on
#   purpose (see disk_guard.py). Relaunching into a full disk is a loop that
#   burns the remaining space, floods the journal, and hides the real fault. It
#   also does not restart after a clean exit 0 -- an operator who pressed Ctrl-C
#   meant it.
#
#   Restarting after a CRASH is safe and does not erase the gap: the successor
#   writes RECORDER_START carrying its predecessor's last journal position and
#   clean/unclean status, and this script writes a RESTART_BOUNDARY record
#   BETWEEN the two processes carrying the dead one's exit code -- so the
#   downtime surfaces as a bounded, attested UNCAPTURED interval that
#   `python -m recorder.coverage_report` names as `restart`, rather than as
#   silence somebody has to reconstruct from file sizes later.
#
# Usage (from anywhere; the script anchors itself):
#   powershell -ExecutionPolicy Bypass -File recorder\supervise.ps1 `
#       -BookMode snapshot -SnapshotInterval 1.0 -MinFreeGb 5.0
#
# For an unattended deploy, wrap this in Task Scheduler with trigger "At startup"
# and "Restart if the task fails".

[CmdletBinding()]
param(
    # Recorder output directory. Default matches record_kraken_ws.DEFAULT_OUT.
    [string]$Out = "",
    # Free-space floor handed to the recorder's own guard, in decimal GB.
    [double]$MinFreeGb = 5.0,
    # Book cadence. Empty means "do not pass the flag" -> the recorder's
    # compiled-in default (delta) applies. The capture is launched with an
    # EXPLICIT mode; this script never changes what the default is.
    [string]$BookMode = "",
    [double]$SnapshotInterval = 0,
    [double]$Duration = 0,
    # Restart rate cap: at most $MaxRestarts relaunches per rolling window.
    [int]$MaxRestarts = 20,
    [double]$RestartWindowMinutes = 60,
    [double]$BackoffInitialSeconds = 5,
    [double]$BackoffMaxSeconds = 300,
    # A process that stayed up this long is considered healthy; the backoff
    # ladder resets so one bad night does not leave a 5-minute delay in force
    # for the rest of the year.
    [double]$HealthyRunSeconds = 600,
    [string]$PythonExe = "python",
    # Overrides the launched command entirely. Exists so the relaunch and
    # no-relaunch paths can be tested against a stub that exits on demand,
    # without a websocket. Operators do not set this.
    [string[]]$RecorderCommand = @(),
    [string]$LogFile = "",
    # Skip the RESTART_BOUNDARY journal record. Testing only.
    [switch]$NoJournalMark
)

$ErrorActionPreference = "Continue"

# disk_guard.EXIT_DISK_GUARD_ABORT. Pinned here as a literal because this script
# must be able to decide without running Python; test_supervisor.py asserts the
# two stay equal.
$EXIT_DISK_GUARD_ABORT = 3
# This script's own "I gave up" code, distinct from anything the recorder emits.
$EXIT_RESTART_CAP = 4

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$researchRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if ($Out -eq "") {
    $Out = Join-Path $repoRoot "trading-bot\local_data\recorded_reserved\kraken_ws_v2"
}
if (-not (Test-Path $Out)) { New-Item -ItemType Directory -Force -Path $Out | Out-Null }
$Out = (Resolve-Path $Out).Path

if ($LogFile -eq "") {
    $LogFile = Join-Path (Split-Path -Parent $Out) "recorder.log"
}
$logDir = Split-Path -Parent $LogFile
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }

# Numbers must reach argparse as invariant-culture text. This host formats 5.5
# as "5,5" under its current culture, which float() rejects -- a locale-dependent
# crash on the one flag that governs whether the capture stops.
function Fmt([double]$n) {
    return $n.ToString([System.Globalization.CultureInfo]::InvariantCulture)
}

function Write-Log([string]$msg) {
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    $line = "$stamp SUPERVISOR $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding utf8
}

if ($RecorderCommand.Count -gt 0) {
    $recArgs = @($RecorderCommand)
} else {
    $recArgs = @("-m", "recorder.record_kraken_ws", "run")
}
$recArgs += @("--out", $Out,
              "--min-free-gb", (Fmt $MinFreeGb),
              "--log-file", $LogFile)
if ($BookMode -ne "")        { $recArgs += @("--book-mode", $BookMode) }
if ($SnapshotInterval -gt 0) { $recArgs += @("--snapshot-interval", (Fmt $SnapshotInterval)) }
if ($Duration -gt 0)         { $recArgs += @("--duration", (Fmt $Duration)) }

Push-Location $researchRoot
try {
    $restartTimes = New-Object System.Collections.ArrayList
    $attempt = 0
    $backoff = $BackoffInitialSeconds

    Write-Log "start: out=$Out floor=$(Fmt $MinFreeGb)GB cap=$MaxRestarts/$(Fmt $RestartWindowMinutes)min log=$LogFile"

    while ($true) {
        Write-Log "launching: $PythonExe $($recArgs -join ' ')"
        $launchedAt = Get-Date
        & $PythonExe @recArgs
        $code = $LASTEXITCODE
        $ran = ((Get-Date) - $launchedAt).TotalSeconds

        if ($code -eq 0) {
            Write-Log "recorder exited 0 (clean stop) after $([Math]::Round($ran,1))s -- NOT relaunching."
            exit 0
        }
        if ($code -eq $EXIT_DISK_GUARD_ABORT) {
            Write-Log ("recorder exited $code (DISK_GUARD_ABORT) after $([Math]::Round($ran,1))s -- " +
                       "NOT relaunching. The free-space floor was breached and the stop is " +
                       "attested in the coverage journal. Free space on the volume holding " +
                       "$Out, then start again by hand.")
            exit $code
        }

        if ($ran -ge $HealthyRunSeconds) {
            $backoff = $BackoffInitialSeconds
            Write-Log "previous process ran $([Math]::Round($ran,1))s (healthy) -- backoff ladder reset."
        }

        # Rolling-window restart cap. Prune first, then decide, so an old burst
        # cannot keep the supervisor shut down forever.
        $cutoff = (Get-Date).ToUniversalTime().AddMinutes(-$RestartWindowMinutes)
        $kept = New-Object System.Collections.ArrayList
        foreach ($t in $restartTimes) { if ($t -ge $cutoff) { [void]$kept.Add($t) } }
        $restartTimes = $kept

        if ($restartTimes.Count -ge $MaxRestarts) {
            Write-Log ("GIVING UP: $($restartTimes.Count) restarts in the last " +
                       "$(Fmt $RestartWindowMinutes) min reached the cap of $MaxRestarts. " +
                       "Last exit code $code. This is a persistent fault, not a flap -- " +
                       "investigate before restarting; Cloudflare bans ~150 connect " +
                       "attempts per rolling 10 min per IP.")
            exit $EXIT_RESTART_CAP
        }

        $attempt++
        [void]$restartTimes.Add((Get-Date).ToUniversalTime())

        if (-not $NoJournalMark) {
            $reason = "recorder exited $code after $([Math]::Round($ran,1))s; supervisor relaunching"
            & $PythonExe -m recorder.journal_mark restart `
                --out $Out `
                --exit-code $code `
                --attempt $attempt `
                --backoff (Fmt $backoff) `
                --reason $reason
            if ($LASTEXITCODE -ne 0) {
                Write-Log "WARNING: could not write RESTART_BOUNDARY (journal_mark exit $LASTEXITCODE) -- this gap will report as 'crash' or 'unknown' rather than 'restart'."
            }
        }

        Write-Log "restart #$attempt in $(Fmt $backoff)s (exit $code after $([Math]::Round($ran,1))s)"
        Start-Sleep -Seconds $backoff
        $backoff = [Math]::Min($backoff * 2, $BackoffMaxSeconds)
    }
}
finally {
    Pop-Location
}
