#!/usr/bin/env bash
#
# Register the Kraken forward recorder's supervisor as a systemd system
# service, so continuous capture survives console close, SSH logout, and
# reboot. Linux equivalent of register_scheduled_task.ps1 -- read that
# script's header for the full "why a registered service, not a bare
# process" reasoning; it applies here too, with one simplification: a
# systemd system service (as opposed to a --user service) is NEVER tied to
# any login session in the first place, so there is no S4U-style special
# case to reach for. Logging off does not touch it because it was never
# inside your session to begin with.
#
# WHAT THIS DOES NOT FIX
#   Same caveat as the Windows RUNBOOK section: this only fixes the
#   console/logoff/reboot failure mode. A VPS is not expected to suspend the
#   way a laptop does, but verify: `systemctl list-units --type=target
#   --all | grep -E 'sleep|suspend'` and, if this distro's image ships any
#   idle-suspend behaviour, mask it:
#     sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
#   The 2026-07-27 ~4h06m gap on the Windows capture was an OS-level
#   suspend, not a process kill -- the same class of fault is worth ruling
#   out here even though it is rare on server images.
#
# THIS SCRIPT DOES NOT TOUCH ANY CURRENTLY RUNNING CAPTURE (Windows or
# otherwise). It only writes and enables a unit; the operator decides when
# to stop whatever is currently capturing and cut over. See
# recorder/RUNBOOK.md "Linux deploy / cutover".
#
# Usage (run as a user with sudo; the unit itself runs as --user below):
#   sudo bash install_systemd_unit.sh \
#       --user kraken --python-exe /usr/bin/python3 \
#       --book-mode snapshot --snapshot-interval 1.0 --min-free-gb 5.0
#
# Then:
#   sudo systemctl enable --now kraken-forward-recorder
#   systemctl status kraken-forward-recorder
#   python3 -m recorder.liveness   # per RUNBOOK.md

set -euo pipefail

SERVICE_NAME="kraken-forward-recorder"
RUN_USER="$(id -un)"
PYTHON_EXE="python3"
BOOK_MODE="snapshot"
SNAPSHOT_INTERVAL="1.0"
MIN_FREE_GB="5.0"
OUT_DIR=""

while [ $# -gt 0 ]; do
    case "$1" in
        --service-name) SERVICE_NAME="$2"; shift 2 ;;
        --user) RUN_USER="$2"; shift 2 ;;
        --python-exe) PYTHON_EXE="$2"; shift 2 ;;
        --book-mode) BOOK_MODE="$2"; shift 2 ;;
        --snapshot-interval) SNAPSHOT_INTERVAL="$2"; shift 2 ;;
        --min-free-gb) MIN_FREE_GB="$2"; shift 2 ;;
        --out) OUT_DIR="$2"; shift 2 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

if [ "$(id -u)" -ne 0 ]; then
    echo "must run as root (writes to /etc/systemd/system) -- try sudo" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# Bundle root is the script dir itself
BUNDLE_ROOT="$SCRIPT_DIR"
SUPERVISE="$BUNDLE_ROOT/supervise.sh"

if [ ! -x "$SUPERVISE" ]; then
    chmod +x "$SUPERVISE" || true
fi
if [ ! -f "$SUPERVISE" ]; then
    echo "supervise.sh not found at $SUPERVISE" >&2
    exit 1
fi

EXEC_ARGS=(--python-exe "$PYTHON_EXE" --book-mode "$BOOK_MODE" \
    --snapshot-interval "$SNAPSHOT_INTERVAL" --min-free-gb "$MIN_FREE_GB")
if [ -n "$OUT_DIR" ]; then
    EXEC_ARGS+=(--out "$OUT_DIR")
fi

UNIT_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

# systemd tokenizes ExecStart with its OWN quoting rules (systemd.service(5)
# "Command lines"), which are shell-like but not shell -- it never invokes
# /bin/sh on this line. So values are quoted here with systemd's own
# double-quote convention (escape backslash and double-quote), not bash's
# printf %q, which would emit bash-only forms like $'...'  that systemd's
# tokenizer does not understand.
sdquote() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '"%s"' "$s"
}

{
    echo "[Unit]"
    echo "Description=Kraken forward recorder supervisor (see $BUNDLE_ROOT/OPERATOR_HANDOVER.md)"
    echo "After=network-online.target"
    echo "Wants=network-online.target"
    echo "StartLimitIntervalSec=600"
    echo "StartLimitBurst=5"
    echo ""
    echo "[Service]"
    echo "Type=simple"
    echo "User=$RUN_USER"
    echo "WorkingDirectory=$BUNDLE_ROOT"
    printf 'ExecStart=/usr/bin/env bash %s' "$(sdquote "$SUPERVISE")"
    for a in "${EXEC_ARGS[@]}"; do
        printf ' %s' "$(sdquote "$a")"
    done
    echo ""
    echo "Restart=on-failure"
    echo "RestartSec=10"
    # supervise.sh already owns the recorder-crash backoff/rate-cap policy
    # internally. This layer only catches the supervisor SCRIPT itself
    # dying unexpectedly (OOM kill, bash fault, host hiccup) -- a different,
    # much rarer failure than anything supervise.sh's own loop handles.
    # Exit 0 (clean stop), 3 (DISK_GUARD_ABORT), and 4 (supervise.sh gave up
    # after its own restart cap) are ALL terminal by policy -- none of them
    # should be retried by systemd either.
    echo "SuccessExitStatus=3 4"
    echo "TimeoutStopSec=30"
    echo "KillMode=control-group"
    echo ""
    echo "[Install]"
    echo "WantedBy=multi-user.target"
} > "$UNIT_PATH"

chmod 644 "$UNIT_PATH"
systemctl daemon-reload

echo "Wrote $UNIT_PATH"
echo "Registered but NOT started. It will not capture until:"
echo "  - the current recorder run elsewhere (Windows or foreground) is stopped, and"
echo "  - you run: sudo systemctl enable --now $SERVICE_NAME"
echo "Verify with: systemctl status $SERVICE_NAME"
echo "         and: $PYTHON_EXE -m recorder.liveness --out $OUT_DIR"
