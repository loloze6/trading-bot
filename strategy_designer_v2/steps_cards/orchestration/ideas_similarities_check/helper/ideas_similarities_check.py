"""ideas_similarities_check: add a paying book to the register and compare it with every other paying book and with holding
(card: orchestration/ideas_similarities_check/card.md; definitions: common/measures.md, "A paying book, and what it shares with the
books we have"). Code only, no model call. It records; it decides nothing.

  python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py RECORD --run NAME_run [--no-compare]
  python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py --all

Why this can't leak: it reads finished records after the fact; it changes no decision of any step.
"""
import argparse, json, math, re, sys
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


def kind_of(run, rid, steps=STEPS):
    """The kind of book (operator, 2026-11-22): "paying" (step 5 confirmed, step 6 profitable enough), "confirmed" (step 5
    confirmed, step 6 not profitable enough: a real idea whose book does not pay), or None (not a book of the register)."""
    v = steps / "05_verification" / run / "verdicts" / rid / "result.json"
    c = steps / "06_profitability" / run / "checks" / rid / "result.json"
    if not (v.exists() and c.exists()) or json.loads(v.read_text()).get("status") != "confirmed":
        return None
    return "paying" if json.loads(c.read_text()).get("status", "").startswith("profitable") else "confirmed"


def parent_of(rid):
    """The idea a repair was written from (line 7.d: `<parent>.d<n>_<name>_<bar>`), as a record id, or None."""
    m = re.fullmatch(r"(.+)\.d\d+_[a-z0-9-]+_(1h|4h|1d)", rid)
    return f"{m.group(1)}_{m.group(2)}" if m else None


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
    """A paying book's returns are committed (`returns/`); a confirmed book's are kept local (`returns/confirmed/`, ignored by
    git: 89 hourly confirmed books would weigh about 90 MB) and rebuilt from its record when missing."""
    f = root / "returns" / f"{k}.csv.gz"
    return f if f.exists() else root / "returns" / "confirmed" / f"{k}.csv.gz"


def series(k, timeframe, root=REGISTER, column="book"):
    if not returns_file(k, root).exists():
        r = next(r for r in books(root) if r["key"] == k)
        write_returns(STEPS / "04_backtest" / r["run"] / "backtests" / r["id"], r["bar"], returns_file(k, root))
    d = pd.read_csv(returns_file(k, root))
    d = d[d["timeframe"] == timeframe]
    return pd.Series(d[column].to_numpy(float), index=pd.to_datetime(d["period"], unit="s", utc=True)).sort_index().dropna()


def books(root=REGISTER):
    f = root / "books.json"
    rows = json.loads(f.read_text()) if f.exists() else []
    return [{**r, "kind": r.get("kind", "paying")} for r in rows]


def write_returns(record, bar, f):
    """The book's period returns on every timeframe it can be compared on (holding on its own bar size only)."""
    frames = []
    for tf in timeframes_from(bar):
        d = book_returns(record, tf); d.insert(0, "timeframe", tf)
        if tf != bar:
            d["hold"] = float("nan")          # holding is compared on the book's own bar size only
        frames.append(d)
    out = pd.concat(frames, ignore_index=True)
    out["period"] = pd.to_datetime(out["period"], utc=True).astype("int64") // 10**9   # UTC seconds
    f.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(f, index=False, float_format="%.7g", compression="gzip")   # 7 digits: far below what a share explained shows


def write_books(rows, root=REGISTER):
    root.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: r["key"])
    write_atomic(root / "books.json", json.dumps(rows, indent=2) + "\n")
    lines = ["# The register of books", "",
             "One line per paying book (step 5 confirmed, step 6 profitable enough) and per confirmed book whose book does not pay",
             "(operator, 2026-11-22): definitions in `common/measures.md`; card: `orchestration/ideas_similarities_check/card.md`.",
             "An idea's latest record counts once.", "",
             "| Book | Kind | Run | Bar | Coins | Engine (git) | Made (UTC) |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r.get('kind', 'paying')} | {r['run']} | {r['bar']} | {len(r['coins'])} | {r['git_sha'][:9]} | {r['made_utc']} |" for r in rows]
    write_atomic(root / "INDEX.md", "\n".join(lines) + "\n")


def add(record, run, root=REGISTER, steps=STEPS):
    """Add a book of the register: a paying book, or a confirmed book whose book does not pay (operator, 2026-11-22): its
    period returns on every timeframe it can be compared on, and its line. An idea already in the register (the same
    record id, in another run) is replaced by the record made last."""
    record = Path(record); rid = record.name
    kind = kind_of(run, rid, steps)
    if kind is None:
        sys.exit(f"{rid}: not a book of the register in {run} (step 5 confirmed is needed)")
    bar = bar_of(record)
    m = json.loads(next(record.glob("*/w*/manifest.json")).read_text())
    row = {"key": key(run, rid), "run": run, "id": rid, "bar": bar, "kind": kind,
           "coins": sorted(p.name for p in record.iterdir() if p.is_dir()),
           "git_sha": m.get("git_sha", ""), "made_utc": m.get("created_utc", "")[:19], "added_utc": utc_now()}
    rows = [r for r in books(root) if r["id"] != rid or r["made_utc"] > row["made_utc"]]
    if any(r["id"] == rid for r in rows):
        print(f"{rid}: a later record of this idea is already in the register; not added")
        return None
    f = root / "returns" / (f"{row['key']}.csv.gz" if kind == "paying" else f"confirmed/{row['key']}.csv.gz")
    write_returns(record, bar, f)
    write_books(rows + [row], root)
    return row


def comparison(k, root=REGISTER):
    """The book's comparison with every other book of the register and with holding its own coins."""
    rows = {r["key"]: r for r in books(root)}
    me = rows[k]
    out = {"book": me, "made_utc": utc_now(), "others": []}
    parent = parent_of(me["id"])
    for o in sorted(rows.values(), key=lambda r: r["key"]):
        if o["key"] == k or (o["kind"] != "paying" and not (o["run"] == me["run"] and o["id"] == parent)):
            continue        # every book is compared with the paying books; a repair also with its parent
        tf = larger(me["bar"], o["bar"])
        c = compare(series(k, tf, root), series(o["key"], tf, root), HOURS[tf])
        out["others"].append({"other": {"key": o["key"], "id": o["id"], "run": o["run"], "bar": o["bar"], "kind": o["kind"], "coins": len(o["coins"])},
                              "comparison_timeframe": tf, **c})
    tf = me["bar"]
    out["against_holding"] = {"comparison_timeframe": tf, **compare(series(k, tf, root), series(k, tf, root, "hold"), HOURS[tf])}
    comp = [o for o in out["others"] if o.get("comparable") and rows[o["other"]["key"]]["kind"] == "paying"]
    out["nearest_relative"] = max(comp, key=lambda o: o["share_explained"]) if comp else None
    par = [o for o in out["others"] if rows[o["other"]["key"]]["kind"] != "paying" or (rows[o["other"]["key"]]["id"] == parent and o["other"]["run"] == me["run"])]
    out["parent"] = par[0] if par and parent else None
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
    lines = [f"# {c['book']['id']} ({c['book']['run']}, {c['book']['bar']}, {c['book']['kind']}): what it shares with the paying books", "",
             f"- Nearest relative: " + (f"{n['other']['id']} ({n['other']['run']}, {n['other']['bar']}): {fmt(n)}" if n else "none comparable"),
             f"- Against holding its coins: {fmt(c['against_holding'])}",
             *([f"- Against its parent (the idea it repairs), {c['parent']['other']['id']}: {fmt(c['parent'])}"] if c.get("parent") else []), "",
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
    def row_of(r):
        f = root / "comparisons" / f"{r['key']}.json"
        if not f.exists():
            return None
        c = json.loads(f.read_text()); n = c["nearest_relative"]; h = c["against_holding"]
        hs = f"{h['share_explained']:.2f}" if h.get("comparable") else "not comparable"
        if not n:
            return (9, f"| {r['id']} | {r['run']} | {r['bar']} | none comparable | | | | {hs} |")
        return (n["share_explained"], f"| {r['id']} | {r['run']} | {r['bar']} | {n['other']['id']} ({n['other']['bar']}) | {n['share_explained']:.2f} | "
                f"{n['who_leads']} | {100 * n['what_is_left']:+.4f} % ({n['what_is_left_t']:.2f}) | {hs} |")
    head = ["| Book | Run | Bar | Nearest paying book | Share explained | Who leads | What is left per period (t) | Against holding: share explained |",
            "|---|---|---|---|---|---|---|---|"]
    rs = books(root)
    pay = [x for x in (row_of(r) for r in sorted(rs, key=lambda r: r["key"]) if r["kind"] == "paying") if x]
    con = sorted(x for x in (row_of(r) for r in rs if r["kind"] == "confirmed") if x)
    lines = ["# Comparisons: each book's nearest paying book", "", "## Paying books", ""] + head + [l for _, l in pay]
    lines += ["", "## Confirmed books whose book does not pay, the least explained by the paying books first",
              "(real ideas that are not yet a profit; the least explained are the variations the research has found)", ""] + head + [l for _, l in con]
    write_atomic(root / "COMPARISONS.md", "\n".join(lines) + "\n")
    write_matrix(root)


def matrix(root=REGISTER):
    """The similarity matrix of the paying books (common/measures.md): the share explained of every pair, read from their
    comparisons; the books ordered so that similar books sit together (start from the first book, then always the book
    most explained by the last one placed). Returns (ordered books, {(key a, key b): comparison entry})."""
    pay = sorted((r for r in books(root) if r["kind"] == "paying"), key=lambda r: r["key"])
    cell = {}
    for r in pay:
        f = root / "comparisons" / f"{r['key']}.json"
        if f.exists():
            for o in json.loads(f.read_text())["others"]:
                cell[(r["key"], o["other"]["key"])] = o
    share = lambda a, b: (cell.get((a, b)) or {}).get("share_explained") or 0.0
    order, left = [], [r["key"] for r in pay]
    while left:
        nxt = left[0] if not order else max(left, key=lambda k: (share(order[-1], k), -left.index(k)))
        order.append(nxt); left.remove(nxt)
    rows = {r["key"]: r for r in pay}
    return [rows[k] for k in order], cell


def write_matrix(root=REGISTER):
    """`MATRIX.md` (readable: numbered books, the share explained in hundredths, "-" not comparable) and `matrix.csv` (for
    code: one line per pair, with the comparison timeframe, the share, the direction and who leads)."""
    order, cell = matrix(root)
    if not order:
        return
    n = {r["key"]: i + 1 for i, r in enumerate(order)}
    lines = ["# The similarity matrix of the paying books", "",
             "Each cell: the share (in hundredths) of the row book's ups and downs that the column book explains, at the larger",
             "of their two bar sizes (`common/measures.md`); 100 is a copy, 0 unrelated; \"-\": under one year in common. The books",
             "are ordered so that similar books sit together: blocks of high numbers are families. Written by",
             "`orchestration/ideas_similarities_check/` with every summary; `matrix.csv` holds the same for code.", "",
             "| # | Book | Run | Bar |", "|---|---|---|---|"]
    lines += [f"| {n[r['key']]} | {r['id']} | {r['run']} | {r['bar']} |" for r in order]
    lines += ["", "| # | " + " | ".join(str(n[r["key"]]) for r in order) + " |", "|---|" + "---|" * len(order)]
    for r in order:
        vals = []
        for c in order:
            if c["key"] == r["key"]:
                vals.append("·"); continue
            e = cell.get((r["key"], c["key"]))
            vals.append(f"{round(100 * e['share_explained'])}" if e and e.get("comparable") else "-")
        lines.append(f"| **{n[r['key']]}** | " + " | ".join(vals) + " |")
    write_atomic(root / "MATRIX.md", "\n".join(lines) + "\n")
    csv = ["book,other,comparison_timeframe,share_explained,direction,who_leads"]
    for r in order:
        for c in order:
            e = cell.get((r["key"], c["key"]))
            if c["key"] != r["key"] and e and e.get("comparable"):
                csv.append(f"{r['key']},{c['key']},{e['comparison_timeframe']},{e['share_explained']:.4f},{e['direction']},{e['who_leads']}")
    write_atomic(root / "matrix.csv", "\n".join(csv) + "\n")


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
