"""ideas_similarities_check: add a paying book to the register and compare it with every other paying book and with holding
(card: orchestration/ideas_similarities_check/card.md; definitions: common/measures.md, "A paying book, and what it shares with the
books we have"). Code only, no model call. It records; it decides nothing.

  python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py RECORD --run NAME_run [--no-compare]
  python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py --all

Why this can't leak: it reads finished records after the fact; it changes no decision of any step.
"""
import argparse, json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FUNC = HERE.parent
STEPS = FUNC.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(STEPS / "common"))
from book_returns import bar_of, book_returns, timeframes_from, HOURS  # noqa: E402
from lib import write_atomic, utc_now  # noqa: E402

REGISTER = FUNC / "register"
MIN_DAYS = 365                     # the window in common: under one year, "not comparable" (operator, 2026-11-21)
READINGS = (("same period", 0), ("new one period ahead", 1), ("new one period behind", -1))   # new[t] with other[t+k]


def paying(run, rid, steps=STEPS):
    """Step 5 confirmed and step 6 profitable enough, read from their own result files."""
    v = steps / "05_verification" / run / "verdicts" / rid / "result.json"
    c = steps / "06_profitability" / run / "checks" / rid / "result.json"
    if not (v.exists() and c.exists()):
        return False
    return json.loads(v.read_text()).get("status") == "confirmed" and json.loads(c.read_text()).get("status", "").startswith("profitable")


def key(run, rid):
    return f"{run}__{rid}"


def larger(bar_a, bar_b):
    return bar_a if HOURS[bar_a] >= HOURS[bar_b] else bar_b


def reading(new, other, k, hours):
    """One reading: the new book's return of each period against the other's return k periods later (k +1: the new
    book one period ahead, the other follows; k -1: one period behind). Pairs are matched on the period's time, so no
    pair spans a gap between windows."""
    o = other.copy()
    o.index = o.index - pd.to_timedelta(hours * k, unit="h")
    pair = pd.concat([new.rename("n"), o.rename("o")], axis=1, join="inner").dropna()
    n = len(pair)
    out = {"periods": n}
    if n < 3 or pair["o"].std() == 0 or pair["n"].std() == 0:
        return {**out, "share_explained": None}
    x, y = pair["o"].to_numpy(), pair["n"].to_numpy()
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    se_a = math.sqrt((res @ res) / (n - 2) * (1 / n + x.mean() ** 2 / ((x - x.mean()) @ (x - x.mean()))))
    r = float(np.corrcoef(x, y)[0, 1])
    return {**out, "share_explained": r * r, "direction": "+" if b >= 0 else "-", "slope": float(b),
            "what_is_left": float(a), "what_is_left_t": float(a / se_a) if se_a > 0 else None}


def compare(new, other, hours):
    """The comparison of two period series on one timeframe (`hours` per period): the window in common, the three
    readings, the largest one's share explained, who leads, direction and what is left."""
    rs = {name: reading(new, other, k, hours) for name, k in READINGS}
    common = pd.concat([new, other], axis=1, join="inner").dropna()
    span_days = len(common) * hours / 24
    win = {"first": str(common.index.min()) if len(common) else None, "last": str(common.index.max()) if len(common) else None,
           "periods": len(common), "days": round(span_days, 1)}
    if span_days < MIN_DAYS:
        return {"window_in_common": win, "comparable": False, "readings": {k: v.get("share_explained") for k, v in rs.items()}}
    ok = {k: v for k, v in rs.items() if v.get("share_explained") is not None}
    if not ok:
        return {"window_in_common": win, "comparable": False, "readings": {}}
    best = max(ok, key=lambda k: ok[k]["share_explained"])
    b = ok[best]
    return {"window_in_common": win, "comparable": True, "share_explained": b["share_explained"], "who_leads": best,
            "direction": b["direction"], "what_is_left": b["what_is_left"], "what_is_left_t": b["what_is_left_t"],
            "readings": {k: v.get("share_explained") for k, v in rs.items()}}


def returns_file(k, root=REGISTER):
    return root / "returns" / f"{k}.csv.gz"


def series(k, timeframe, root=REGISTER, column="book"):
    d = pd.read_csv(returns_file(k, root))
    d = d[d["timeframe"] == timeframe]
    return pd.Series(d[column].to_numpy(float), index=pd.to_datetime(d["period"], unit="s", utc=True)).sort_index().dropna()


def books(root=REGISTER):
    f = root / "books.json"
    return json.loads(f.read_text()) if f.exists() else []


def write_books(rows, root=REGISTER):
    root.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: r["key"])
    write_atomic(root / "books.json", json.dumps(rows, indent=2) + "\n")
    lines = ["# The register of paying books", "",
             "One line per paying book (step 5 confirmed, step 6 profitable enough): definitions in `common/measures.md`;",
             "card: `orchestration/ideas_similarities_check/card.md`. An idea's latest record counts once.", "",
             "| Book | Run | Bar | Coins | Engine (git) | Made (UTC) |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['run']} | {r['bar']} | {len(r['coins'])} | {r['git_sha'][:9]} | {r['made_utc']} |" for r in rows]
    write_atomic(root / "INDEX.md", "\n".join(lines) + "\n")


def add(record, run, root=REGISTER, steps=STEPS):
    """Add a paying book: its period returns on every timeframe it can be compared on, and its line. An idea already in
    the register (the same record id, in another run) is replaced by the record made last."""
    record = Path(record); rid = record.name
    if not paying(run, rid, steps):
        sys.exit(f"{rid}: not a paying book in {run} (step 5 confirmed and step 6 profitable enough are both needed)")
    bar = bar_of(record)
    frames = []
    for tf in timeframes_from(bar):
        d = book_returns(record, tf); d.insert(0, "timeframe", tf)
        if tf != bar:
            d["hold"] = float("nan")          # holding is compared on the book's own bar size only
        frames.append(d)
    m = json.loads(next(record.glob("*/w*/manifest.json")).read_text())
    row = {"key": key(run, rid), "run": run, "id": rid, "bar": bar,
           "coins": sorted(p.name for p in record.iterdir() if p.is_dir()),
           "git_sha": m.get("git_sha", ""), "made_utc": m.get("created_utc", "")[:19], "added_utc": utc_now()}
    rows = [r for r in books(root) if r["id"] != rid or r["made_utc"] > row["made_utc"]]
    if any(r["id"] == rid for r in rows):
        print(f"{rid}: a later record of this idea is already in the register; not added")
        return None
    (root / "returns").mkdir(parents=True, exist_ok=True)
    out = pd.concat(frames, ignore_index=True)
    out["period"] = pd.to_datetime(out["period"], utc=True).astype("int64") // 10**9   # UTC seconds
    out.to_csv(returns_file(row["key"], root), index=False, float_format="%.7g", compression="gzip")   # 7 digits: far below what a share explained shows
    write_books(rows + [row], root)
    return row


def comparison(k, root=REGISTER):
    """The book's comparison with every other book of the register and with holding its own coins."""
    rows = {r["key"]: r for r in books(root)}
    me = rows[k]
    out = {"book": me, "made_utc": utc_now(), "others": []}
    for o in sorted(rows.values(), key=lambda r: r["key"]):
        if o["key"] == k:
            continue
        tf = larger(me["bar"], o["bar"])
        c = compare(series(k, tf, root), series(o["key"], tf, root), HOURS[tf])
        out["others"].append({"other": {"key": o["key"], "id": o["id"], "run": o["run"], "bar": o["bar"], "coins": len(o["coins"])},
                              "comparison_timeframe": tf, **c})
    tf = me["bar"]
    out["against_holding"] = {"comparison_timeframe": tf, **compare(series(k, tf, root), series(k, tf, root, "hold"), HOURS[tf])}
    comp = [o for o in out["others"] if o.get("comparable")]
    out["nearest_relative"] = max(comp, key=lambda o: o["share_explained"]) if comp else None
    return out


def fmt(c):
    if not c.get("comparable"):
        return f"not comparable ({c['window_in_common']['days']} days in common)"
    t = c["what_is_left_t"]
    return (f"share explained {c['share_explained']:.2f}, {c['who_leads']}, direction {c['direction']}, "
            f"what is left {100 * c['what_is_left']:+.4f} % per period (t {t:.2f}), on {c['comparison_timeframe']}, "
            f"{c['window_in_common']['days']:.0f} days in common")


def write_comparison(k, root=REGISTER):
    c = comparison(k, root)
    d = root / "comparisons"; d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / f"{k}.json", json.dumps(c, indent=2, default=str) + "\n")
    n = c["nearest_relative"]
    lines = [f"# {c['book']['id']} ({c['book']['run']}, {c['book']['bar']}): what it shares with the books we have", "",
             f"- Nearest relative: " + (f"{n['other']['id']} ({n['other']['run']}, {n['other']['bar']}): {fmt(n)}" if n else "none comparable"),
             f"- Against holding its coins: {fmt(c['against_holding'])}", "",
             "| Other paying book | Run | Bar | Timeframe | Days in common | Share explained | Who leads | Direction | What is left per period (t) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for o in sorted(c["others"], key=lambda o: -(o.get("share_explained") or -1)):
        if o.get("comparable"):
            lines.append(f"| {o['other']['id']} | {o['other']['run']} | {o['other']['bar']} | {o['comparison_timeframe']} | "
                         f"{o['window_in_common']['days']:.0f} | {o['share_explained']:.2f} | {o['who_leads']} | {o['direction']} | "
                         f"{100 * o['what_is_left']:+.4f} % ({o['what_is_left_t']:.2f}) |")
        else:
            lines.append(f"| {o['other']['id']} | {o['other']['run']} | {o['other']['bar']} | {o['comparison_timeframe']} | "
                         f"{o['window_in_common']['days']:.0f} | not comparable | | | |")
    write_atomic(d / f"{k}.md", "\n".join(lines) + "\n")
    return c


def write_summary(root=REGISTER):
    lines = ["# Comparisons: each paying book's nearest relative", "",
             "| Book | Run | Bar | Nearest relative | Share explained | Who leads | What is left per period (t) | Against holding: share explained |",
             "|---|---|---|---|---|---|---|---|"]
    for r in sorted(books(root), key=lambda r: r["key"]):
        f = root / "comparisons" / f"{r['key']}.json"
        if not f.exists():
            continue
        c = json.loads(f.read_text()); n = c["nearest_relative"]; h = c["against_holding"]
        hs = f"{h['share_explained']:.2f}" if h.get("comparable") else "not comparable"
        if n:
            lines.append(f"| {r['id']} | {r['run']} | {r['bar']} | {n['other']['id']} ({n['other']['bar']}) | {n['share_explained']:.2f} | "
                         f"{n['who_leads']} | {100 * n['what_is_left']:+.4f} % ({n['what_is_left_t']:.2f}) | {hs} |")
        else:
            lines.append(f"| {r['id']} | {r['run']} | {r['bar']} | none comparable | | | | {hs} |")
    write_atomic(root / "COMPARISONS.md", "\n".join(lines) + "\n")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("record", type=Path, nargs="?")
    a.add_argument("--run")
    a.add_argument("--all", action="store_true", help="compare every book of the register again")
    a.add_argument("--no-compare", action="store_true", help="add the book only (to fill the register first)")
    args = a.parse_args()
    if args.all:
        for r in books():
            write_comparison(r["key"])
        write_summary()
        print(f"ideas_similarities_check: {len(books())} books compared")
        return
    if not args.record or not args.run:
        sys.exit("give a record and its --run, or --all")
    row = add(args.record, args.run)
    if row and not args.no_compare:
        c = write_comparison(row["key"]); write_summary()
        n = c["nearest_relative"]
        print(f"{row['id']}: nearest relative " + (f"{n['other']['id']}: {fmt(n)}" if n else "none comparable"))
    elif row:
        print(f"{row['id']}: added to the register")


if __name__ == "__main__":
    main()
