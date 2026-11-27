"""Why so few confirmed ideas pay: every tested idea of nights 7 to 9 (market profiles named), by profile and side.
Reads files only (working tree for nights 7-8, the night 9 branches by git show)."""
import json, re, subprocess, csv, os, statistics as st, collections
REPO = "/home/user/trading-bot"; SC = "strategy_designer_v2/steps_cards"

def git_show(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{SC}/{path}"], cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def local(path):
    p = os.path.join(REPO, SC, path)
    return open(p).read() if os.path.exists(p) else None

RUNS = [(r, None) for r in ["night7_chopreversal_run", "night7_panic_run", "night7_rangefail_run", "night7_steadydecline_run",
        "night8_choppyagitated_run", "night8_choppycalm_run", "night8_fallingagitated_run", "night8_fallingcalm_run",
        "night8_risingagitated_run", "night8_risingcalm_run"]]
RUNS += [(f"night9_{n}_run", f"origin/night9-{n}") for n in
         ["chopagishort", "chopdeep", "chopmonth", "chopstretch", "fallcalmfade", "fallcalmwide"]]

rows = []
for run, ref in RUNS:
    get = (lambda p: git_show(ref, p)) if ref else local
    t = get(f"orchestration/run_idea/{run}/table.json")
    if not t:
        continue
    for r in json.loads(t):
        if not r.get("step5"):
            continue
        b = r["backtest"]
        plan = get(f"03_test_plan/{run}/plans/{b}.md") or ""
        m = re.search(r"^Profile:\s*([a-z ]+?)\s*(\(|$)", plan, re.M)
        prof = m.group(1).strip() if m else "none"
        sd = re.search(r"^Side:\s*(.+)$", plan, re.M)
        side = sd.group(1).lower() if sd else ""
        side = "short" if "short only" in side else "long" if "long only" in side else "both"
        res = get(f"06_profitability/{run}/checks/{b}/result.json")
        chk = get(f"06_profitability/{run}/checks/{b}/check.md") or ""
        meas = {}
        if res:
            for x in json.loads(res).get("measures", []):
                meas[x["measure"]] = (x.get("value"), x.get("passed"))
        yr = re.search(r"Yearly return \| ([+-]?[0-9.]+) %", chk)
        dp = re.search(r"Days in a position \| ([0-9.]+) %", chk)
        rows.append(dict(run=run, id=b, profile=prof, side=side,
                         confirmed=str(r["step5"]).startswith("confirmed"),
                         profitable=str(r.get("step6", "")).startswith("profitable"),
                         meas=meas, yearly=float(yr.group(1)) if yr else None, days=float(dp.group(1)) if dp else None))

def v(r, k):
    x = r["meas"].get(k); return x[0] if x else None
def failed(r):
    return [k for k, (val, ok) in r["meas"].items() if ok is False]

print(f"ideas tested {len(rows)}, confirmed {sum(r['confirmed'] for r in rows)}, confirmed and profitable {sum(r['confirmed'] and r['profitable'] for r in rows)}")
groups = collections.defaultdict(list)
for r in rows:
    trend = next((t for t in ("rising", "falling", "choppy") if t in r["profile"]), "any")
    groups[(trend, r["side"])].append(r)
print("\n| profile trend | side | tested | confirmed | conf+prof | of confirmed: fail Calmar | fail Sharpe-hold | fail mean/day | median days in pos % | median yearly % (conf) | median Calmar (conf) | median Sharpe-hold (conf) |")
for k in sorted(groups):
    g = groups[k]; c = [r for r in g if r["confirmed"]]
    cnp = [r for r in c if not r["profitable"]]
    med = lambda L: round(st.median(L), 2) if L else None
    print(f"| {k[0]} | {k[1]} | {len(g)} | {len(c)} | {sum(r['profitable'] for r in c)} | "
          f"{sum('calmar_min' in failed(r) for r in cnp)}/{len(cnp)} | {sum('sharpe_vs_hold_min' in failed(r) for r in cnp)}/{len(cnp)} | "
          f"{sum('avg_daily_return_min' in failed(r) for r in cnp)}/{len(cnp)} | {med([r['days'] for r in g if r['days'] is not None])} | "
          f"{med([r['yearly'] for r in c if r['yearly'] is not None])} | {med([v(r,'calmar_min') for r in c if v(r,'calmar_min') is not None])} | "
          f"{med([v(r,'sharpe_vs_hold_min') for r in c if v(r,'sharpe_vs_hold_min') is not None])} |")
c = [r for r in rows if r["confirmed"] and r["days"] is not None and v(r, "calmar_min") is not None]
print("\nconfirmed ideas by share of days in a position:")
for lo, hi in ((0, 5), (5, 10), (10, 20), (20, 40), (40, 101)):
    g = [r for r in c if lo <= r["days"] < hi]
    if g:
        print(f"  {lo:>3}-{hi:<3}% days: n {len(g):3}  profitable {sum(r['profitable'] for r in g):3}  median Calmar {st.median([v(r,'calmar_min') for r in g]):.2f}"
              f"  median yearly {st.median([r['yearly'] for r in g if r['yearly'] is not None]):.1f} %  median Sharpe {st.median([v(r,'sharpe_min') for r in g]):.2f}")
json.dump(rows, open("why_by_regime_rows.json", "w"))
