def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    cases = []
    daily = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; lo = b["low"].values; hi = b["high"].values
            n = len(b)
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            lowmin = pd.Series(lo).shift(1).rolling(12).min().values
            himax = pd.Series(hi).shift(1).rolling(12).max().values
            rng = pd.Series(hi - lo).rolling(180).mean().values
            r30 = cl / pd.Series(cl).shift(180).values - 1
            lr = pd.Series(np.log(cl)).diff()
            vol = lr.rolling(42).std().values
            vol180 = lr.rolling(180).std().values
            r90 = cl / pd.Series(cl).shift(540).values - 1
            for t in range(n - 18):
                if prev[t] <= 1e-9 and alloc[t] > 1e-9:
                    path = cl[t:t + 19] / cl[t] - 1
                    cases.append(dict(coin=c, wn=int(w[1:]), fwd=cl[t + 18] / cl[t] - 1,
                                      mae=path.min(),
                                      width=(himax[t] - lowmin[t]) / rng[t] if rng[t] else np.nan,
                                      r30=r30[t], r90=r90[t], volratio=vol[t] / vol180[t],
                                      vol180=vol180[t], alloc=alloc[t]))
            # position gain per bar, grouped by state of entry
            g = alloc[:-1] * (cl[1:] / cl[:-1] - 1)
            daily.append(pd.DataFrame(dict(g=g, a=alloc[:-1], vr=(vol / vol180)[:-1], r30=r30[:-1])))
    C = pd.DataFrame(cases).dropna(subset=["width", "volratio", "r30"])
    drift = {}
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 18, 18)
            rr += list(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(rr)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    out["spearman"] = C[["width", "volratio", "r30", "r90", "vol180", "ex"]].corr(method="spearman")
    def tab(a, bcol):
        C["_a"] = pd.qcut(C[a], 3, labels=["lo", "mid", "hi"])
        C["_b"] = pd.qcut(C[bcol], 3, labels=["lo", "mid", "hi"])
        r = C.groupby(["_a", "_b"]).agg(n=("ex", "size"), ex=("ex", "mean"), sd=("ex", "std"), mae=("mae", "mean"))
        r["t"] = r.ex / (r.sd / np.sqrt(r.n))
        r.index = [f"{a}:{x}|{bcol}:{y}" for x, y in r.index]
        return r
    out["width_x_volratio"] = tab("width", "volratio")
    out["width_x_r30"] = tab("width", "r30")
    out["r90_q"] = C.groupby(pd.qcut(C.r90, 4).astype(str)).agg(n=("ex", "size"), ex=("ex", "mean"), mae=("mae", "mean"))
    # worst cases: share of total losses, profile
    C["worst"] = C.ex <= C.ex.quantile(0.1)
    out["worst_profile"] = C.groupby("worst")[["width", "volratio", "r30", "r90", "vol180", "alloc", "mae"]].median()
    # bar-level position gain by volratio state
    Dl = pd.concat(daily).dropna()
    Dl = Dl[Dl.a > 1e-9]
    out["gain_by_vr"] = Dl.groupby(pd.qcut(Dl.vr, 5).astype(str)).agg(n=("g", "size"), mean_gain=("g", "mean"), alloc=("a", "mean"))
    out["gain_by_r30"] = Dl.groupby(pd.qcut(Dl.r30, 5).astype(str)).agg(n=("g", "size"), mean_gain=("g", "mean"), alloc=("a", "mean"))
    return out
