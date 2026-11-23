import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    h = 3
    rows = []
    for coin, ws in bars.items():
        allret = []; per = []
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            fc = df["forecast"].values; al = df["postRebalance_current_allocation"].values
            n = len(df)
            for i in range(0, n - h, h):
                r = c[i + h] / c[i] - 1
                allret.append(r)
                if i == 0:
                    continue
                r1 = c[i] / c[i - 1] - 1
                rng = hi[i] - lo[i]
                cl = (c[i] - lo[i]) / rng if rng > 0 else np.nan
                p20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                p10 = c[i] / c[i - 10] - 1 if i >= 10 else np.nan
                r1d = c[i + 1] / c[i] - 1
                per.append((coin, w, r, r1, cl, p20, p10, fc[i], al[i], r1d))
        mu = np.mean(allret)
        for p in per:
            rows.append(p + (p[2] - mu,))
    D = pd.DataFrame(rows, columns=["coin", "win", "r", "r1", "cl", "p20", "p10", "fc", "al", "r1d", "ex"])
    dn = D[D.r1 < 0].dropna(subset=["cl"]).copy()

    def slope_t(d, x="cl"):
        d = d.dropna(subset=[x, "ex"])
        res = stats.linregress(d[x], d["ex"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(d), "mean_ex": d.ex.mean(),
                          "mean_ex_t": d.ex.mean() / (d.ex.std() / np.sqrt(len(d)))})

    out = {}
    out["fc_vs_cl_corr"] = float(dn[["fc", "cl"]].corr().iloc[0, 1])
    out["slope_on_forecast_all_down"] = slope_t(dn, "fc")
    dn["q"] = pd.qcut(dn.cl, 5, labels=False)
    for name, sub in [("p20_down", dn[dn.p20 <= 0]), ("p20_up", dn[dn.p20 > 0])]:
        g = sub.groupby("q").ex.agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out["quintiles_" + name] = g
    # graded by p20 depth within falling trend: interaction cl * (-p20)
    s = dn[dn.p20 <= 0].copy(); s["x"] = s.cl * (-s.p20)
    out["p20down_slope_on_cl_times_depth"] = slope_t(s, "x")
    s2 = dn[dn.p10 <= 0]
    out["p10down_slope_cl"] = slope_t(s2, "cl")
    out["p10up_slope_cl"] = slope_t(dn[dn.p10 > 0], "cl")
    # 1-day vs days 2-3 decomposition by cl quintile
    dn["r23"] = (1 + dn.r) / (1 + dn.r1d) - 1
    out["day1_vs_day23_by_q"] = dn.groupby("q")[["r1d", "r23", "r"]].mean()
    # allocation on non-down grid bars (carry exposure)
    out["mean_alloc_down_vs_notdown"] = pd.Series({"down": dn.al.mean(), "not_down": D[D.r1 >= 0].al.mean()})
    return out
