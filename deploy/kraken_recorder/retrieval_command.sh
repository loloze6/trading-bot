#!/usr/bin/env bash
#
# Forced command for the retrieval SSH key.
# ==========================================
#
# The analysis host needs to reach into this machine to fetch capture data.
# It does NOT need a shell here, and it does not need root. This script is
# what the retrieval key is pinned to in authorized_keys:
#
#   command="/opt/kraken_recorder/retrieval_command.sh",no-pty,\
#   no-port-forwarding,no-agent-forwarding,no-X11-forwarding ssh-ed25519 AAAA...
#
# With that entry, sshd ignores whatever the client asked to run and executes
# THIS instead, passing the client's request in $SSH_ORIGINAL_COMMAND. So a
# stolen retrieval key buys the attacker exactly the three operations below
# against exactly one directory -- not a login shell, not the OS, not the
# recorder service, and not root.
#
# WHY A WHITELIST AND NOT A RESTRICTED SHELL
#   `retrieve_shards.py` issues three remote commands and no others:
#     1. the manifest      python3 -m recorder.retrieval_manifest --out DIR
#     2. the bytes         rsync --server --sender ...   (server SENDS only)
#     3. the prune delete  rm -f DIR/<shard>
#   Anything else is refused. `--sender` is load-bearing on line 2: the
#   receiving form of rsync --server would let the client WRITE here, which
#   would turn a retrieval key into a remote-file-write primitive.
#
# THE DELETE IS THE DANGEROUS ONE, SO IT IS THE NARROWEST
#   Only a single literal path, only under $OUT_DIR, only ending
#   `.ndjson.zst`, never the coverage journal, never a glob, never -r. This
#   holds even if `retrieve_shards.py`'s own triple-verify were bypassed
#   entirely -- the two checks are independent on purpose.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
BUNDLE_ROOT="$SCRIPT_DIR"

# Must match --remote-out on the analysis host. Override per-install by
# exporting KRAKEN_RECORDER_OUT in the retrieval user's environment.
OUT_DIR="${KRAKEN_RECORDER_OUT:-$BUNDLE_ROOT/data/kraken_ws_v2}"
OUT_DIR="${OUT_DIR%/}"

JOURNAL_FILENAME="_session.ndjson"

deny() {
    printf 'retrieval key: REFUSED (%s)\n' "$1" >&2
    printf 'retrieval key: requested: %s\n' "${SSH_ORIGINAL_COMMAND:-<none>}" >&2
    exit 1
}

CMD="${SSH_ORIGINAL_COMMAND:-}"
[ -n "$CMD" ] || deny "this key has no interactive shell"

# No shell metacharacters, anywhere. Everything the client legitimately sends
# is a flat argv; refusing these means the word-split below cannot be turned
# into command injection, and lets us exec an array instead of eval'ing text.
case "$CMD" in
    *';'*|*'|'*|*'&'*|*'`'*|*'$('*|*'>'*|*'<'*|*'*'*|*'?'*|*'['*|*$'\n'*|*$'\r'*)
        deny "shell metacharacter in command" ;;
esac

strip_quotes() {
    local s="$1"
    s="${s%\'}"; s="${s#\'}"
    s="${s%\"}"; s="${s#\"}"
    printf '%s' "$s"
}

# True if $1 resolves to a path at or below $OUT_DIR. readlink -m normalises
# without requiring existence, so a delete of an already-gone shard is still
# checked rather than erroring past the check.
under_out_dir() {
    local p real
    p="$1"
    case "$p" in *..*) return 1 ;; esac
    real="$(readlink -m -- "$p" 2>/dev/null)" || return 1
    [ "$real" = "$OUT_DIR" ] && return 0
    [ "${real#"$OUT_DIR"/}" != "$real" ]
}

# NOTE ON --remote-module-root: setting it makes `retrieve_shards.py` send
# `cd <root> && python3 -m ...`, which the `&&` rejection above refuses. Do
# not pass it when using this key -- it is not needed, because the manifest
# branch below cd's to the bundle root itself. OPERATOR_HANDOVER.md says so
# at the point of use.
#
# Paths containing whitespace are not supported (the split below is on
# whitespace). Install the bundle somewhere without spaces in the path.
read -ra ARGV <<< "$CMD"
[ "${#ARGV[@]}" -gt 0 ] || deny "empty command"

case "${ARGV[0]}" in

    python3|python|/usr/bin/python3)
        # Expected: python3 -m recorder.retrieval_manifest --out DIR
        [ "${#ARGV[@]}" -eq 5 ]                              || deny "unexpected manifest argv length"
        [ "${ARGV[1]}" = "-m" ]                              || deny "only -m recorder.retrieval_manifest is allowed"
        [ "${ARGV[2]}" = "recorder.retrieval_manifest" ]     || deny "only recorder.retrieval_manifest is allowed"
        [ "${ARGV[3]}" = "--out" ]                           || deny "manifest requires --out"
        target="$(strip_quotes "${ARGV[4]}")"
        under_out_dir "$target"                              || deny "manifest --out is outside $OUT_DIR"
        cd "$BUNDLE_ROOT"
        exec python3 -m recorder.retrieval_manifest --out "$OUT_DIR"
        ;;

    rsync)
        # Expected: rsync --server --sender <flags...> . <path>
        [ "${ARGV[1]:-}" = "--server" ]  || deny "only rsync --server --sender is allowed"
        [ "${ARGV[2]:-}" = "--sender" ]  || deny "only the SENDING form of rsync --server is allowed"
        target="$(strip_quotes "${ARGV[$((${#ARGV[@]} - 1))]}")"
        under_out_dir "$target"          || deny "rsync path is outside $OUT_DIR"
        exec "${ARGV[@]}"
        ;;

    rm)
        # Expected: rm -f DIR/<something>.ndjson.zst -- one file, nothing else.
        [ "${#ARGV[@]}" -eq 3 ]      || deny "delete takes exactly one path"
        [ "${ARGV[1]}" = "-f" ]      || deny "only 'rm -f <one shard>' is allowed"
        target="$(strip_quotes "${ARGV[2]}")"
        under_out_dir "$target"      || deny "delete path is outside $OUT_DIR"
        case "$target" in
            *.ndjson.zst) ;;
            *) deny "only compacted .ndjson.zst shards may be deleted" ;;
        esac
        [ "$(basename -- "$target")" != "$JOURNAL_FILENAME" ] \
            || deny "the coverage journal is never deletable over this key"
        exec rm -f -- "$target"
        ;;

    *)
        deny "command not on the retrieval whitelist"
        ;;
esac
