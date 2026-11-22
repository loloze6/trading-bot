import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": r / sd, "r": r,
                               "f5": c.shift(-5) / c - 1, "f1": c.shift(-1) / c - 1,
                               "p20": c / c.shift(20) - 1,
                               "falling": (b["regime"] == "mean_reversion").values,
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    grid = d[d["pos"] % 5 == 0].copy()
    drift = grid.groupby("coin")["f5"].mean(); sd5 = grid.groupby("coin")["f5"].std()
    grid["u5"] = grid["f5"] - grid["coin"].map(drift)
    grid["s5"] = grid["u5"] / grid["coin"].map(sd5)
    g = grid.dropna(subset=["z", "u5"])
    out = {}
    up = g[(~g["falling"]) & (g["z"] > 0)]
    dn = g[(g["falling"]) & (g["z"] > 0)]
    def rho(x):
        if len(x) < 10: return pd.Series({"n": len(x), "rho": np.nan, "p": np.nan, "big_mean_u5": np.nan, "big_n": 0})
        rr, p = stats.spearmanr(x["z"], x["s5"])
        big = x[x["z"] > 1.5]
        return pd.Series({"n": len(x), "rho": rr, "p": p, "big_mean_u5": big["u5"].mean(), "big_n": len(big)})
    out["rising_up_by_coin"] = up.groupby("coin").apply(rho)
    out["rising_up_by_year"] = up.groupby("yr").apply(rho)
    out["rising_up_all"] = rho(up).to_frame().T
    out["falling_up_by_coin"] = dn.groupby("coin").apply(rho)
    out["falling_up_all"] = rho(dn).to_frame().T
    # difference big rises rising vs falling
    a = up[up["z"] > 1.5]["u5"]; b2 = dn[dn["z"] > 1.5]["u5"]
    t, p = stats.ttest_ind(a, b2, equal_var=False)
    out["big_rise_rising_minus_falling"] = pd.DataFrame([{"n_rising": len(a), "n_falling": len(b2), "diff": a.mean() - b2.mean(), "t": t}])
    # rising regime: p20 momentum graded
    gr = g[~g["falling"]].dropna(subset=["p20"])
    out["rising_p20_rho_by_coin"] = gr.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x["p20"], x["s5"])[0], "p": stats.spearmanr(x["p20"], x["s5"])[1]}))
    # weekday: day-level mean across coins (one obs per day), labelled by return day
    dd = d.dropna(subset=["f1"]).copy()
    dd["u1"] = dd["f1"] - dd.groupby("coin")["f1"].transform("mean")
    dd["rwd"] = (dd["wd"] + 1) % 7
    daylvl = dd.groupby(["day", "rwd", "yr"])["u1"].mean().reset_index()
    out["weekday_daylevel"] = daylvl.groupby("rwd")["u1"].agg(n="size", mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    sat = daylvl[daylvl["rwd"] == 5]
    out["sat_by_year"] = sat.groupby("yr")["u1"].agg(n="size", mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["sat_by_coin"] = dd[dd["rwd"] == 5].groupby("coin")["u1"].agg(n="size", mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    return out
