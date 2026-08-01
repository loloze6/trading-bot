# Register the Kraken forward recorder's supervisor as a Windows Scheduled Task,
# so continuous capture survives console close, user logoff, and reboot.
#
# WHY A SCHEDULED TASK, NOT A DETACHED PROCESS
#   A detached process (Start-Process -WindowStyle Hidden, or
#   [Diagnostics.Process]::Start with no window) still lives inside the user's
#   logon session. It survives closing the ONE console that launched it, but a
#   full logoff tears down the session and everything in it — this was
#   confirmed by inspection: as deployed 2026-07-27, the recorder ran as a bare
#   `python -m recorder.record_kraken_ws run` (PID checked live, no supervisor
#   at all) parented directly by a VS Code integrated-terminal PowerShell host,
#   itself parented by the VS Code process. Closing that terminal — or the VS
#   Code window, or logging off — tears down that whole parent chain and the
#   recorder with it. A Scheduled Task with LogonType S4U runs in its own
#   session, detached from any interactive logon, and a `-AtStartup` trigger
#   means it comes back after a reboot with no operator action.
#
# WHAT THIS DOES NOT FIX
#   System sleep suspends every process on the machine, task-launched or not —
#   there is no Scheduled Task setting that keeps a running task's process
#   alive-and-ticking through S3/modern-standby sleep. The one real gap found
#   in the 2026-07-27 capture (~4h06m, 16:42:20Z-20:48:45Z, see coverage_report
#   / SESSION_LOG for 2026-07-27) shows the signature of exactly this: the
#   journal recorded ZERO heartbeat rollups for the entire gap (heartbeats are
#   a local asyncio task independent of the network, so their absence means the
#   process was not merely disconnected, it was not scheduled by the OS at
#   all), and the SAME process (same PID, same run_id, no successor
#   RECORDER_START) simply resumed afterwards, which a hard kill could not
#   produce. That is a sleep/suspend signature, not a process-kill signature.
#   Fix the actual cause with the power settings below; this task registration
#   only fixes the console/logoff/reboot failure mode.
#
# OPERATOR COMMAND (run once, as the account that should own the task; elevate
# if -LogonType Password is used instead of the S4U default):
#
#   powershell -ExecutionPolicy Bypass -File recorder\register_scheduled_task.ps1 `
#       -BookMode snapshot -SnapshotInterval 1.0 -MinFreeGb 5.0
#
# Then, separately, disable sleep on AC power so the task's process is never
# suspended by the OS while plugged in (elevated prompt):
#
#   powercfg /change standby-timeout-ac 0
#   powercfg /change hibernate-timeout-ac 0
#
# Verify: `Get-ScheduledTask -TaskName KrakenForwardRecorder | Get-ScheduledTaskInfo`
# and `python -m recorder.liveness` per RUNBOOK.md §4.
#
# THIS SCRIPT DOES NOT TOUCH ANY CURRENTLY RUNNING CAPTURE. It only registers a
# task definition; the operator decides when to stop the current foreground run
# and let the task own the next launch.

[CmdletBinding()]
param(
    [string]$TaskName = "KrakenForwardRecorder",
    [string]$Out = "",
    [double]$MinFreeGb = 5.0,
    [string]$BookMode = "snapshot",
    [double]$SnapshotInterval = 1.0,
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

$researchRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$supervisePath = Join-Path $PSScriptRoot "supervise.ps1"
if (-not (Test-Path $supervisePath)) {
    throw "supervise.ps1 not found at $supervisePath"
}

$argList = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$supervisePath`"",
    "-BookMode", $BookMode,
    "-SnapshotInterval", $SnapshotInterval,
    "-MinFreeGb", $MinFreeGb
)
if ($Out -ne "") { $argList += @("-Out", "`"$Out`"") }

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument ($argList -join " ") -WorkingDirectory $researchRoot

# AtStartup: comes back after a reboot with no operator action. AtLogOn is
# intentionally NOT also registered — two triggers would race two supervisor
# instances (and two recorders) against the same output directory.
$trigger = New-ScheduledTaskTrigger -AtStartup

# S4U runs independent of any interactive session (survives logoff) without
# needing the account password stored. RunLevel Highest matches what an
# interactively-launched capture would have had.
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType S4U -RunLevel Highest

# AllowStartIfOnBatteries / DontStopIfGoingOnBatteries: the default Task
# Scheduler behaviour stops a running task when the machine switches to
# battery, which would silently reproduce the same kind of gap this task
# exists to close. ExecutionTimeLimit zero: this task must never be killed for
# running "too long" -- it is meant to run for the life of the capture.
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Principal $principal -Settings $settings -Force `
    -Description ("Kraken forward recorder supervisor. Registered by " +
                  "register_scheduled_task.ps1 -- see strategy-research/recorder/RUNBOOK.md " +
                  "section 'Console survival' before changing.") | Out-Null

Write-Host "Registered scheduled task '$TaskName'. It will not start capturing until:"
Write-Host "  - the current foreground/manual recorder run is stopped by the operator, and"
Write-Host "  - the task is started once by hand (Start-ScheduledTask -TaskName $TaskName) or the machine reboots."
Write-Host "Remember: this does not prevent system sleep. Run the powercfg commands in this script's header too."
