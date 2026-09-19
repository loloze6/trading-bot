"""
Archive Linear issues matching a simple condition.

Why this exists: Linear's Free plan caps non-archived issues at 250. The
product has no manual "archive" button (web, desktop, or mobile) -- only
auto-archive after a configurable inactivity period. The GraphQL API's
`archiveIssue` mutation works immediately regardless of plan tier, even
though it's not exposed in the UI. This script wraps that mutation.

Usage (always dry-run unless --execute is passed):

    export LINEAR_API_KEY=lin_api_...
    python linear_archive.py --state completed,canceled,duplicate --closed-before 2026-08-31
    python linear_archive.py --state completed,canceled,duplicate --closed-before 2026-08-31 --execute
    python linear_archive.py --ids CUL-34,CUL-142 --execute

See README.md in this folder for the full runbook.
"""

import argparse
import json
import os
import sys
import urllib.request

API_URL = "https://api.linear.app/graphql"


def read_key_file() -> str | None:
    """Read LINEAR_API_KEY=... from a .env file next to this script, if present."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.isfile(env_path):
        return None
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("LINEAR_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def post(query: str, key: str) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": key},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_candidates(key: str, team: str) -> list[dict]:
    """Fetch all non-archived issues for the team. One page (250) is enough
    at this workspace's current scale; raise here rather than silently
    truncate if that ever stops being true."""
    query = (
        '{ issues(filter: { team: { key: { eq: "%s" } }, archivedAt: { null: true } }, first: 250) '
        "{ nodes { id identifier title state { name type } completedAt canceledAt } pageInfo { hasNextPage } } }"
        % team
    )
    result = post(query, key)
    if "errors" in result:
        print("ERROR fetching issues:", json.dumps(result["errors"], indent=2))
        sys.exit(1)
    data = result["data"]["issues"]
    if data["pageInfo"]["hasNextPage"]:
        raise RuntimeError(
            "More than 250 non-archived issues -- this script only fetches one page. "
            "Archive a batch first, then re-run."
        )
    return data["nodes"]


def matches(issue: dict, args) -> bool:
    if args.ids:
        return issue["identifier"] in args.ids
    if args.state and issue["state"]["type"] not in args.state:
        return False
    closed = issue["completedAt"] or issue["canceledAt"]
    if args.closed_before and (not closed or closed[:10] > args.closed_before):
        return False
    if args.closed_after and (not closed or closed[:10] < args.closed_after):
        return False
    return True


def archive(ids_uuids: list[tuple[str, str]], key: str) -> tuple[list[str], list[tuple]]:
    successes, failures = [], []
    batch_size = 20
    for i in range(0, len(ids_uuids), batch_size):
        chunk = ids_uuids[i : i + batch_size]
        parts = [f'a{j}: issueArchive(id: "{uid}") {{ success }}' for j, (_, uid) in enumerate(chunk)]
        result = post("mutation { " + " ".join(parts) + " }", key)
        if "errors" in result:
            failures.append((chunk, result["errors"]))
            continue
        data = result["data"]
        for j, (ident, uid) in enumerate(chunk):
            if data.get(f"a{j}", {}).get("success"):
                successes.append(ident)
            else:
                failures.append((ident, data.get(f"a{j}")))
    return successes, failures


def log_run(args, successes: list[str]) -> None:
    log_path = os.path.join(os.path.dirname(__file__), "linear_archive_log.md")
    from datetime import datetime, timezone

    condition = f"ids={args.ids}" if args.ids else (
        f"state={args.state} closed_before={args.closed_before} closed_after={args.closed_after}"
    )
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"- Condition: {condition}\n")
        f.write(f"- Archived ({len(successes)}): {', '.join(successes)}\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--team", default="CUL", help="Team key (default: CUL)")
    p.add_argument("--state", help="Comma-separated state types, e.g. completed,canceled,duplicate")
    p.add_argument("--closed-before", help="YYYY-MM-DD, inclusive")
    p.add_argument("--closed-after", help="YYYY-MM-DD, inclusive")
    p.add_argument("--ids", help="Comma-separated issue identifiers, e.g. CUL-34,CUL-142 (overrides --state/--closed-*)")
    p.add_argument("--execute", action="store_true", help="Actually archive. Without this, only prints matches.")
    args = p.parse_args()
    args.state = args.state.split(",") if args.state else None
    args.ids = args.ids.split(",") if args.ids else None

    key = os.environ.get("LINEAR_API_KEY") or read_key_file()
    if not key:
        print("Set LINEAR_API_KEY, or put it in a .env file next to this script (see README.md).")
        sys.exit(1)

    issues = fetch_candidates(key, args.team)
    matched = [i for i in issues if matches(i, args)]

    print(f"{len(matched)} issue(s) match:")
    for i in sorted(matched, key=lambda x: x["completedAt"] or x["canceledAt"] or ""):
        closed = i["completedAt"] or i["canceledAt"] or "?"
        print(f"  {i['identifier']} | {i['state']['name']} | {closed} | {i['title'][:60]}")

    if not matched:
        return
    if not args.execute:
        print("\nDry run only. Re-run with --execute to archive these.")
        return

    ids_uuids = [(i["identifier"], i["id"]) for i in matched]
    successes, failures = archive(ids_uuids, key)
    print(f"\nArchived: {len(successes)}  Failed: {len(failures)}")
    if failures:
        print(json.dumps(failures, indent=2, default=str))
    log_run(args, successes)


if __name__ == "__main__":
    main()
