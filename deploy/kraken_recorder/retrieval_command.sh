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
# WHY NOT VENDOR rrsync
#   rrsync solves the adjacent problem -- general-purpose restricted rsync
#   over an arbitrary subtree, both directions -- and this needs one
#   direction, one directory, one file pattern. Three concrete reasons to
#   extend this script instead of pinning the key to rrsync:
#     a) The key cannot be pinned to rrsync anyway. rrsync handles only
#        rsync; the manifest and prune commands still need a dispatcher, so
#        rrsync would be an extra dependency UNDER this script, not instead
#        of it.
#     b) rrsync ships with rsync under GPL-3. Vendoring it into a bundle
#        handed to a third-party operator drags a licence obligation onto
#        the whole handover for a component we would be using at ~5% of its
#        surface.
#     c) It would add a Perl (or, on newer rsync, a second Python) runtime
#        to a bundle whose stated prerequisites are Python 3.8+ and bash.
#   What is borrowed is rrsync's *model*: enumerate allowed options, split
#   the short-option cluster at the protocol `e` marker, deny by default.
#   See the rsync branch below for the observed evidence behind the list.
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

# BOTH SIDES OF THE COMPARISON GET NORMALISED, OR THE COMPARISON IS A LIE.
# `readlink -m` resolves symlinks and `..` without requiring the path to
# exist (so deleting an already-gone shard is still checked rather than
# erroring past the check). Normalising only the target and comparing it
# against a raw $OUT_DIR is the bug this replaces: with the data directory
# on a symlink -- /opt/kraken_recorder/data -> /mnt/big/kraken, which is the
# normal shape once the capture volume is a separate disk -- the target
# resolves to /mnt/big/... while OUT_DIR stayed /opt/..., so every
# legitimate retrieval was denied.
#
# Resolving the target also means a symlink planted INSIDE the capture
# directory that points outside it is denied, because it resolves outside.
# That is deliberate and is the reason -L/--copy-links must stay refused:
# together they keep "under OUT_DIR" true after resolution, not just before.
OUT_DIR_REAL="$(readlink -m -- "$OUT_DIR" 2>/dev/null)" || OUT_DIR_REAL=""
[ -n "$OUT_DIR_REAL" ] || deny "cannot normalise OUT_DIR ($OUT_DIR) -- needs GNU coreutils' readlink -m"

under_out_dir() {
    local real
    real="$(readlink -m -- "$1" 2>/dev/null)" || return 1
    [ -n "$real" ] || return 1
    [ "$real" = "$OUT_DIR_REAL" ] && return 0
    [ "${real#"$OUT_DIR_REAL"/}" != "$real" ]
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
        # ------------------------------------------------------------------
        # ALLOWED-OPTION WHITELIST (rrsync's model, narrowed to one job)
        # ------------------------------------------------------------------
        # Checking only `--server --sender` and the path is not enough: rsync
        # passes the client's options through, and several of them change what
        # the server will hand over. Every option is therefore checked against
        # a list, and anything unlisted is denied.
        #
        # What rsync actually sends was OBSERVED, not guessed -- rsync 3.2.7
        # on Ubuntu 22.04, driven by the exact `rsync -az --checksum` that
        # retrieve_shards.py:153 builds, with -e pointed at a stub that
        # recorded its argv:
        #
        #   rsync --server --sender -logDtprcze.iLsfxCIvu . <path>
        #
        # THE `e` SPLIT IS THE WHOLE TRICK. The cluster is two different
        # things joined together: real options up to the `e`, then an opaque
        # protocol/compat blob from `e` onward. In the baseline above, the
        # blob is `e.iLsfxCIvu` -- note the capital L sitting in it. That L is
        # a compat bit, NOT --copy-links. A naive scan for "L anywhere" would
        # reject every legitimate transfer; a naive "allow every letter" would
        # wave a real -L through. Observed placement of the dangerous ones:
        #
        #   -L (--copy-links)      -> -lLogDtprcze...   L BEFORE the e
        #   -k (--copy-dirlinks)   -> -lkogDtprcze...   k BEFORE the e
        #   -s (--protect-args)    -> -slogDtprcze...   s BEFORE the e
        #   --copy-unsafe-links    -> a separate token after the cluster
        #   --remove-source-files  -> a separate token after the cluster
        #
        # So: validate letters before the `e`, treat the blob as opaque but
        # charset-constrained, and allow NO long options at all (the baseline
        # sends none). -L and -k would let the client read through a symlink
        # out of the capture directory; --remove-source-files would let a
        # *pull* delete on this host. None are on the list, so all are denied.
        [ "${ARGV[1]:-}" = "--server" ]  || deny "only rsync --server --sender is allowed"
        [ "${ARGV[2]:-}" = "--sender" ]  || deny "only the SENDING form of rsync --server is allowed"

        # -logDtprcz, exactly the letters the observed baseline sends.
        RSYNC_ALLOWED_SHORT="logDtprcz"

        n="${#ARGV[@]}"
        # Minimum shape: rsync --server --sender . <path>
        [ "$n" -ge 5 ] || deny "rsync command too short to be a pull"

        # Tail must be `. <path>` -- exactly one source, never a list.
        [ "${ARGV[$((n - 2))]}" = "." ] || deny "expected '. <path>' at the end of the rsync command"
        target="$(strip_quotes "${ARGV[$((n - 1))]}")"

        # Everything between --sender and the trailing `. <path>`.
        i=3
        while [ "$i" -lt "$((n - 2))" ]; do
            tok="${ARGV[$i]}"
            case "$tok" in
                --*)
                    deny "rsync long option '$tok' is not on the retrieval whitelist" ;;
                -*)
                    # Split the cluster at the first `e`.
                    opts="${tok#-}"
                    blob=""
                    case "$opts" in
                        *e*) blob="e${opts#*e}"; opts="${opts%%e*}" ;;
                    esac
                    # The compat blob must look like a compat blob and nothing
                    # else: a dot then plain alphanumerics.
                    if [ -n "$blob" ]; then
                        case "$blob" in
                            e.*[!A-Za-z0-9]*) deny "malformed rsync protocol blob '$blob'" ;;
                            e.*)  ;;
                            e)    ;;
                            *)    deny "malformed rsync protocol blob '$blob'" ;;
                        esac
                    fi
                    # Every real option letter must be on the list.
                    while [ -n "$opts" ]; do
                        c="${opts%"${opts#?}"}"
                        opts="${opts#?}"
                        case "$RSYNC_ALLOWED_SHORT" in
                            *"$c"*) ;;
                            *) deny "rsync option -$c is not on the retrieval whitelist" ;;
                        esac
                    done
                    ;;
                *)
                    deny "unexpected rsync argument '$tok'" ;;
            esac
            i=$((i + 1))
        done

        under_out_dir "$target" || deny "rsync path is outside $OUT_DIR"
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
