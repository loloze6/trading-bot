def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift per horizon over all visible windows (non-overlapping grid)
        drift = {}
        for h in (3, 7, 14, 21):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            ret30 = np.full(n, np.nan)
            ret30[30:] = c[30:] / c[:-30] - 1
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for i in range(0, n, 7):
                if reg[i] != "unknown" or np.isnan(ret30[i]):
                    continue
                r = {"coin": coin, "win": w, "ret30": ret30[i], "day": ts[i],
                     "fc": df["forecast"].values[i]}
                for h in (3, 7, 14, 21):
                    if i + h < n:
                        r[f"x{h}"] = c[i + h] / c[i] - 1 - drift[h]
                        r[f"tot{h}"] = c[i + h] / c[i] - 1
                    else:
                        r[f"x{h}"] = np.nan
                        r[f"tot{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    out["n_in_profile_grid"] = len(d)
    # sign: short-side excess = -x
    def summ(g, col="x7"):
        v = g[col].dropna()
        if len(v) < 3:
            return pd.Series({"n": len(v), "mean": np.nan, "t": np.nan})
        return pd.Series({"n": len(v), "mean": v.mean(), "t": v.mean() / (v.std() / np.sqrt(len(v)))})
    d["side"] = np.where(d["ret30"] < 0, "fall", "rise")
    # signed in the idea's (continuation) direction
    for h in (3, 7, 14, 21):
        d[f"c{h}"] = np.where(d["ret30"] < 0, -d[f"x{h}"], d[f"x{h}"])
    out["by_side_horizon"] = pd.DataFrame({f"h{h}": d.groupby("side").apply(lambda g: summ(g, f"c{h}")).stack() for h in (3, 7, 14, 21)})
    f = d[d.side == "fall"].copy()
    f["q"] = pd.qcut(f["ret30"], 4, labels=["deepest", "q2", "q3", "shallow"])
    out["fall_by_depth_q_c7"] = f.groupby("q").apply(lambda g: pd.concat([summ(g, "c7"), pd.Series({"ret30": g.ret30.mean()})]))
    out["fall_by_depth_q_c14"] = f.groupby("q").apply(lambda g: summ(g, "c14"))
    out["fall_by_coin_c7"] = f.groupby("coin").apply(lambda g: summ(g, "c7"))
    out["fall_by_win_c7"] = f.groupby("win").apply(lambda g: summ(g, "c7"))
    f["year"] = pd.to_datetime(f["day"]).dt.year
    out["fall_by_year_c7"] = f.groupby("year").apply(lambda g: summ(g, "c7"))
    out["fall_total7_mean"] = float(-f["tot7"].mean())
    out["corr_ret30_x7_fall"] = float(f[["ret30", "x7"]].dropna().corr().iloc[0, 1])
    r = d[d.side == "rise"].copy()
    r["q"] = pd.qcut(r["ret30"], 4, labels=["small", "q2", "q3", "large"])
    out["rise_by_q_c7"] = r.groupby("q").apply(lambda g: summ(g, "c7"))
    return out
