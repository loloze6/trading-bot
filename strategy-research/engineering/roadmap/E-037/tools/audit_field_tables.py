"""Audit every §3 field table against real artifacts on disk."""
import io, re, glob, json, os
import yaml
from collections import Counter

GUIDE = "strategy-research/docs/USER_GUIDE.md"
s = io.open(GUIDE, encoding="utf-8").read()
sec = s[s.index("## 3. Artifacts"): s.index("## 4. Skills")]

# entry -> documented field names (first column, backticked)
entries = re.split(r"\n### ", sec)[1:]
documented = {}
for e in entries:
    head = e.split("\n")[0].strip()
    m = re.search(r"\| Field \|.*\n\|[-| ]+\n((?:\|.*\n)+)", e)
    if not m:
        continue
    fields = []
    for row in m.group(1).strip().split("\n"):
        cell = row.split("|")[1].strip()
        for name in re.findall(r"`([A-Za-z0-9_]+)`", cell):
            fields.append(name)
    if fields:
        documented[head] = fields

# map entry heading -> glob for real instances
def _all_keys(node):
    """Every key at EVERY depth. Top-level-only was the original bug: it reported
    median_sharpe as absent from protocol_result.yaml, where it appears 57 times
    nested. "Not a top-level key" is not the same claim as "does not exist"."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _all_keys(v)
    elif isinstance(node, list):
        for x in node:
            yield from _all_keys(x)


def globs(head):
    m = re.match(r"`([^`]+)`", head)
    if not m:
        return []
    fn = m.group(1)
    if fn.startswith("config/"):
        return ["strategy-research/" + fn]
    return [f"strategy-research/runs/*/artifacts/{fn}",
            f"strategy-research/runs/*/{fn}",
            f"strategy-research/campaign_record/{fn}",
            f"strategy-research/{fn}"]

print(f"{'artifact':44} {'files':>5}  phantom / documented   undocumented-real")
print("-" * 108)
report = {}
for head, fields in documented.items():
    files = []
    for g in globs(head):
        files += glob.glob(g)
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        print(f"{head[:43]:44} {0:>5}  (no instances on disk)")
        continue
    seen = Counter()
    real_keys = set()
    n = 0
    for f in files:
        try:
            d = yaml.safe_load(io.open(f, encoding="utf-8")) if not f.endswith(".json") \
                else json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        n += 1
        file_keys = set(_all_keys(d))
        real_keys |= file_keys
        for k in fields:
            if k in file_keys:      # at ANY depth, not just top level
                seen[k] += 1
    phantom = [k for k in fields if seen[k] == 0]
    undoc = sorted(str(k) for k in real_keys - set(fields))
    report[head] = (n, phantom, undoc)
    flag = "  <== PHANTOM" if phantom else ""
    print(f"{head[:43]:44} {n:>5}  {len(phantom)}/{len(fields)}{' ':18}{len(undoc)}{flag}")
    if phantom:
        print(f"{'':46}   never present: {', '.join(phantom)}")

io.open("_audit_out.json", "w", encoding="utf-8").write(json.dumps(
    {k: {"files": v[0], "phantom": v[1], "undocumented": v[2]} for k, v in report.items()}, indent=1))
print("\nwritten: _audit_out.json")
