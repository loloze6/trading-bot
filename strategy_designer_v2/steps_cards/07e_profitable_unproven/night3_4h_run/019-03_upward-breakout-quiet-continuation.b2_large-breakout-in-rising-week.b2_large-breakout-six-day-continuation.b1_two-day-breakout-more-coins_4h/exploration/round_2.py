import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = [12, 36, 72]
    drift = {}
    for c in bars:
        d = {}
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs); d[h] = (rs.mean(), rs.std())
        drift[c] = d
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values; n = len(cl)
            ser = pd.Series(hi).shift(1).rolling(12).max().values
            serl = pd.Series(lo).shift(1).rolling(12).min().values
            rng = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            raw = (cl - ser) / rng
            quiet = (ser - serl) / rng  # prior 2-day range in avg bar ranges
            r7 = pd.Series(cl).pct_change(42).values
            r30 = pd.Series(cl).pct_change(180).values
            brk = raw > 0
            prev = np.r_[False, brk[:-1]]
            ent = brk & ~prev
            seen = set()
            for t in np.where(ent)[0]:
                cell = t // 36
                if cell in seen or np.isnan(r7[t]) or r7[t] <= 0: continue
                seen.add(cell)
                row = {"coin": c, "raw": raw[t], "r7": r7[t], "quiet": quiet[t], "r30": r30[t]}
                for h in H:
                    if t + h < n:
                        row["u%d" % h] = cl[t + h] / cl[t] - 1 - drift[c][h][0]
                        row["s%d" % h] = row["u%d" % h] / drift[c][h][1]
                cases.append(row)
    cs = pd.DataFrame(cases)
    out = {"n_cases": len(cs)}
    cs["rq"] = pd.qcut(cs.raw, 3, labels=False); cs["r7q"] = pd.qcut(cs.r7, 3, labels=False)
    out["raw_x_r7_u36"] = cs.pivot_table(index="rq", columns="r7q", values="u36", aggfunc="mean").round(4)
    out["raw_x_r7_n"] = cs.pivot_table(index="rq", columns="r7q", values="u36", aggfunc="count")
    def tq(key, q=5):
        c2 = cs.dropna(subset=[key, "u36"]).copy()
        c2["b"] = pd.qcut(c2[key], q, labels=False, duplicates="drop")
        g = c2.groupby("b")
        return pd.DataFrame({"med": g[key].median(), "n": g.u36.count(), "u36": g.u36.mean(),
            "t36": g.u36.apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
            "u72": g.u72.mean(), "s36": g.s36.mean()}).round(4)
    out["by_quiet"] = tq("quiet")
    out["by_r30"] = tq("r30")
    # per-coin rank correlation raw vs s36, and top-third mean
    pc = []
    for c, g in cs.dropna(subset=["s36"]).groupby("coin"):
        rho = stats.spearmanr(g.raw, g.s36).correlation
        top = g[g.raw >= g.raw.quantile(2/3)].u36.mean(); bot = g[g.raw <= g.raw.quantile(1/3)].u36.mean()
        pc.append({"coin": c, "n": len(g), "rho": rho, "top_minus_bot": top - bot})
    pc = pd.DataFrame(pc).set_index("coin")
    out["per_coin"] = pc.round(3)
    out["per_coin_pos_share"] = float((pc.top_minus_bot > 0).mean())
    # book daily timing vs market
    rows = []
    for c in days:
        for w, d in days[c].items():
            rows.append(d.assign(coin=c, w=w))
    D = pd.concat(rows)
    # daily mean across coins
    dm = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["daily"] = pd.Series({"book_mean": dm.book_return.mean(), "hold_mean": dm.coin_return.mean(),
        "book_t": dm.book_return.mean() / (dm.book_return.std() / np.sqrt(len(dm))),
        "corr": dm.book_return.corr(dm.coin_return), "n_days": len(dm)}).round(6)
    # book gain in market states: up vs down hold days
    dm["state"] = np.where(dm.coin_return > 0, "up", "down")
    out["book_by_state"] = dm.groupby("state").book_return.agg(["mean", "count"]).round(5)
    return out
