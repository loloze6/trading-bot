#!/bin/sh
# holdout_date_gate.sh — structural gate against committing holdout-range dates.
#
# WHY THIS EXISTS
#   campaign_data_policy.yaml:holdout_range seals 2026-01-01..2026-06-30. That seal was
#   PROTOCOL-ONLY: nothing mechanically stopped a run from reading, or a commit from
#   publishing, bars inside it. Dispatch W5 found two backtest run directories whose
#   declared range crossed the boundary (holdout_contaminated_runs in the same file).
#   This hook is the mechanical guard the seal never had.
#
# WHAT IT SCANS
#   The CONTENT of every text file in the git INDEX — i.e. exactly what the pending
#   commit would publish, not merely the changed delta. Binary files are skipped by
#   `git grep -I`; the count of files actually examined is printed on every run so that
#   "0 hits" is never confusable with "0 files scanned".
#
# DENY BY DEFAULT
#   The gate FAILS the commit — it does not pass it — whenever it cannot prove a clean
#   scan: missing git/grep, scanner self-test deviation, git grep hard error (exit >1),
#   a missing or unreadable exemption registry, or zero files examined. Silence is
#   never treated as success.
#
# THE EXEMPTION PROBLEM (read before widening anything)
#   A literal "block any 2026-01-01..2026-06-30 date" rule matches 663 files in this
#   repo, and ~99% of those matches are FALSE POSITIVES: they are `created_utc` /
#   `timestamp` / `updated_at` wall-clock authorship stamps. The campaign was actively
#   running during 2026 H1 real time (git log shows commits in 2026-03, -04 and -06),
#   so most artifacts ever written are stamped inside the sealed window. Blocking those
#   would make the gate unusable and guarantee it gets bypassed with --no-verify, which
#   is strictly worse than no gate at all.
#   A date is dangerous when it is MARKET DATA (a bar timestamp, a declared backtest
#   range). It is harmless when it is PROVENANCE (when a file was written) or PROSE
#   (a document naming the holdout window it promises not to touch).
#   So the gate exempts exactly two narrow, enumerated things, and nothing else:
#     1. AUTHORSHIP_KEYS below — a closed list of metadata keys.
#     2. Paths in the exemption registry, each pinned WITH a line count.
#   Anything in a shape not on those lists blocks. New file, new key, new format, or an
#   exempt file gaining even one extra holdout-date line => blocked until a human
#   classifies it. That is the deny-by-default property, preserved.
#
# USAGE
#   sh strategy-research/tools/holdout_date_gate.sh            # scan index (hook mode)
#   sh strategy-research/tools/holdout_date_gate.sh --self-test-only
#   sh strategy-research/tools/holdout_date_gate.sh --report-residual
#       prints "path<TAB>count" for every non-exempt hit, the format the registry uses.
#
# Exit: 0 clean, 1 blocked (hit or scan-not-provable).

set -u

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "HOLDOUT GATE: FAIL — not inside a git repository (deny by default)." >&2
    exit 1
}
cd "$REPO_ROOT" || exit 1

REGISTRY="strategy-research/config/holdout_gate_exemptions.txt"

# The sealed window, 2026-01-01..2026-06-30. Months 01-06 of 2026 are wholly inside it,
# so a month-level match IS the range — no day arithmetic, nothing to get off by one.
# 2026-07-01 onward and 2025-12-31 and earlier cannot match by construction.
PATTERN='2026-0[1-6]-[0-3][0-9]'

# Closed list of provenance keys (see THE EXEMPTION PROBLEM above). Deliberately
# anchored to the key, so a market-data value can never inherit an exemption merely by
# sitting on the same line as one of these words.
AUTHORSHIP_KEYS='"created_utc"[[:space:]]*:|"timestamp"[[:space:]]*:|"updated_at"[[:space:]]*:|"generated_at"[[:space:]]*:|"generated_utc"[[:space:]]*:|"decision_timestamp"[[:space:]]*:|"analysis_timestamp"[[:space:]]*:|^[[:space:]]*(timestamp|created_utc|updated_at|generated_at|generated_utc|review_date|recommendation_date|decision_timestamp|analysis_timestamp)[[:space:]]*:'

GREP=${HOLDOUT_GATE_GREP:-grep}

fail() { echo ""; echo "HOLDOUT GATE: COMMIT BLOCKED — $1" >&2; exit 1; }

# All progress output goes to stderr so that --report-residual emits ONLY machine-
# readable "path<TAB>count" on stdout (the registry format).
info() { echo "$@" >&2; }

# ---------------------------------------------------------------------------
# 1. Scanner self-test. Runs on EVERY invocation, before any real scanning.
#    A scanner that cannot prove it distinguishes 2026-01-01 from 2025-12-31 is not
#    trusted to report the index clean. This also defeats HOLDOUT_GATE_GREP being
#    pointed at a permissive stub: a stub that matches nothing fails the positive
#    control, one that matches everything fails the negative control.
# ---------------------------------------------------------------------------
self_test() {
    command -v "$GREP" >/dev/null 2>&1 || {
        echo "  self-test: scanner '$GREP' not executable" >&2
        return 1
    }

    st_dir=$(mktemp -d 2>/dev/null) || { echo "  self-test: mktemp failed" >&2; return 1; }

    # Positive control: first day of the holdout. MUST match.
    printf 'ts,open\n2026-01-01 00:00:00,1\n' > "$st_dir/positive.csv"
    # Negative control: the day before the seal. MUST NOT match.
    printf 'ts,open\n2025-12-31 23:00:00,1\n' > "$st_dir/negative.csv"
    # Boundary controls: last sealed day must match, first day after must not.
    printf '2026-06-30\n' > "$st_dir/last_sealed.csv"
    printf '2026-07-01\n' > "$st_dir/first_free.csv"

    st_rc=0
    "$GREP" -q -E "$PATTERN" "$st_dir/positive.csv" 2>/dev/null || {
        echo "  self-test: POSITIVE CONTROL FAILED — 2026-01-01 not detected" >&2; st_rc=1; }
    "$GREP" -q -E "$PATTERN" "$st_dir/negative.csv" 2>/dev/null && {
        echo "  self-test: NEGATIVE CONTROL FAILED — 2025-12-31 wrongly detected" >&2; st_rc=1; }
    "$GREP" -q -E "$PATTERN" "$st_dir/last_sealed.csv" 2>/dev/null || {
        echo "  self-test: BOUNDARY FAILED — 2026-06-30 (last sealed day) not detected" >&2; st_rc=1; }
    "$GREP" -q -E "$PATTERN" "$st_dir/first_free.csv" 2>/dev/null && {
        echo "  self-test: BOUNDARY FAILED — 2026-07-01 (outside seal) wrongly detected" >&2; st_rc=1; }

    rm -rf "$st_dir"
    return $st_rc
}

info "HOLDOUT GATE: sealed window 2026-01-01..2026-06-30 (campaign_data_policy.yaml:holdout_range)"
if self_test; then
    info "  self-test: PASS (+2026-01-01 +2026-06-30 / -2025-12-31 -2026-07-01)"
else
    fail "scanner self-test failed — cannot trust a clean result (deny by default)."
fi

[ "${1:-}" = "--self-test-only" ] && { info "HOLDOUT GATE: self-test only, no scan requested."; exit 0; }

# ---------------------------------------------------------------------------
# 2. Enumerate the text files that would be committed, and count them.
# ---------------------------------------------------------------------------
# Pre-initialised so the EXIT trap cannot trip `set -u` on an early failure path.
HITS=""; RESIDUAL=""
FILE_LIST=$(mktemp) || fail "mktemp failed (deny by default)."
trap 'rm -f "$FILE_LIST" "$HITS" "$RESIDUAL" 2>/dev/null' EXIT
git grep --cached -I -l -e '' > "$FILE_LIST" 2>/dev/null
examined=$(wc -l < "$FILE_LIST" | tr -d ' ')

if [ "$examined" -eq 0 ]; then
    fail "0 files examined — the scan did not run (deny by default). A truly empty index is indistinguishable from a broken scanner, so this is treated as failure."
fi
info "  files examined: $examined text files in the index"

# ---------------------------------------------------------------------------
# 3. Scan. git grep exit: 0 = hits, 1 = no hits, >1 = real error (never "clean").
# ---------------------------------------------------------------------------
HITS=$(mktemp) || fail "mktemp failed (deny by default)."
git grep --cached -n -I -E "$PATTERN" > "$HITS" 2>/dev/null
rc=$?
if [ $rc -gt 1 ]; then
    fail "git grep exited $rc (hard error, not 'no matches') — scan unusable (deny by default)."
fi

# ---------------------------------------------------------------------------
# 4. Drop provenance-key lines, then compare what is left against the registry.
# ---------------------------------------------------------------------------
RESIDUAL=$(mktemp) || fail "mktemp failed (deny by default)."
"$GREP" -v -E "$AUTHORSHIP_KEYS" < "$HITS" > "$RESIDUAL" 2>/dev/null
rc=$?
[ $rc -gt 1 ] && fail "authorship filter exited $rc — scan unusable (deny by default)."

if [ "${1:-}" = "--report-residual" ]; then
    cut -d: -f1 < "$RESIDUAL" | sort | uniq -c | awk '{print $2"\t"$1}'
    exit 0
fi

[ -r "$REGISTRY" ] || fail "exemption registry $REGISTRY missing or unreadable — cannot tell an audited exemption from an unreviewed one (deny by default)."

violations=$(mktemp) || fail "mktemp failed (deny by default)."
cut -d: -f1 < "$RESIDUAL" | sort | uniq -c | awk '{print $2"\t"$1}' > "$violations.counts"

# A registered path is allowed AT MOST its registered number of holdout-date lines.
# Gaining even one more re-blocks it: the exemption is pinned to audited content, not
# to the filename.
: > "$violations"
while IFS="$(printf '\t')" read -r path count; do
    [ -z "$path" ] && continue
    allowed=$(awk -F'\t' -v p="$path" '$1==p {print $2; exit}' "$REGISTRY")
    if [ -z "$allowed" ]; then
        echo "$path	$count	NOT REGISTERED" >> "$violations"
    elif [ "$count" -gt "$allowed" ]; then
        echo "$path	$count	EXCEEDS registered $allowed" >> "$violations"
    fi
done < "$violations.counts"

n_res=$(wc -l < "$violations.counts" | tr -d ' ')
n_vio=$(wc -l < "$violations" | tr -d ' ')
info "  holdout-date lines: $(wc -l < "$HITS" | tr -d ' ') total, $(wc -l < "$RESIDUAL" | tr -d ' ') after provenance-key filter, across $n_res file(s)"

if [ "$n_vio" -gt 0 ]; then
    echo ""
    echo "Files carrying unregistered holdout-range dates:" >&2
    while IFS="$(printf '\t')" read -r path count why; do
        echo "  $path  ($count line(s), $why)" >&2
        "$GREP" -n -E "$PATTERN" "$path" 2>/dev/null | "$GREP" -v -E "$AUTHORSHIP_KEYS" | head -3 | sed 's/^/      /' >&2
    done < "$violations"
    rm -f "$violations" "$violations.counts"
    fail "$n_vio file(s) carry dates inside the sealed holdout window. If these are market data, they must not be committed. If they are prose or provenance, register them in $REGISTRY with a reason."
fi
rm -f "$violations" "$violations.counts"

info "HOLDOUT GATE: PASS — $examined files examined, no unregistered holdout-range dates."
exit 0
