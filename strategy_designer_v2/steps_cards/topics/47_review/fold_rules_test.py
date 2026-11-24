"""Topic 31, three rules tested on past ideas (the operator, 2026-11-24: "test the best 3 in parallel"). No model call.
Population: step 7's follow-ups confirmed by step 5 that have a register record (their size and t by fold:
folds_power.csv); outcome: whether they hold on both unseen periods (where tested), and whether step 6 found them paying.
  T1 (explore on older years, check on newer ones): the idea's effect points its own way (size t > 0) on the newer
     folds, 2022-23 and 2024-25 (folds 1 and 4). Retrospective: step 7 did see those years, so the filter is weaker than
     it would be live.
  T2 (a higher bar for more cases tried): m = the rows step 7 saw in its explorations' results for the parent (each row
     one compared case); the bar = the two-sided 5 % z for m tests (Bonferroni); the idea passes if step 5's t reaches
     it.
  T3: T1 and T2.
Per rule: ideas kept and removed; of each, the share holding on both unseen periods and the share paying.
  python3 topics/47_review/fold_rules_test.py"""
import json, pathlib, re
import numpy as np, pandas as pd
from scipy.stats import norm

HERE = pathlib.Path(__file__).resolve().parent; STEPS = HERE.parents[1]
LINES = {p.name[2]: p for p in STEPS.glob("07?_*")}
fp = pd.read_csv(HERE / "folds_power.csv")
newer = fp[fp.subset.astype(str) == "14"].set_index(["run", "book"]).t.rename("t_newer")
t8 = fp[fp.folds == 4].set_index(["run", "book"]).t.rename("size_t8")
v = pd.read_csv(HERE / "first_ideas.csv").rename(columns={"id": "book", "t": "step5_t"})
d = pd.concat([t8, newer], axis=1).reset_index().merge(v[["run", "book", "generation", "line", "status", "step5_t"]], on=["run", "book"])
d = d[(d.generation > 0) & (d.status == "confirmed")].copy()


def tries(run, book, line):
    bar = book.rsplit("_", 1)[-1]; parent = book[: book.rfind(".")] + "_" + bar
    folder = LINES.get(line)
    if folder is None: return np.nan
    ex = folder / run / parent / "exploration"
    if not ex.is_dir(): return np.nan
    rows = 0
    for f in ex.glob("round_*_result.txt"):
        for l in f.read_text(errors="ignore").splitlines():
            if l.strip() and not l.startswith("##") and re.search(r"-?\d+\.\d+", l) and not re.match(r"^\s*(n|count|slope|mean)\b", l):
                rows += 1
    return rows or np.nan


d["tries"] = [tries(r, b, l) for r, b, l in zip(d.run, d.book, d.line)]
d["bar_t"] = norm.ppf(1 - 0.025 / d.tries.clip(lower=1))
for run, book in zip(d.run, d.book): pass


def outcome(run, book):
    u = STEPS / "orchestration/unseen_test" / run / f"{book}.json"
    hold = None
    if u.exists():
        h = [p.get("holds") for p in json.load(open(u))["periods"].values()]
        hold = None if any(x is None for x in h) else all(h)
    c = STEPS / "06_profitability" / run / "checks" / book / "result.json"
    pays = bool(c.exists() and json.load(open(c)).get("status", "").startswith("profitable"))
    return hold, pays


d[["holds", "pays"]] = [outcome(r, b) for r, b in zip(d.run, d.book)]
d["T1"] = d.t_newer > 0
d["T2"] = d.step5_t >= d.bar_t
d["T3"] = d.T1 & d.T2
d.to_csv(HERE / "fold_rules_test.csv", index=False, float_format="%.4g")
print(f"confirmed follow-ups with a register record: {len(d)}; with the tries counted: {int(d.tries.notna().sum())}; "
      f"unseen-tested: {int(d.holds.notna().sum())}")
print(f"tries per analysis (rows seen): median {d.tries.median():.0f}, quartiles {d.tries.quantile(.25):.0f}-{d.tries.quantile(.75):.0f}; "
      f"the bar t: median {d.bar_t.median():.2f}")
rows = []
for rule in ("T1", "T2", "T3"):
    x = d.dropna(subset=["tries"]) if rule != "T1" else d
    for kept in (True, False):
        y = x[x[rule] == kept]; u = y.holds.dropna()
        rows.append({"rule": rule, "kept": "kept" if kept else "removed", "ideas": len(y),
                     "share_of_ideas": len(y) / max(len(x), 1), "pays": y.pays.mean(),
                     "unseen_tested": len(u), "holds_both_unseen": u.astype(float).mean() if len(u) else np.nan})
print(pd.DataFrame(rows).round(2).to_string(index=False))
