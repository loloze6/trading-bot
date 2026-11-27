"""Group medians of the per-book figures (per_book.json) -> results table (stdout)."""
import json, math, os, statistics as st
OUT = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(OUT, "per_book.json")))
groups = [("choppy calm", lambda r: r["group"] == "choppy calm"), ("choppy agitated", lambda r: r["group"] == "choppy agitated"),
          ("choppy", lambda r: r["group"] == "choppy"), ("all choppy", lambda r: r["group"] != "reference profitable"),
          ("reference profitable", lambda r: r["group"] == "reference profitable")]
def med(xs):
    xs = [x for x in xs if not (isinstance(x, float) and math.isnan(x))]
    return (st.median(xs), len(xs)) if xs else (float("nan"), 0)
cols = [("n", "trades"), ("median_bars", "bars held"), ("mean_net", "net %"), ("mean_gross", "gross %"), ("mean_mfe", "MFE %"),
        ("mean_mae", "MAE %"), ("mean_giveback", "give-back pts"), ("giveback_share", "give-back/MFE"),
        ("share_gave_back_half", "share gave >half"), ("share_2x_mean_then_lower", "share >=2x mean then below mean")]
print("| group | books | " + " | ".join(c[1] for c in cols) + " |")
print("|" + "---|" * (len(cols) + 2))
for g, f in groups:
    rs = [r for r in rows if f(r)]
    cells = []
    for k, _ in cols:
        m, n = med([r[k] for r in rs])
        cells.append(f"{m:.0f}" if k in ("n", "median_bars") else (f"{m:.2f}" + ("" if n == len(rs) else f" ({n} bks)")))
    print(f"| {g} | {len(rs)} | " + " | ".join(cells) + " |")
print()
print("Net % per trade, exit at the plan's exit vs after N bars (median across books; books where N bars beats the plan)")
print("| group | plan | 1 | 2 | 3 | 5 | 10 |")
print("|---|---|---|---|---|---|---|")
for g, f in groups:
    rs = [r for r in rows if f(r)]
    cells = [f"{med([r['mean_net'] for r in rs])[0]:.2f}"]
    for n in (1, 2, 3, 5, 10):
        better = sum(r[f"hold{n}"] > r["mean_net"] for r in rs)
        cells.append(f"{med([r[f'hold{n}'] for r in rs])[0]:.2f} ({better}/{len(rs)})")
    print(f"| {g} | " + " | ".join(cells) + " |")
print()
print("Books with mean net per trade > 0 at the plan's exit:", {g: f"{sum(r['mean_net']>0 for r in rows if f(r))}/{sum(1 for r in rows if f(r))}" for g, f in groups})
print("Engine check (trade_diagnostics): trades matched", sum(r["chk_matched"] for r in rows), "of", sum(r["n"] for r in rows),
      "; equal within 0.01 pts:", sum(r["chk_equal"] for r in rows), "; worst diff", max(r["chk_worst"] for r in rows))
