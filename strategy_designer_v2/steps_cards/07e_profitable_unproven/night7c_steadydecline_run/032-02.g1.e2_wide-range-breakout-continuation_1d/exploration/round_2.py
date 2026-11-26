def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    H = [1, 5, 10]
    cmean = {}
    for c in coins:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(rs)
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng = (hi - lo) / cl
            rr = rng / rng.rolling(28).mean()
            pe = cl / cl.shift(28) - 1
            mx = cl.rolling(28).max()
            dist = (mx - cl) / mx
            vol = cl.pct_change().rolling(28).std()
            f = pd.DataFrame({"pe": pe, "rr": rr, "dist": dist, "pez": pe / (vol * np.sqrt(28)),
                              "pos": b["postRebalance_current_allocation"].fillna(0)})
            f["r1"] = (cl.shift(-1) / cl - 1)
            f["gain"] = f["pos"] * f["r1"]
            f["mktpart"] = f["pos"] * cmean[(c, 1)]
            n = len(cl)
            for h in H:
                fr = cl.shift(-h) / cl - 1
                g = np.zeros(n, bool); g[np.arange(0, n, h)] = True
                f[f"x{h}"] = np.where(g, fr - cmean[(c, h)], np.nan)
            f["coin"] = c; f["w"] = w; f["year"] = pd.to_datetime(b["timestamp"]).dt.year.values
            feats.append(f)
    F = pd.concat(feats).dropna(subset=["pe", "dist", "rr"])
    def summ(s):
        s = s.dropna(); return f"{s.mean():+.4f} t{stats.ttest_1samp(s,0).statistic:.2f} n{len(s)}" if len(s) > 2 else ""
    F["athigh"] = F.dist <= 1e-9
    F["wide"] = F.rr >= 1
    F["up"] = F.pe > 0
    t = {}
    for (u, a, wd), g in F.groupby(["up", "athigh", "wide"]):
        t[f"up{int(u)}_high{int(a)}_wide{int(wd)}"] = {f"h{h}": summ(g[f"x{h}"]) for h in H}
    out["cells"] = pd.DataFrame(t).T
    # grading of nearness across all days (dist quintiles, at-high separate)
    G = F[~F.athigh].copy(); G["q"] = pd.qcut(G.dist, 5, labels=False)
    tab = {"athigh": {f"h{h}": summ(F[F.athigh][f"x{h}"]) for h in H}}
    for q, g in G.groupby("q"):
        tab[f"dq{q}"] = {f"h{h}": summ(g[f"x{h}"]) for h in H}
    out["dist_all"] = pd.DataFrame(tab).T
    # at-high days: size of 28d rise (vol-scaled) quintiles
    A = F[F.athigh].copy(); A["q"] = pd.qcut(A.pez, 5, labels=False)
    out["athigh_pez_q"] = pd.DataFrame({f"h{h}": A.groupby("q")[f"x{h}"].apply(summ) for h in H})
    A["q"] = pd.qcut(A.pe, 5, labels=False)
    out["athigh_pe_q"] = pd.DataFrame({f"h{h}": A.groupby("q")[f"x{h}"].apply(summ) for h in H})
    # where the book's bar gain comes from: by state of the bar it held over
    F["state"] = np.where(F.athigh, "athigh", np.where(F.dist < 0.05, "near5", np.where(F.up, "up_far", "down")))
    out["book_gain_by_state"] = F.groupby("state").agg(gain_sum=("gain", "sum"), mkt_sum=("mktpart", "sum"), mean_pos=("pos", "mean"), n=("pos", "size"))
    out["book_gain_by_year"] = F.groupby("year").agg(gain_sum=("gain", "sum"), mkt_sum=("mktpart", "sum"))
    return out
