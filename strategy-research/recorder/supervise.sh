#!/usr/bin/env bash
#
# Restart supervisor for the Kraken forward recorder -- Linux port of
# supervise.ps1. SAME POLICY, different host. Read supervise.ps1's header
# first; the reasoning there (why this is the highest-value piece of the
# deploy, what it does NOT do, why a crash is safe to relaunch and a
# DISK_GUARD_ABORT is not) is not repeated here and still applies verbatim.
#
# Usage (from anywhere; the script anchors itself via its own path):
#   bash recorder/supervise.sh --book-mode snapshot --snapshot-interval 1.0 \
#       --min-free-gb 5.0
#
# For an unattended deploy, run this under the systemd unit in this same
# directory (kraken-forward-recorder.service) rather than a bare shell.
#
# CONTRACT WITH supervise.ps1 (see tests/test_supervisor.py /
# tests/test_supervisor_sh.py -- both scripts are exercised against the same
# stub-recorder behaviour):
#   - exit 0 (clean stop)         -> do not relaunch
#   - exit 3 (DISK_GUARD_ABORT)   -> do not relaunch
#   - any other exit              -> relaunch, bounded exponential backoff
#   - restart-rate cap per rolling window -> give up, exit 4
#   - a RESTART_BOUNDARY journal record is written between the dead process
#     and its successor, carrying the dead process's exit code
#   - a run that stayed up >= HEALTHY_RUN_SECONDS resets the backoff ladder

set -u

# disk_guard.EXIT_DISK_GUARD_ABORT. Pinned here as a literal because this
# script must be able to decide without running Python; test_supervisor_sh.py
# asserts the two stay equal.
EXIT_DISK_GUARD_ABORT=3
# This script's own "I gave up" code, distinct from anything the recorder
# emits. Matches supervise.ps1's EXIT_RESTART_CAP.
EXIT_RESTART_CAP=4

OUT=""
MIN_FREE_GB=5.0
BOOK_MODE=""
SNAPSHOT_INTERVAL=0
DURATION=0
MAX_RESTARTS=20
RESTART_WINDOW_MINUTES=60
BACKOFF_INITIAL_SECONDS=5
BACKOFF_MAX_SECONDS=300
HEALTHY_RUN_SECONDS=600
PYTHON_EXE="python3"
RECORDER_COMMAND=""
LOG_FILE=""
NO_JOURNAL_MARK=0

usage() {
    echo "Usage: supervise.sh [--out DIR] [--min-free-gb N] [--book-mode MODE]"
    echo "  [--snapshot-interval N] [--duration N] [--max-restarts N]"
    echo "  [--restart-window-minutes N] [--backoff-initial-seconds N]"
    echo "  [--backoff-max-seconds N] [--healthy-run-seconds N]"
    echo "  [--python-exe PATH] [--recorder-command 'CMD ARGS...']"
    echo "  [--log-file PATH] [--no-journal-mark]"
    exit 2
}

while [ $# -gt 0 ]; do
    case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --min-free-gb) MIN_FREE_GB="$2"; shift 2 ;;
        --book-mode) BOOK_MODE="$2"; shift 2 ;;
        --snapshot-interval) SNAPSHOT_INTERVAL="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        --max-restarts) MAX_RESTARTS="$2"; shift 2 ;;
        --restart-window-minutes) RESTART_WINDOW_MINUTES="$2"; shift 2 ;;
        --backoff-initial-seconds) BACKOFF_INITIAL_SECONDS="$2"; shift 2 ;;
        --backoff-max-seconds) BACKOFF_MAX_SECONDS="$2"; shift 2 ;;
        --healthy-run-seconds) HEALTHY_RUN_SECONDS="$2"; shift 2 ;;
        --python-exe) PYTHON_EXE="$2"; shift 2 ;;
        --recorder-command) RECORDER_COMMAND="$2"; shift 2 ;;
        --log-file) LOG_FILE="$2"; shift 2 ;;
        --no-journal-mark) NO_JOURNAL_MARK=1; shift ;;
        -h|--help) usage ;;
        *) echo "unknown argument: $1" >&2; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." >/dev/null 2>&1 && pwd)"
RESEARCH_ROOT="$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"

if [ -z "$OUT" ]; then
    OUT="$REPO_ROOT/trading-bot/local_data/recorded_reserved/kraken_ws_v2"
fi
mkdir -p "$OUT"
OUT="$(cd "$OUT" >/dev/null 2>&1 && pwd)"

if [ -z "$LOG_FILE" ]; then
    LOG_FILE="$(dirname "$OUT")/recorder.log"
fi
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    local stamp
    stamp="$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)"
    local line="$stamp SUPERVISOR $1"
    echo "$line"
    echo "$line" >> "$LOG_FILE"
}

# Float helpers (bash arithmetic is integer-only; awk gives us portable
# float math without depending on python being importable mid-crash-loop).
fmin() { awk -v a="$1" -v b="$2" 'BEGIN { print (a < b) ? a : b }'; }
fmul() { awk -v a="$1" -v b="$2" 'BEGIN { print a * b }'; }
fge()  { awk -v a="$1" -v b="$2" 'BEGIN { exit !(a >= b) }'; }
fgt()  { awk -v a="$1" -v b="$2" 'BEGIN { exit !(a > b) }'; }

if [ -n "$RECORDER_COMMAND" ]; then
    # shellcheck disable=SC2206
    REC_ARGS=($RECORDER_COMMAND)
else
    REC_ARGS=(-m recorder.record_kraken_ws run)
fi
REC_ARGS+=(--out "$OUT" --min-free-gb "$MIN_FREE_GB" --log-file "$LOG_FILE")
if [ -n "$BOOK_MODE" ]; then
    REC_ARGS+=(--book-mode "$BOOK_MODE")
fi
if fgt "$SNAPSHOT_INTERVAL" 0; then
    REC_ARGS+=(--snapshot-interval "$SNAPSHOT_INTERVAL")
fi
if fgt "$DURATION" 0; then
    REC_ARGS+=(--duration "$DURATION")
fi

cd "$RESEARCH_ROOT" || exit 1

restart_times=()
attempt=0
backoff="$BACKOFF_INITIAL_SECONDS"

log "start: out=$OUT floor=${MIN_FREE_GB}GB cap=$MAX_RESTARTS/${RESTART_WINDOW_MINUTES}min log=$LOG_FILE"

while true; do
    log "launching: $PYTHON_EXE ${REC_ARGS[*]}"
    launched_at=$(date +%s.%N)
    "$PYTHON_EXE" "${REC_ARGS[@]}"
    code=$?
    ended_at=$(date +%s.%N)
    ran=$(awk -v a="$launched_at" -v b="$ended_at" 'BEGIN { printf "%.3f", b - a }')

    if [ "$code" -eq 0 ]; then
        log "recorder exited 0 (clean stop) after ${ran}s -- NOT relaunching."
        exit 0
    fi
    if [ "$code" -eq "$EXIT_DISK_GUARD_ABORT" ]; then
        log "recorder exited $code (DISK_GUARD_ABORT) after ${ran}s -- NOT relaunching. The free-space floor was breached and the stop is attested in the coverage journal. Free space on the volume holding $OUT, then start again by hand."
        exit "$code"
    fi

    if fge "$ran" "$HEALTHY_RUN_SECONDS"; then
        backoff="$BACKOFF_INITIAL_SECONDS"
        log "previous process ran ${ran}s (healthy) -- backoff ladder reset."
    fi

    # Rolling-window restart cap. Prune first, then decide, so an old burst
    # cannot keep the supervisor shut down forever.
    now_epoch=$(date -u +%s)
    cutoff=$(awk -v n="$now_epoch" -v m="$RESTART_WINDOW_MINUTES" 'BEGIN { printf "%d", n - m * 60 }')
    kept=()
    for t in ${restart_times[@]+"${restart_times[@]}"}; do
        if [ "$t" -ge "$cutoff" ]; then
            kept+=("$t")
        fi
    done
    restart_times=(${kept[@]+"${kept[@]}"})

    if [ "${#restart_times[@]}" -ge "$MAX_RESTARTS" ]; then
        log "GIVING UP: ${#restart_times[@]} restarts in the last ${RESTART_WINDOW_MINUTES} min reached the cap of $MAX_RESTARTS. Last exit code $code. This is a persistent fault, not a flap -- investigate before restarting; Cloudflare bans ~150 connect attempts per rolling 10 min per IP."
        exit "$EXIT_RESTART_CAP"
    fi

    attempt=$((attempt + 1))
    restart_times+=("$(date -u +%s)")

    if [ "$NO_JOURNAL_MARK" -eq 0 ]; then
        reason="recorder exited $code after ${ran}s; supervisor relaunching"
        "$PYTHON_EXE" -m recorder.journal_mark restart \
            --out "$OUT" \
            --exit-code "$code" \
            --attempt "$attempt" \
            --backoff "$backoff" \
            --reason "$reason"
        if [ $? -ne 0 ]; then
            log "WARNING: could not write RESTART_BOUNDARY (journal_mark failed) -- this gap will report as 'crash' or 'unknown' rather than 'restart'."
        fi
    fi

    log "restart #$attempt in ${backoff}s (exit $code after ${ran}s)"
    sleep "$backoff"
    backoff=$(fmin "$(fmul "$backoff" 2)" "$BACKOFF_MAX_SECONDS")
done
