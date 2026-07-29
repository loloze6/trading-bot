#!/bin/bash
# build_inventory.sh — Idempotent inventory of strategy-research/ tracked files.
# Optimized: single ls-tree call for all bytes, directory-level git log for aggregates.
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
    # Format: <mode> blob <object> <size> <path>
    path=$NF
    for (i=5; i<NF; i++) path = path " " $(i)  # Handle spaces in paths
    size=$(NF-2)
    print path "\t" size
}' > "$tmp_lstree"

# STEP 2: Separate files into two sets
echo "Separating aggregated and per-file rows..." >&2

# Per-file rows: everything NOT in runs/ or results/
awk '!/^strategy-research\/(runs|results)\// {print}' "$tmp_lstree" > "$tmp_perfile"

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

        # Sum bytes from ls-tree output
        total_bytes=$(grep "^$dir_path/" "$tmp_lstree" | awk '{s+=$NF} END {print s}')

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
exit 0
