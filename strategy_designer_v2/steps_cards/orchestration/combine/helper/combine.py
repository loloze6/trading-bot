"""combine (card: ../card.md): one portfolio version from the register's books, by the card's rules 1 to 6.

  python3 orchestration/combine/helper/combine.py --version NAME

Reads `../boxes.csv` (boxes.py), the register (books.json, the books' daily returns) and each book's record. Writes
`../portfolios/<version>/`: portfolio.json (the books, their boxes and weights), measures.json (in-sample, against
alternative (a) and P4's 20 strategies), and a line in `../portfolios/INDEX.md`. The unseen coins are judged later
(next steps 1u), on the same version.
Why this cannot leak: it reads finished records after the fact; no rule reads a result beyond step 6's answer and the
sign of a book's return in its boxes.
"""
import argparse, json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FUNC = HERE.parent
STEPS = FUNC.parents[1]
REG = STEPS / "orchestration" / "ideas_similarities_check" / "register"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(STEPS / "common"))
import boxes as bx  # noqa: E402
from lib import idea_code, write_atomic, utc_now  # noqa: E402

RELATED = 0.5                  # rule 4: correlation in size at or above it: the same bet
MIN_DAYS = 365                 # under a year of days in common: not comparable (common/measures.md)


def family(r):
    """The brief idea a book descends from, in its run (brief numbers are per run: next steps 3e)."""
    return r["run"], idea_code(r["id"].rsplit("_", 1)[0]).split(".")[0]


def generations(r):
    return idea_code(r["id"].rsplit("_", 1)[0]).count(".")


def daily(key):
    """A book's daily returns (the register's returns file, its 1d rows), one per day."""
    f = REG / "returns" / f"{key}.csv.gz"
    d = pd.read_csv(f)
    d = d[d.timeframe == "1d"]
    return d.groupby("period").book.mean()


def related(a, b):
    j = pd.concat([daily(a), daily(b)], axis=1, join="inner").dropna()
    return len(j) >= MIN_DAYS and abs(j.corr().iloc[0, 1]) >= RELATED


def choose(books, cells):
    """Rules 2 to 5: admitted, one per family, unrelated where they share a box, weights 1 / n."""
    rows = {r["key"]: r for r in books}
    boxes = cells[cells.in_boxes].groupby("key").apply(lambda g: list(zip(g.profile, g.box_side)), include_groups=False).to_dict()
    ret = cells.groupby("key").return_in_boxes.first().to_dict()
    log = []
    adm = [k for k in rows if rows[k]["kind"] == "paying" and k in boxes and (ret.get(k) or 0) > 0]
    log += [f"not admitted (return in its boxes {ret.get(k)}): {k}" for k in rows if rows[k]["kind"] == "paying" and k not in adm]
    fam = {}
    for k in sorted(adm, key=lambda k: (generations(rows[k]), rows[k].get("made_utc", ""))):
        fam.setdefault(family(rows[k]), k)
    kept = set(fam.values())
    log += [f"same family as {fam[family(rows[k])]}: {k}" for k in adm if k not in kept]
    chosen = []
    for k in sorted(kept, key=lambda k: rows[k].get("made_utc", "")):
        clash = next((o for o in chosen if set(boxes[o]) & set(boxes[k]) and related(o, k)), None)
        if clash:
            log.append(f"related to {clash} in a shared box: {k}")
        else:
            chosen.append(k)
    crowd = {}
    for k in chosen:
        for b in boxes[k]:
            crowd[b] = crowd.get(b, 0) + 1
    weights = {k: 1 / max(crowd[b] for b in boxes[k]) for k in chosen}
    return weights, {k: boxes[k] for k in chosen}, crowd, log


def coin_returns(r):
    b = bx.coin_days(STEPS / "04_backtest" / r["run"] / "backtests" / r["id"])
    b["ret"] = b.groupby(["coin", "window"]).value.pct_change()
    return b.set_index(["day", "coin"])[["ret", "position"]]


def portfolio(weights, rows):
    """Rule 6: coin by coin, the weighted sum of the books' returns; then the mean over the coins of that day. Also how
    often, coin-day by coin-day, the weighted positions add up to more than one full position."""
    ret, pos = [], []
    for k, w in weights.items():
        cr = coin_returns(rows[k])
        cr = cr[~cr.index.duplicated()]
        ret.append(cr.ret.rename(k) * w); pos.append(cr.position.abs().rename(k) * w)
    R = pd.concat(ret, axis=1); P = pd.concat(pos, axis=1)
    per_coin = R.sum(axis=1, min_count=1)
    day = per_coin.groupby(level="day").mean().dropna()
    over = (P.sum(axis=1) > 1 + 1e-9).mean()
    return day, over


def stats(r):
    r = r.fillna(0.0)
    c = (1 + r).cumprod(); fall = float((1 - c / c.cummax()).max()); yearly = c.iloc[-1] ** (365 / len(r)) - 1
    return {"days": len(r), "sharpe": round(r.mean() / r.std() * np.sqrt(365), 3), "yearly": round(yearly, 4),
            "worst_fall": round(fall, 4), "calmar": round(yearly / fall, 3) if fall else None}


def main():
    a = argparse.ArgumentParser(); a.add_argument("--version", required=True); args = a.parse_args()
    books = json.loads((REG / "books.json").read_text()); rows = {r["key"]: r for r in books}
    cells = pd.read_csv(FUNC / "boxes.csv")
    cells = cells[cells.profile.notna()]
    weights, boxes, crowd, log = choose(books, cells)
    port, over = portfolio(weights, rows)
    alt_a, over_a = portfolio({k: 1 / len(weights) for k in weights}, rows)
    p1 = pd.read_csv(STEPS / "topics" / "44_review" / "p1_candidates_earning.csv"); p1 = p1[p1.status == "candidate"]
    p4 = {f"{r.run}__{r.id}": 1 / len(p1) for r in p1.itertuples() if f"{r.run}__{r.id}" in rows}
    p4r, over_p4 = portfolio(p4, rows)
    out = FUNC / "portfolios" / args.version; out.mkdir(parents=True, exist_ok=True)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=STEPS).stdout.strip()
    write_atomic(out / "portfolio.json", json.dumps({"version": args.version, "made_utc": utc_now(), "commit": sha,
        "books": [{"key": k, "weight": round(w, 4), "boxes": [f"{p} {s}" for p, s in boxes[k]]} for k, w in sorted(weights.items(), key=lambda x: -x[1])],
        "box_counts": {f"{p} {s}": n for (p, s), n in sorted(crowd.items())}, "left_out": log}, indent=1))
    m = {"in_sample": {"this version": {**stats(port), "overlap_share": round(over, 4)},
                       "alternative (a): the same books at equal weight": {**stats(alt_a), "overlap_share": round(over_a, 4)},
                       f"P4: its {len(p4)} strategies at equal weight": {**stats(p4r), "overlap_share": round(over_p4, 4)}},
         "unseen_coins": "to judge (next steps 1u)"}
    write_atomic(out / "measures.json", json.dumps(m, indent=1))
    idx = FUNC / "portfolios" / "INDEX.md"
    line = f"| {args.version} | {sha[:10]} | {len(weights)} books | in-sample Sharpe {m['in_sample']['this version']['sharpe']} | unseen coins: to judge |"
    lines = idx.read_text().splitlines() if idx.exists() else ["# Portfolio versions (every version tried stays listed)", "", "| Version | Commit | Books | In-sample | Unseen coins |", "|---|---|---|---|---|"]
    write_atomic(idx, "\n".join([l for l in lines if not l.startswith(f"| {args.version} |")] + [line]) + "\n")
    print(json.dumps(m, indent=1)); print(f"{len(weights)} books; left out: {len(log)}")


if __name__ == "__main__":
    main()
