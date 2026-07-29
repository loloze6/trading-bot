#!/bin/bash
# build_inventory.sh — Idempotent inventory of strategy-research/ tracked files.
cd "$(git rev-parse --show-toplevel)" || exit 1

out="strategy-research/docs/INVENTORY.tsv"
tmp=$(mktemp)
trap "rm -f '$tmp'" EXIT

echo "path	bytes	ext	top_dir	first_commit	last_commit	commit_count	file_count" > "$out"

# Process each file sequentially
git ls-files strategy-research/ | sort | while read -r path; do
    if [[ -z "$path" ]]; then continue; fi

    bytes=$(git cat-file -s HEAD:"$path")
    last=$(git log -1 --format=%cs -- "$path" | cut -d- -f1-2)
    first=$(git log --format=%cs -- "$path" | tail -1 | cut -d- -f1-2)
    count=$(git log --oneline -- "$path" | wc -l)

    # Check if aggregated directory
    if [[ "$path" == strategy-research/runs/* ]]; then
        dir=$(echo "$path" | sed 's|^strategy-research/runs/\([^/]*\)/.*|\1|')
        echo "runs/$dir/" "$bytes" "$count" "$first" "$last"
    elif [[ "$path" == strategy-research/results/* ]]; then
        dir=$(echo "$path" | sed 's|^strategy-research/results/\([^/]*\)/.*|\1|')
        echo "results/$dir/" "$bytes" "$count" "$first" "$last"
    elif [[ "$path" == strategy-research/quarantine/* ]]; then
        dir=$(echo "$path" | sed 's|^strategy-research/quarantine/\([^/]*\)/.*|\1|')
        echo "quarantine/$dir/" "$bytes" "$count" "$first" "$last"
    else
        # Per-file row
        ext=""
        [[ "$path" == *.* ]] && ext=".${path##*.}"
        rest="${path#strategy-research/}"
        top_dir="_root"
        [[ "$rest" == */* ]] && top_dir="${rest%%/*}"
        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$path" "$bytes" "$ext" "$top_dir" "$first" "$last" "$count" "1" >> "$out"
    fi
done | sort -u | awk '
{
    path=$1; bytes=$2; count=$3; first=$4; last=$5
    if (path in dirs) {
        dirs[path] = dirs[path] "\t" bytes "\t" count "\t" first "\t" last
        bytes_sum[path] += bytes
        count_sum[path] += count
        file_count[path]++
        if (first < first_date[path]) first_date[path] = first
        if (last > last_date[path]) last_date[path] = last
    } else {
        dirs[path] = bytes "\t" count "\t" first "\t" last
        bytes_sum[path] = bytes
        count_sum[path] = count
        file_count[path] = 1
        first_date[path] = first
        last_date[path] = last
    }
}
END {
    for (path in dirs) {
        dir_type = match(path, /^([a-z]+)\//, m) ? m[1] : ""
        if (dir_type) {
            printf "%s\t%s\t(dir)\t%s\t%s\t%s\t%s\t%s\n",
                path, bytes_sum[path], dir_type, first_date[path], last_date[path], count_sum[path], file_count[path]
        }
    }
}' >> "$out"

echo "Generated $out"
