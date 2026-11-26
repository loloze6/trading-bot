"""combine, the judge on the unseen coins (card: ../card.md, rule 6; common/unseen_coins.md): a version's portfolio,
unchanged, on each book's unseen-coins record, against alternative (a) and P4's strategies at equal weight.

  python3 orchestration/combine/helper/judge_unseen.py --version NAME

Reads `../portfolios/<version>/portfolio.json` (the books and weights, unchanged) and each book's unseen-coins record
(`04_backtest/<run>/unseen_coins/backtests/<id>/`, made by `orchestration/unseen_test/` with `--coins`). Rule 6 by
combine.py's own portfolio function: coin by coin, the weighted sum of the books' returns, then the mean over the
coins of that day. A book with no unseen coin (its plan tested every coin of the data) or no record adds nothing and
is listed. Writes the entry `unseen_coins` of `../portfolios/<version>/measures.json` and the version's INDEX line.
Why this cannot leak: it reads finished records after the fact; no weight, book or portfolio is changed by what it
reads.
"""
import argparse, json, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import combine as cb  # noqa: E402

COINS = "unseen_coins"


def book_alone(r):
    """The book's own unseen-coins result (orchestration/unseen_test/<run>/<id>.json)."""
    f = cb.STEPS / "orchestration" / "unseen_test" / r["run"] / f"{r['id']}.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    e = d.get("periods", {}).get(COINS)
    if e is None:
        return {"holds": "no record"}
    if not e.get("coins_asked"):
        return {"holds": "none (the plan tested every coin of the data)"}
    return {"holds": {True: "holds", False: "does not hold", None: "no data"}[e["holds"]], "coins": len(e.get("coins") or []),
            "years": e.get("years"), "main": e.get("main"), "in_sample_main": (d.get("in_sample") or {}).get("main"),
            "coin_windows": e.get("coin_windows"), "holding_sharpe": e.get("holding_sharpe"),
            "sharpe": e.get("sharpe"), "step5": e.get("step5"), "step6": e.get("step6")}


def judged(weights, rows):
    day, over = cb.portfolio(weights, rows, COINS)
    used = [k for k in weights if cb.coin_returns(rows[k], COINS) is not None]
    coins = set()
    for k in used:
        coins |= set(cb.coin_returns(rows[k], COINS).index.get_level_values("coin"))
    return {**cb.stats(day), "coins": len(coins), "books_with_record": len(used), "books": len(weights),
            "overlap_share": round(over, 4), "years": f"{day.index.min():%Y}-{day.index.max():%Y}"}


def main():
    a = argparse.ArgumentParser(); a.add_argument("--version", required=True); args = a.parse_args()
    out = cb.FUNC / "portfolios" / args.version
    port = json.loads((out / "portfolio.json").read_text())
    rows = {r["key"]: r for r in json.loads((cb.REG / "books.json").read_text())}
    weights = {b["key"]: b["weight"] for b in port["books"]}
    p1 = pd.read_csv(cb.STEPS / "topics" / "44_review" / "p1_candidates_earning.csv"); p1 = p1[p1.status == "candidate"]
    p4 = {f"{r.run}__{r.id}": 1 / len(p1) for r in p1.itertuples() if f"{r.run}__{r.id}" in rows}
    res = {"this version": judged(weights, rows),
           "alternative (a): the same books at equal weight": judged({k: 1 / len(weights) for k in weights}, rows),
           f"P4: its {len(p4)} strategies at equal weight": judged(p4, rows)}
    v = res["this version"]["sharpe"]
    others = [res[k]["sharpe"] for k in res if k != "this version"]
    outcome = ("O3: v1 does not hold" if v <= 0 else "O1: v1 holds and does better than (a) and P4" if v > max(others)
               else "O2: v1 holds, no better than (a)" if v <= res["alternative (a): the same books at equal weight"]["sharpe"]
               else "v1 holds, above (a) but not above P4")
    alone = {k: book_alone(rows[k]) for k in weights}
    p4_alone = {k: book_alone(rows[k]) for k in p4}
    m = json.loads((out / "measures.json").read_text())
    m[COINS] = {"outcome": outcome, "portfolios": res, "each book alone": alone,
                "P4 books alone": {k: x["holds"] for k, x in p4_alone.items()}}
    cb.write_atomic(out / "measures.json", json.dumps(m, indent=1))
    idx = cb.FUNC / "portfolios" / "INDEX.md"
    lines = idx.read_text().splitlines()
    held = sum(x["holds"] == "holds" for x in alone.values())
    ran = sum(x["holds"] in ("holds", "does not hold") for x in alone.values())
    lines = [(l.rsplit("|", 2)[0] + f"| unseen coins Sharpe {v} ((a) {others[0]}, P4 {others[1]}); {held} of {ran} books hold alone |")
             if l.startswith(f"| {args.version} |") else l for l in lines]
    cb.write_atomic(idx, "\n".join(lines) + "\n")
    print(json.dumps(m[COINS], indent=1))


if __name__ == "__main__":
    main()
