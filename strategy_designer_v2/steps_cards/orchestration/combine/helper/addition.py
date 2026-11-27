"""combine, what a run adds to the portfolio (card: ../card.md, "What a run adds to the portfolio"; next steps A8):
the portfolio built by the card's rules 1 to 5 on the common records twice, with every candidate and without the
candidates of a run or of a batch (a list of runs), both measured on the same coin-days.

  python3 orchestration/combine/helper/addition.py --runs RUN [RUN ...] [--name NAME]

`--runs`: run names as in the register (a shell pattern such as 'night9_*' names every run it matches). `--name`: the
file's name, needed for a batch (default: the run's name). Prints the table and writes `../additions/<name>.md`, for
the run's reading to quote (runs/NIGHT_RULES.md). It builds no version and writes nothing in `../portfolios/`. The
file holds no date and no commit: the same candidates give the same file.
Why this cannot leak: it reads finished records after the fact; the rules that build both portfolios read no result
beyond step 6's answer and the sign of a book's return in its boxes.
"""
import argparse, fnmatch, json, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import combine as cb  # noqa: E402
import update as up  # noqa: E402


def measures(day, scale=None):
    """Sharpe, yearly return and worst fall of daily returns (step 6's formulas), and their yearly return at a worst
    fall of 20 % (update.at_fall); with `scale`, the yearly return at that scale instead (a calendar year is read at
    the whole period's scale)."""
    if day is None or len(day) == 0:
        return None
    s = cb.stats(day)
    if scale is None:
        a = up.at_fall(day)
        return {**s, "scale": a and a["scale"], "at_fall": a and a["yearly"]}
    r = day.fillna(0.0)
    return {**s, "scale": scale, "at_fall": round(float((1 + scale * r).prod() ** (365 / len(r)) - 1), 4)}


def addition(runs, data=None):
    """The two portfolios and their measures: every candidate, and every candidate but those of `runs`."""
    books = json.loads((cb.REG / "books.json").read_text())
    rows = {r["key"]: r for r in books}
    keys = up.candidates(books)
    named = sorted({rows[k]["run"] for k in keys if any(fnmatch.fnmatchcase(rows[k]["run"], p) for p in runs)})
    rest = [k for k in keys if rows[k]["run"] not in named]
    data = up.bx.DATA if data is None else data
    cells = up.cells(rows, keys, data)
    out = {"runs": named, "candidates": {"with": len(keys), "without": len(rest)}}
    weights, coin_day = {}, {}
    for side, ks in (("with", keys), ("without", rest)):
        weights[side] = up.select(ks, rows, data, cells)[1] if ks else {}
        coin_day[side] = cb.per_coin(weights[side], rows, up.COMMON)[0] if weights[side] else None
    both = [c for c in coin_day.values() if c is not None]
    same = both[0].index.intersection(both[1].index) if len(both) == 2 else None      # the same coin-days for both
    out["coin_days"] = None if same is None else len(same)
    day = {s: None if c is None or same is None else c.loc[same].groupby(level="day").mean().dropna() for s, c in coin_day.items()}
    whole = {s: measures(d) for s, d in day.items()}
    years = sorted({y for d in day.values() if d is not None for y in d.index.year})
    out["periods"] = [("all years", whole)] + [
        (str(y), {s: measures(d[d.index.year == y], whole[s]["scale"]) for s, d in day.items()}) for y in years]
    out["strategies"] = {s: sorted(w) for s, w in weights.items()}
    out["entered"] = sorted(set(weights["with"]) - set(weights["without"]))
    out["left"] = sorted(set(weights["without"]) - set(weights["with"]))
    out["weights"] = weights
    return out


def text(name, a):
    pct = lambda m, k: "-" if m is None or m[k] is None else f"{m[k]:+.1%}" if k != "worst_fall" else f"{m[k]:.1%}"
    num = lambda m, k: "-" if m is None or m[k] is None else f"{m[k]:.2f}"
    w, o = a["weights"]["with"], a["weights"]["without"]
    whole = a["periods"][0][1]
    lines = [f"# What {name} adds to the portfolio (orchestration/combine/card.md, \"What a run adds to the portfolio\")", "",
             f"- Runs: {', '.join(a['runs']) or 'none of the candidates is of these runs'}",
             f"- Candidates: {a['candidates']['with']} with, {a['candidates']['without']} without "
             f"({a['candidates']['with'] - a['candidates']['without']} of these runs)",
             f"- Strategies in the portfolio: {len(w)} with, {len(o)} without",
             f"- Both measured on the same coin-days: {a['coin_days'] if a['coin_days'] is not None else '-'}",
             f"- Scale for a worst fall of 20 % (before any cost of leverage): x {num(whole['with'], 'scale')} with, "
             f"x {num(whole['without'], 'scale')} without; a year is read at that scale", "",
             "| Period | Days | Sharpe: with | without | Yearly: with | without | Worst fall: with | without | Yearly at a 20 % fall: with | without |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for label, m in a["periods"]:
        x, y = m["with"], m["without"]
        lines.append(f"| {label} | {(x or y or {}).get('days', '-')} | {num(x, 'sharpe')} | {num(y, 'sharpe')} | {pct(x, 'yearly')} | {pct(y, 'yearly')} | "
                     f"{pct(x, 'worst_fall')} | {pct(y, 'worst_fall')} | {pct(x, 'at_fall')} | {pct(y, 'at_fall')} |")
    for title, ks, wt in (("Entered the portfolio with these runs", a["entered"], w), ("Left the portfolio with these runs", a["left"], o)):
        lines += ["", f"{title} ({len(ks)}):"] + [f"- {k} (weight {wt[k]:.4g})" for k in ks]
    moved = [k for k in sorted(set(w) & set(o)) if abs(w[k] - o[k]) > 1e-9]
    lines += ["", f"In both, at another weight ({len(moved)}):"] + [f"- {k} (weight {w[k]:.4g} with, {o[k]:.4g} without)" for k in moved]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs", nargs="+", required=True)
    p.add_argument("--name")
    args = p.parse_args()
    if not args.name and (len(args.runs) > 1 or any(c in args.runs[0] for c in "*?[")):
        sys.exit("addition: a batch needs --name (the file's name)")
    name = args.name or args.runs[0]
    t = text(name, addition(args.runs))
    out = cb.FUNC / "additions" / f"{name}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    cb.write_atomic(out, t)
    print(t + f"\naddition: written to {out.relative_to(cb.STEPS)}")


if __name__ == "__main__":
    main()
