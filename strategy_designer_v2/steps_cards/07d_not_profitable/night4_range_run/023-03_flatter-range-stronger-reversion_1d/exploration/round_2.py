def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            netr = c / c.shift(30) - 1
            flat = 1 - (c - c.shift(30)).abs() / (H - L)
            al = df["postRebalance_current_allocation"].reset_index(drop=True)
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, d=2*pos[i]-1, flat=flat[i],
                                     netr=netr[i], fwd=fwd[i], al=al[i]))
    R = pd.DataFrame(rows).dropna(subset=["d", "flat", "fwd", "netr"])
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["usual"] = R.groupby(["coin", "h"])["fwd"].transform("std")
    R["u"] = R["fwd"] - R["drift"]
    R = R[R["d"] != 0]
    res = []
    for h in (5, 10):
        Rh = R[R["h"] == h]
        for fq, g in Rh.groupby(pd.qcut(Rh["flat"], 3, labels=["trendy", "mid", "flat"])):
            r, p = stats.spearmanr(g["d"], g["u"])
            cont = (np.sign(g["d"]) * g["u"])
            res.append(dict(h=h, flat=fq, n=len(g), spearman_d_u=r, p=p,
                            cont_mean=cont.mean(), cont_t=cont.mean()/(cont.std()/np.sqrt(len(g))),
                            strength=(cont/g["usual"]).mean(),
                            total=(np.sign(g["d"])*g["fwd"]).mean()))
    out["d_vs_unusual_by_flatness"] = pd.DataFrame(res)
    # graded continuation in d: by d decile at h5, signed
    R5 = R[R["h"] == 5].copy()
    R5["dq"] = pd.qcut(R5["d"], 6, labels=False)
    a = R5.groupby("dq").agg(d_mean=("d", "mean"), u_mean=("u", "mean"), n=("u", "count"))
    out["h5_unusual_by_signed_d"] = a
    # 30d net return graded (momentum) at h5,h10
    res = []
    for h in (5, 10):
        Rh = R[R["h"] == h].copy()
        Rh["nq"] = pd.qcut(Rh["netr"], 5, labels=False)
        for q, g in Rh.groupby("nq"):
            res.append(dict(h=h, q=q, netr=g["netr"].mean(), u=g["u"].mean(),
                            t=g["u"].mean()/(g["u"].std()/np.sqrt(len(g))), n=len(g)))
    out["unusual_by_30d_return_quintile"] = pd.DataFrame(res)
    # book's position vs d at h5: losses by held side and d side
    R5["held"] = np.sign(R5["al"]); R5["dside"] = np.sign(R5["d"])
    R5["pnl"] = R5["al"] * R5["fwd"]
    out["h5_pnl_by_held_x_dside"] = R5.groupby(["held", "dside"])["pnl"].agg(["mean", "count"])
    # book's daily return: deepest falls by coin-window sum
    br = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            br.append(dict(coin=coin, w=w, book=dd["book_return"].sum(), coin_ret=dd["coin_return"].sum()))
    D = pd.DataFrame(br)
    out["worst_coin_windows"] = D.sort_values("book").head(10).reset_index(drop=True)
    out["corr_book_vs_coin_window"] = float(D["book"].corr(D["coin_ret"]))
    return out
