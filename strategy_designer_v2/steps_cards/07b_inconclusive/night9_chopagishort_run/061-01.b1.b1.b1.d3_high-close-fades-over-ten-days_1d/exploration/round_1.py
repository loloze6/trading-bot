import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [2, 5, 10, 20]
    bars = data["bars"]
    # coin drift per horizon: non-overlapping returns over all windows
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            rng = hi - lo
            loc = np.where(rng > 0, (cl - lo) / np.where(rng > 0, rng, 1), np.nan)
            f = b["forecast"].fillna(0).values
            reg = b["regime"].astype(str).values
            n = len(b)
            # 10-bar grid, first bar per cell for each "group"
            for i in range(n):
                r = {"coin": c, "win": w, "i": i, "cell": i // 10, "loc": loc[i], "reg": reg[i],
                     "f": f[i], "fprev": f[i-1] if i > 0 else 0.0,
                     "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(b["timestamp"].iloc[i]).normalize()}
                for h in H:
                    r[f"u{h}"] = -(cl[i+h]/cl[i]-1 - drift[(c,h)]) if i + h < n else np.nan
                    r[f"t{h}"] = -(cl[i+h]/cl[i]-1) if i + h < n else np.nan
                rows.append(r)
    df = pd.DataFrame(rows)
    # cases: first short bet (forecast drop >=2 to <= -2) per 10-bar cell
    bet = df[(df.f <= -2) & ((df.fprev - df.f) >= 2)]
    cases = bet.groupby(["coin", "win", "cell"]).head(1).copy()

    def summ(g, col="u10"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "mean": np.nan, "t_day": np.nan, "days": 0})
        d = g.groupby("day")[col].sum()
        nd = len(d); m = g[col].mean()
        dev = g.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev**2).sum()) / len(g)
        return pd.Series({"n": len(g), "mean": m, "t_day": m / se if se > 0 else np.nan, "days": nd})

    out = {}
    out["cases_all_h"] = pd.DataFrame({f"h{h}": summ(cases, f"u{h}") for h in H}).T
    out["cases_total_move_h"] = pd.DataFrame({f"h{h}": summ(cases, f"t{h}") for h in H}).T
    cases["locbin"] = pd.cut(cases["loc"], [0.79, 0.85, 0.9, 0.95, 1.01])
    out["cases_by_loc"] = cases.groupby("locbin").apply(lambda g: summ(g)).reset_index()
    cases["fq"] = pd.qcut(cases["f"].abs(), 4, duplicates="drop")
    out["cases_by_absf_q"] = cases.groupby("fq").apply(lambda g: summ(g)).reset_index()
    out["corr_loc_u10"] = float(cases[["loc", "u10"]].dropna().corr().iloc[0, 1])
    out["corr_absf_loc"] = float(cases[["loc"]].assign(a=cases.f.abs()).dropna().corr().iloc[0, 1])
    out["cases_by_coin"] = cases.groupby("coin").apply(lambda g: summ(g)).reset_index()
    out["cases_by_year"] = cases.groupby("year").apply(lambda g: summ(g)).reset_index()
    # all in-profile bars (regime unknown or mean_reversion) on 10-bar grid, by loc bins
    grid = df[df.i % 10 == 0].copy()
    grid["inprof"] = grid.reg.isin(["unknown", "mean_reversion"])
    grid["locbin"] = pd.cut(grid["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 0.9, 1.01])
    out["grid_inprofile_by_loc"] = grid[grid.inprof].groupby("locbin").apply(lambda g: summ(g)).reset_index()
    out["grid_outprofile_by_loc"] = grid[~grid.inprof].groupby("locbin").apply(lambda g: summ(g)).reset_index()
    out["grid_inprofile_by_loc_h2"] = grid[grid.inprof].groupby("locbin").apply(lambda g: summ(g, "u2")).reset_index()
    out["regime_counts"] = df.reg.value_counts()
    return out
