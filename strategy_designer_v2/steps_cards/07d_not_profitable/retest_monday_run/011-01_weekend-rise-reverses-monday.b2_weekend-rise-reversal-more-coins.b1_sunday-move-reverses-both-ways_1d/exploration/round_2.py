def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            cl = b["close"].astype(float)
            r1 = cl.pct_change()
            sd20 = r1.rolling(20).std(); sd60 = r1.rolling(60).std()
            mad = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            fwd = cl.shift(-2) / cl - 1
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "pos": np.arange(len(b)), "wd": ts.dt.weekday,
                               "year": ts.dt.year, "r1": r1, "z": r1 / mad, "fwd": fwd,
                               "volratio": sd20 / sd60, "f": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows).dropna(subset=["r1", "fwd", "volratio"])
    A = A[A["r1"] != 0]
    A["sret"] = -np.sign(A["r1"]) * A["fwd"]
    S = A[(A["wd"] == 6) & (A["f"] != 0)].copy()
    cuts = S["volratio"].quantile([1/3, 2/3]).values
    A["vq"] = np.digitize(A["volratio"], cuts)
    S["vq"] = np.digitize(S["volratio"], cuts)
    # condition alone: reversal of 1-day move over 2 days on non-Sunday bars, grid of every 2nd bar
    G = A[(A["wd"] != 6) & (A["pos"] % 2 == 0)]
    def summ(gb):
        r = gb["sret"].agg(["size", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["size"]))
        return r.round(5)
    out["reversal_by_weekday_x_volq_nonSunday"] = summ(G.groupby(["vq"]))
    out["reversal_by_weekday_nonSunday"] = summ(G.groupby("wd"))
    out["sunday_by_volq"] = summ(S.groupby("vq"))
    # difference Sunday minus other days within each vq
    res = {}
    for q in range(3):
        a = S.loc[S["vq"] == q, "sret"]; b2 = G.loc[G["vq"] == q, "sret"]
        t = stats.ttest_ind(a, b2, equal_var=False)
        res[q] = {"sun_minus_other": a.mean() - b2.mean(), "t": t.statistic, "n_sun": len(a), "n_other": len(b2)}
    out["sunday_minus_other_by_volq"] = pd.DataFrame(res).T.round(5)
    # case-level pseudo book variants: weekly mean per (wn, week) of position gain, chained in window order
    S["week"] = S["pos"]
    S["aret"] = S["alloc"] * S["fwd"]
    S["eq"] = np.sign(S["f"]) * 0.3 * S["fwd"]
    S["capped"] = np.clip(S["alloc"], -0.3, 0.3) * S["fwd"]
    S["hv"] = np.where(S["vq"] == 2, S["aret"], 0.0)
    S["hv_eq"] = np.where(S["vq"] == 2, S["eq"], 0.0)
    S["notlow"] = np.where(S["vq"] >= 1, S["aret"], 0.0)
    S["daykey"] = S["year"].astype(str) + "_" + S["pos"].astype(str)
    S2 = A[(A["wd"] == 6)].copy()
    var = {}
    S["t0"] = 0
    # group by window & sunday date proxy: use (wn, year, week-of-year)
    tsS = []
    for c, ws in data["bars"].items():
        pass
    wk = S.groupby(["wn", "year", "pos"])  # pos differs per coin; approximate by coin-pooled weekly via rank
    S["wkid"] = S.groupby(["coin", "wn"]).cumcount()
    for col in ["aret", "eq", "capped", "hv", "hv_eq", "notlow"]:
        W = S.groupby(["wn", "wkid"])[col].mean().sort_index()
        v = (1 + W).cumprod()
        mdd = (v / v.cummax() - 1).min()
        years = len(W) / 52.0
        yr = v.iloc[-1] ** (1 / years) - 1
        var[col] = {"yearly": yr, "maxdd": mdd, "calmar_proxy": yr / -mdd, "weekly_sharpe": W.mean() / W.std() * np.sqrt(52)}
    out["variants_weekly_chain"] = pd.DataFrame(var).T.round(4)
    # worst cases: volq and |z|
    q5 = S["aret"].quantile(0.02)
    out["worst2pct_volq_share"] = S.loc[S["aret"] <= q5, "vq"].value_counts(normalize=True)
    out["worst2pct_mean_absalloc"] = S.loc[S["aret"] <= q5, "alloc"].abs().mean()
    out["all_mean_absalloc_by_volq"] = S.groupby("vq")["alloc"].apply(lambda s: s.abs().mean())
    return out
