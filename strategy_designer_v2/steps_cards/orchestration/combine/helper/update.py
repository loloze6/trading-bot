"""combine, steps 10 and 11 of common/data_use.md (card: ../card.md, "Versions by rule"): a new portfolio version when
the list of candidates changes, built by the card's rules 1 to 5 on each candidate's common record, then measured on
the portfolio coins against holding the same coins (equal weight, the same days); ready for the final test when its
Sharpe is above holding's.

  python3 orchestration/combine/helper/update.py

A candidate: a register book of kind `paying` (books.json) with a common record (data_use.md, step 9): its chart file
`04_backtest/<run>/common/backtests/<plan id>/chart_bars.csv.gz` and its result
`orchestration/common_record/<run>/<plan id>.json`. The list is compared with the last version built by this helper
(`../portfolios/INDEX.md`, each version's `portfolio.json`, its `candidates`); when it differs (and is not empty), the
next version `v<n+1>` is written: `boxes.csv`, `portfolio.json`, `measures.json`, its INDEX line. Otherwise nothing is
written. Prints one line: what it did.
Why this cannot leak: it reads finished records after the fact; each day's profile uses closes up to that day; no
rule reads a result beyond step 6's answer (the book's kind) and the sign of a book's return in its boxes.
"""
import json, re, subprocess, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import boxes as bx  # noqa: E402
import combine as cb  # noqa: E402

COMMON = "common"                                   # the common record's folder under 04_backtest/<run>/
PORTFOLIOS = cb.FUNC / "portfolios"
SECTION = "## Versions by rule, on the common records (common/data_use.md, steps 10 to 12)"
HEADER = ["| Version | Commit | Candidates | Books | Portfolio coins: Sharpe (holding) | Ready | Final test |",
          "|---|---|---|---|---|---|---|"]
HOLDING = "holding the same coins, equal weight, the same days"
VERSION_LINE = re.compile(r"^\| (v\d+\w*) \|")


def record_dir(r, records=COMMON):
    return cb.STEPS / "04_backtest" / r["run"] / records / "backtests" / r["id"]


def has_common_record(r):
    return ((record_dir(r) / "chart_bars.csv.gz").exists()
            and (cb.STEPS / "orchestration" / "common_record" / r["run"] / f"{r['id']}.json").exists())


def candidates(books):
    """Step 10's list: the paying books with a common record, by key."""
    return sorted(r["key"] for r in books if r.get("kind") == "paying" and has_common_record(r))


def versions():
    """Every version listed in INDEX.md, in its order."""
    idx = PORTFOLIOS / "INDEX.md"
    return [m.group(1) for l in (idx.read_text().splitlines() if idx.exists() else []) if (m := VERSION_LINE.match(l))]


def last_list():
    """(the last version built on the common records, its candidates), or (None, None)."""
    for v in reversed(versions()):
        f = PORTFOLIOS / v / "portfolio.json"
        p = json.loads(f.read_text()) if f.exists() else {}
        if "candidates" in p:
            return v, p["candidates"]
    return None, None


def next_name():
    return f"v{max([int(m.group(1)) for v in versions() if (m := re.match(r'v(\d+)', v))] or [0]) + 1}"


def cells(rows, keys, data=bx.DATA):
    """Rule 1 on each candidate's common record: the rows of boxes.csv (boxes.py's reader)."""
    out = []
    for k in keys:
        r = rows[k]
        res = bx.read_book(record_dir(r), data=data)
        if res is None:
            out.append({"key": k, "status": "no record on this machine"}); continue
        for (p, s), v in res["cells"].items():
            out.append({"key": k, "run": r["run"], "id": r["id"], "side": r.get("side"), "profile": p, "box_side": s,
                        **{n: (round(x, 5) if isinstance(x, float) else x) for n, x in v.items()},
                        "in_boxes": (p, s) in res["boxes"], "return_in_boxes": res["return_in_boxes"],
                        "days_held": res["days_held"]})
    return pd.DataFrame(out)


def daily(r, records=COMMON):
    """A book's daily return on a record: the mean over its coins of each coin's return that day."""
    cr = cb.coin_returns(r, records)
    return cr.ret.groupby(level="day").mean().dropna()


def related_on(rows, records=COMMON):
    """Rule 4 on the records' daily returns in place of the register's research returns."""
    def related(a, b):
        j = pd.concat([daily(rows[a], records), daily(rows[b], records)], axis=1, join="inner").dropna()
        return len(j) >= cb.MIN_DAYS and abs(j.corr().iloc[0, 1]) >= cb.RELATED
    return related


def holding(weights, rows, records=COMMON):
    """Holding the coins the portfolio trades, equal weight, on its coin-days: each coin's close-to-close return (read
    from the books' chart files), the mean over the coins of that day."""
    used, close = None, {}
    for k in weights:
        cr = cb.coin_returns(rows[k], records)
        if cr is None:
            continue
        idx = cr.ret.dropna().index
        used = idx if used is None else used.union(idx)
        b = pd.read_csv(record_dir(rows[k], records) / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "close"])
        b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
        b = b.sort_values(["coin", "window", "timestamp"]).groupby(["coin", "window", "day"], as_index=False).last()
        b["ret"] = b.groupby(["coin", "window"]).close.pct_change()
        for coin, g in b.dropna(subset=["ret"]).groupby("coin"):
            close.setdefault(coin, g.drop_duplicates("day").set_index("day").ret)
    if used is None:
        return None
    hold = pd.concat(close, names=["coin", "day"]).swaplevel().reindex(used)
    return hold.groupby(level="day").mean().dropna()


def measure(weights, rows, records=COMMON):
    """Step 11 (and step 12 on the final records): the version against holding the same coins; ready when its Sharpe
    is above holding's."""
    if not weights:
        return {"this version": None, HOLDING: None, "ready": False, "why": "no book admitted"}
    day, over = cb.portfolio(weights, rows, records)
    hold = holding(weights, rows, records)
    same = day.index.intersection(hold.index)                 # the same days for both
    day, hold = day.loc[same], hold.loc[same]
    coins = sorted({c for k in weights if (cr := cb.coin_returns(rows[k], records)) is not None
                    for c in cr.index.get_level_values("coin")})
    v, h = cb.stats(day), cb.stats(hold)
    return {"this version": {**v, "overlap_share": round(over, 4), "coins": coins,
                             "years": f"{day.index.min():%Y}-{day.index.max():%Y}"},
            HOLDING: h, "ready": bool(v["sharpe"] > h["sharpe"])}


def index_line(name, sha, n_cand, n_books, m, final="not made"):
    v, h = m["this version"], m[HOLDING]
    sharpe = f"{v['sharpe']} ({h['sharpe']})" if v else "-"
    return f"| {name} | {sha[:10]} | {n_cand} | {n_books} | {sharpe} | {'ready' if m['ready'] else 'not ready'} | {final} |"


def write_index_line(name, line):
    """The version's line in INDEX.md's section of versions by rule (the section added after the older table)."""
    idx = PORTFOLIOS / "INDEX.md"
    lines = idx.read_text().splitlines() if idx.exists() else ["# Portfolio versions (every version tried stays listed)"]
    if SECTION not in lines:
        lines += ["", SECTION, ""] + HEADER
    if any(l.startswith(f"| {name} |") for l in lines):
        lines = [line if l.startswith(f"| {name} |") else l for l in lines]
    else:
        lines.append(line)
    cb.write_atomic(idx, "\n".join(lines) + "\n")


def build(name, keys, rows, data=bx.DATA):
    """Step 10's version from the candidates `keys`, then step 11's measures; writes the version's folder and line."""
    c = cells(rows, keys, data)
    known = c[c.profile.notna()] if "profile" in c.columns else c.iloc[0:0]
    if known.empty:
        weights, boxes, crowd, log = {}, {}, {}, [f"not admitted (no record on this machine): {k}" for k in keys]
    else:
        weights, boxes, crowd, log = cb.choose([rows[k] for k in keys], known, related=related_on(rows))
    out = PORTFOLIOS / name; out.mkdir(parents=True, exist_ok=True)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=cb.STEPS).stdout.strip()
    c.to_csv(out / "boxes.csv", index=False)
    cb.write_atomic(out / "portfolio.json", json.dumps({"version": name, "made_utc": cb.utc_now(), "commit": sha,
        "records": "common", "candidates": list(keys),
        "books": [{"key": k, "weight": round(w, 4), "boxes": [f"{p} {s}" for p, s in boxes[k]]}
                  for k, w in sorted(weights.items(), key=lambda x: (-x[1], x[0]))],
        "box_counts": {f"{p} {s}": n for (p, s), n in sorted(crowd.items())}, "left_out": log}, indent=1))
    m = {"portfolio_coins": measure(weights, rows),
         "ready_rule": f"ready when this version's Sharpe after costs is above {HOLDING} (common/data_use.md, step 11)"}
    m["ready"] = m["portfolio_coins"].pop("ready")
    cb.write_atomic(out / "measures.json", json.dumps(m, indent=1))
    write_index_line(name, index_line(name, sha, len(keys), len(weights), {**m["portfolio_coins"], "ready": m["ready"]}))
    return weights, m


def update(data=bx.DATA):
    """Step 10: the next version when the list of candidates changed; (its name, its measures) or (None, why)."""
    books = json.loads((cb.REG / "books.json").read_text())
    rows = {r["key"]: r for r in books}
    keys = candidates(books)
    if not keys:
        return None, "no candidate has a common record: no version"
    last, before = last_list()
    if before == keys:
        return None, f"the list of candidates ({len(keys)}) is that of {last}: no new version"
    name = next_name()
    _, m = build(name, keys, rows, data)
    return name, m


def main():
    name, m = update()
    if name is None:
        print(f"update: {m}")
    else:
        v = m["portfolio_coins"]["this version"]
        print(f"update: {name} built; {'ready' if m['ready'] else 'not ready'} for the final test"
              + (f" (Sharpe {v['sharpe']}, holding {m['portfolio_coins'][HOLDING]['sharpe']})" if v else ""))


if __name__ == "__main__":
    main()
