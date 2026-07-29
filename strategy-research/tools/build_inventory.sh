#!/bin/bash
# build_inventory.sh — Idempotent inventory of strategy-research/ tracked files.
# Optimized: single ls-tree call for all bytes, directory-level git log for aggregates.
#
# EXCLUDED PATHS (infrastructure, not subjects):
#   - strategy-research/docs/INVENTORY.tsv (this generator's output)
#   - strategy-research/docs/REFERENCE_MAP.tsv (future index; exclude prospectively)
#   - strategy-research/tools/build_inventory.sh (this script itself)
# These are excluded because their byte counts carry no information for deciding
# what to archive, and self-description makes the generator non-idempotent.
set -e
cd "$(git rev-parse --show-toplevel)" || exit 1

out="strategy-research/docs/INVENTORY.tsv"
tmp_lstree=$(mktemp)
tmp_perfile=$(mktemp)
tmp_agg=$(mktemp)
trap "rm -f '$tmp_lstree' '$tmp_perfile' '$tmp_agg'" EXIT

# STEP 1: Get all file sizes in one git ls-tree call
echo "Collecting file sizes..." >&2
git ls-tree -r -l HEAD strategy-research | awk '{
    # Format: <mode> <type> <object> <size> TAB <path>
    # Fields 1-4 separated by whitespace: mode type object size
    size = $4
    # Path is everything after the TAB
    match($0, /\t(.*)$/, arr)
    path = arr[1]
    print path "\t" size
}' > "$tmp_lstree"

# STEP 2: Separate files into two sets
echo "Separating aggregated and per-file rows..." >&2

# Per-file rows: everything NOT in runs/, results/, and excluding generator artifacts
awk -F'\t' '$1 !~ /^strategy-research\/(runs|results)\// && $1 !~ /^strategy-research\/docs\/(INVENTORY\.tsv|REFERENCE_MAP\.tsv)$/ && $1 !~ /^strategy-research\/tools\/build_inventory\.sh$/ {print}' "$tmp_lstree" > "$tmp_perfile"

# STEP 3: Process per-file rows (293 files total)
echo "Processing per-file rows..." >&2
{
    echo -e "path\tbytes\text\ttop_dir\tfirst_commit\tlast_commit\tcommit_count\tfile_count"

    while read -r path size; do
        if [[ -z "$path" ]]; then continue; fi

        # Get commit info for this file
        last=$(git log -1 --format=%cs -- "$path" 2>/dev/null | cut -d- -f1-2)
        first=$(git log --format=%cs -- "$path" 2>/dev/null | tail -1 | cut -d- -f1-2)
        count=$(git log --oneline -- "$path" 2>/dev/null | wc -l)

        # Extract extension
        if [[ "$path" == *.* ]]; then
            ext=".${path##*.}"
        else
            ext=""
        fi

        # Extract top_dir
        rest="${path#strategy-research/}"
        if [[ "$rest" == */* ]]; then
            top_dir="${rest%%/*}"
        else
            top_dir="_root"
        fi

        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$path" "$size" "$ext" "$top_dir" "$first" "$last" "$count" "1"
    done < "$tmp_perfile"
} > "$out"

# STEP 4: Process aggregated directories (runs/ and results/)
echo "Processing aggregated directories..." >&2

for dir_type in runs results; do
    base_dir="strategy-research/$dir_type"

    # Get unique immediate subdirectories
    git ls-files "$base_dir/" 2>/dev/null | cut -d/ -f3 | sort -u | grep -v '^$' | while read -r subdir; do
        if [[ -z "$subdir" ]]; then
            continue
        fi

        dir_path="$base_dir/$subdir"

        # Count files in this subdirectory
        file_count=$(git ls-files "$dir_path/" 2>/dev/null | wc -l)

        if [[ $file_count -eq 0 ]]; then
            continue
        fi

        # Sum bytes from ls-tree output (field $2 is size, after TAB)
        total_bytes=$(grep "^$dir_path/" "$tmp_lstree" | awk -F'\t' '{s+=$2} END {print s}')

        # Get commit dates at directory level
        last=$(git log -1 --format=%cs -- "$dir_path/" 2>/dev/null | cut -d- -f1-2)
        first=$(git log --format=%cs -- "$dir_path/" 2>/dev/null | tail -1 | cut -d- -f1-2)
        count=$(git log --oneline -- "$dir_path/" 2>/dev/null | wc -l)

        # Output aggregated row
        rel_path="$dir_type/$subdir/"
        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$rel_path" "$total_bytes" "(dir)" "$dir_type" "$first" "$last" "$count" "$file_count" >> "$out"
    done
done

# Report stats
row_count=$(($(wc -l < "$out") - 1))
echo "Generated $out ($row_count rows)"

# =============================================================================
# STEP 5: REFERENCE_MAP.tsv — who points at each INVENTORY.tsv row
# =============================================================================
# FACTS ONLY. No verdicts, no delete candidates. Classification is a separate
# decision made by the operator, not by this script.
#
# One output row per INVENTORY.tsv row, in INVENTORY.tsv order. Driving the
# output off "$out" is what guarantees the 1:1 row correspondence; do not
# re-derive the subject list from the tree.
#
# DEFINITIONS (mechanical, no judgement)
#
#   PATH PROBE  — the subject path with the leading "strategy-research/" removed,
#                 but ONLY when the remainder still contains a "/". This keeps a
#                 probe path-shaped (>=1 slash) always: root-level files such as
#                 strategy-research/CLAUDE.md keep their prefix rather than
#                 degrading into the bare name "CLAUDE.md", which would collide
#                 with trading-bot/CLAUDE.md. Trailing "/" is stripped so a
#                 directory row matches both "runs/run_004" and
#                 "runs/run_004/artifacts/x". Because the stripped form is a
#                 substring of the full form, one literal probe matches both
#                 prefixed and unprefixed spellings.
#
#   BASENAME PROBE — the file name truncated at its FIRST ".", i.e. all
#                 extensions removed ("research_brief.schema.json" ->
#                 "research_brief"). Dotfiles, where that would leave an empty
#                 string, fall back to the full name. This is deliberately the
#                 loose definition: it is what exposes names that are pipeline
#                 ARTIFACT VOCABULARY rather than references to a file. See the
#                 divergence warning below.
#
#   SELF        — for a file row, the subject referencing itself. For a
#                 directory row, any file INSIDE that directory: a run artifact
#                 naming its own run is self-description, not an inbound
#                 reference, and counting it would swamp the column.
#
#   EXECUTABLE  — *.py, *.sh, anything under tools/hooks/, and *.yaml|*.json
#                 under a config/ or workflow/ directory.
#   PROSE       — *.md.
#   Referrers that are neither (run artifacts, .tsv, .txt, .ps1) are counted in
#   refs_by_path/refs_by_basename but in NEITHER class column, so
#   refs_executable + refs_prose <= the distinct referrer count. That is
#   expected, not a bug.
#
# WARNING — refs_by_path AND refs_by_basename MEASURE DIFFERENT THINGS.
#   They diverge by orders of magnitude for names that are also artifact type
#   names in the pipeline; "expanded_hypothesis_card" matches 266 files, almost
#   none of which reference any FILE by that name. NEVER collapse the two
#   columns, and never present the basename count alone as "references".
#
# CORPUS — every file tracked at HEAD (so .git is excluded by construction),
#   minus the three infrastructure paths excluded above. Binary files are
#   skipped by grep -I.

ref_out="strategy-research/docs/REFERENCE_MAP.tsv"
tmp_probes=$(mktemp)
tmp_puniq=$(mktemp)
tmp_cands=$(mktemp)
tmp_reffiles=$(mktemp)
tmp_reflines=$(mktemp)
trap "rm -f '$tmp_lstree' '$tmp_perfile' '$tmp_agg' '$tmp_probes' '$tmp_puniq' '$tmp_cands' '$tmp_reffiles' '$tmp_reflines'" EXIT

echo "Building probe table..." >&2
awk -F'\t' 'NR>1 {
    p = $1; sub(/\/$/, "", p)
    probe = p
    if (p ~ /^strategy-research\//) {
        rest = p; sub(/^strategy-research\//, "", rest)
        if (rest ~ /\//) probe = rest
    }
    name = p; sub(/.*\//, "", name)
    stem = name; sub(/\..*$/, "", stem)
    if (stem == "") stem = name
    print probe "\tP\t" $1
    print stem  "\tB\t" $1
}' "$out" > "$tmp_probes"
cut -f1 "$tmp_probes" | sort -u > "$tmp_puniq"

# Candidate referrer corpus. NOTE ON ANCHORING: these records are BARE paths
# with no trailing fields, so a ^...$ line-anchored pattern is correct here.
# This is NOT the case for the tab-separated ls-tree data filtered in STEP 2,
# where the same pattern would silently never fire and the filter must be
# field-scoped with -F'\t'. Do not copy one form to the other site.
git ls-files -z \
  | grep -z -v -E '^strategy-research/(docs/(INVENTORY|REFERENCE_MAP)\.tsv|tools/build_inventory\.sh)$' \
  > "$tmp_cands"

# Two-stage search. Stage 1 narrows ~8.8k files to those matching any probe;
# stage 2 extracts only the matching lines. Both greps are `|| true` because
# grep exits 1 on no-match, which xargs turns into 123 and `set -e` would
# treat as fatal; the non-empty checks below are the real failure detection.
echo "Stage 1: locating referrer files..." >&2
xargs -0 -r grep -I -l -F -f "$tmp_puniq" < "$tmp_cands" > "$tmp_reffiles" || true
if [[ ! -s "$tmp_reffiles" ]]; then
    echo "FATAL: no referrer files found; probe table or corpus is broken" >&2
    exit 1
fi

echo "Stage 2: extracting matching lines..." >&2
tr '\n' '\0' < "$tmp_reffiles" \
  | xargs -0 -r grep -I -H -F -f "$tmp_puniq" > "$tmp_reflines" || true
if [[ ! -s "$tmp_reflines" ]]; then
    echo "FATAL: referrer files matched but no lines extracted" >&2
    exit 1
fi

echo "Attributing references..." >&2
awk -v PROBES="$tmp_probes" -v INV="$out" '
function cls(f) {
    if (f ~ /\.py$/ || f ~ /\.sh$/) return "E"
    if (f ~ /(^|\/)tools\/hooks\//) return "E"
    if (f ~ /(^|\/)(config|workflow)\// && f ~ /\.(yaml|json)$/) return "E"
    if (f ~ /\.md$/) return "P"
    return "O"
}
function is_self(s, f,    sf) {
    sf = SF[s]
    if (f == sf) return 1
    if (sf ~ /\/$/ && index(f, sf) == 1) return 1
    return 0
}
BEGIN { FS = "\t" }
FILENAME == PROBES { np++; PR[np] = $1; TY[np] = $2; SU[np] = $3; next }
FILENAME == INV {
    if (FNR == 1) next
    no++; ORD[no] = $1
    sf = $1
    if (sf !~ /^strategy-research\//) sf = "strategy-research/" sf
    SF[$1] = sf
    next
}
{
    # grep -H output: "<path>:<content>". No tracked path can contain ":"
    # (illegal in Windows filenames), so splitting at the first colon is exact.
    ci = index($0, ":")
    if (ci == 0) next
    f = substr($0, 1, ci - 1)
    c = substr($0, ci + 1)
    for (i = 1; i <= np; i++)
        if (index(c, PR[i])) M[SU[i] SUBSEP TY[i] SUBSEP f] = 1
}
END {
    for (k in M) {
        split(k, a, SUBSEP)      # a[1]=subject a[2]=type a[3]=referrer
        uk = a[1] SUBSEP a[3]
        if (!(uk in UN)) { UN[uk] = 1; UL[a[1]] = UL[a[1]] "\n" a[3] }
        if (a[2] == "P") PM[uk] = 1; else BM[uk] = 1
    }
    print "path\trefs_by_path\trefs_by_basename\trefs_executable\trefs_prose\trefs_self\ttop_referrers"
    for (r = 1; r <= no; r++) {
        s = ORD[r]
        np_c = 0; nb_c = 0; ne_c = 0; npr_c = 0; ns_c = 0
        delete strong; delete weak
        nstrong = 0; nweak = 0
        n = split(UL[s], refs, "\n")
        for (j = 1; j <= n; j++) {
            f = refs[j]
            if (f == "") continue
            if (is_self(s, f)) { ns_c++; continue }
            uk = s SUBSEP f
            if (uk in PM) { np_c++; strong[++nstrong] = f } else { weak[++nweak] = f }
            if (uk in BM) nb_c++
            c = cls(f)
            if (c == "E") ne_c++; else if (c == "P") npr_c++
        }
        # Deterministic top_referrers: path matches first (stronger evidence),
        # then basename-only, lexicographic within each group, capped at 3.
        top = ""; ntop = 0
        if (nstrong > 1) asort(strong)
        if (nweak   > 1) asort(weak)
        for (j = 1; j <= nstrong && ntop < 3; j++) { top = (ntop ? top ";" : "") strong[j]; ntop++ }
        for (j = 1; j <= nweak   && ntop < 3; j++) { top = (ntop ? top ";" : "") weak[j];   ntop++ }
        printf "%s\t%d\t%d\t%d\t%d\t%d\t%s\n", s, np_c, nb_c, ne_c, npr_c, ns_c, top
    }
}
' "$tmp_probes" "$out" "$tmp_reflines" > "$ref_out"

ref_rows=$(($(wc -l < "$ref_out") - 1))
echo "Generated $ref_out ($ref_rows rows)"
exit 0
