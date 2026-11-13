"""Orchestrator tool: one row per idea taken through steps 3 to 6 tonight, from the result files (no number typed)."""
import glob, json, re
from pathlib import Path
SC = Path(__file__).resolve().parents[1]
def res(path):
    p = SC / path / "result.json"
    return json.loads(p.read_text()) if p.exists() else None
def v5(o):
    if not o: return ""
    st = (o.get("main_measure") or {}).get("statistic") or {}
    t = st.get("value")
    return f"{o['status']}" + (f" ({t:+.2f})" if isinstance(t, (int, float)) else "")
def v6(o):
    if not o: return ""
    m = {x["measure"]: x["value"] for x in o["measures"]}
    return ("**profitable**" if o["status"] == "profitable enough" else "no") + f" (Sharpe {m['sharpe_min']:.2f}, vs holding {m['sharpe_vs_hold_min']:+.2f}, Calmar {m['calmar_min']:.2f})"
rows = []
ideas = {}
for lin in sorted(SC.glob("overnight_run/gen*/handoff/N*.md")):
    t = lin.read_text(); ideas[lin.stem] = re.search(r"^Idea:\s*(.+)$", t, re.M).group(1)
for nid in sorted(ideas):
    rid = nid + "_1d"
    plan = next((p for d in ("plans_rerun", "plans_newcomp", "plans") for p in [SC / "03_test_plan/overnight_run" / d / f"{rid}.md"] if p.exists()), None)
    outcome = re.search(r"^outcome: (\S+)", plan.read_text(), re.M).group(1) if plan else "no plan"
    s5 = res(f"05_verification/overnight_run/verdicts_used/{rid}") or res(f"05_verification/overnight_run/verdicts/{rid}")
    if nid.startswith("N1-01"):
        s5 = res(f"05_verification/overnight_run/verdicts_fixdesc_1/{rid}")
    s6 = res(f"06_profitability/overnight_run/checks/{rid}")
    o5, o6 = res(f"05_verification/overnight_run/verdicts_oos/{rid}_oos"), res(f"06_profitability/overnight_run/checks_oos/{rid}_oos")
    p5, p6 = res(f"05_verification/overnight_run/verdicts_oos/{rid}_oos2"), res(f"06_profitability/overnight_run/checks_oos/{rid}_oos2")
    rel = [res(f"06_profitability/overnight_run/checks_calmar_vs_hold/{rid}{s}") for s in ("", "_oos", "_oos2")]
    relcol = " / ".join("-" if o is None else ("yes" if o["status"] == "profitable enough" else "no") for o in rel)
    rows.append(f"| {nid} | {ideas[nid][:120]}{'...' if len(ideas[nid]) > 120 else ''} | {outcome if outcome != 'plan' else v5(s5)} | {v6(s6)} | {v5(o5)} {('/ ' + v6(o6)) if o6 else ''} | {v5(p5)} {('/ ' + v6(p6)) if p6 else ''} | {relcol} |")
print("| Idea | In words | Real? (6 coins, 2018-25) | Profitable? (6 coins) | Unseen coins 2022-25: real / profitable | Unseen coins 2018-21: real / profitable | Profitable with Calmar relative to holding (6 coins / unseen 22-25 / unseen 18-21) |")
print("|---|---|---|---|---|---|---|")
print("\n".join(rows))
