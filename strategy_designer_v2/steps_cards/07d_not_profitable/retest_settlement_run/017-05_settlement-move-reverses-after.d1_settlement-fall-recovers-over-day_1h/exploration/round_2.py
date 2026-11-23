def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for c, wins in data["bars"].items():
        r = []
        for w, b in wins.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            r.append(cl[idx + 24] / cl[idx] - 1)
        drift[c] = np.concatenate(r).mean()
    rows = []; allrows = []
    for c, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; ts = pd.to_datetime(b["timestamp"]); hr = ts.dt.hour.values
            n = len(b)
            pc = cl.pct_change()
            vr = (pc.rolling(168, min_periods=50).std() / pc.rolling(720, min_periods=100).std())
            r1d = cl / cl.shift(24) - 1
            f24 = cl.shift(-24) / cl - 1
            df = pd.DataFrame({"pos": np.arange(n), "hr": hr, "fc": b["forecast"].values, "vr": vr.values,
                               "r1d": r1d.values, "f24": f24.values, "year": ts.dt.year.values,
                               "al": b["postRebalance_current_allocation"].values})
            df["coin"] = c; df["win"] = w; df["cell"] = df["pos"] // 24
            g = df[df.pos % 24 == 0].dropna(subset=["f24"])
            allrows.append(g)
            st = df[np.isin(hr, [23, 15])].dropna(subset=["f24"])
            rows.append(st[st.fc > 0].groupby("cell").head(1))
            rows.append(st[st.fc <= 0].groupby("cell").head(1).assign(fc=0.0))
    D = pd.concat(rows); A = pd.concat(allrows)
    for X in (D, A):
        X["ex"] = X["f24"] - X["coin"].map(drift)
    allv = pd.concat([D["vr"], A["vr"]]).dropna()
    q1, q2 = np.nanquantile(D["vr"], [1/3, 2/3])
    for X in (D, A):
        X["vq"] = np.where(X.vr > q2, "hot", np.where(X.vr > q1, "mid", "calm"))
    S = D[D.fc > 0].copy()
    med = S.fc.median()
    S["fh"] = np.where(S.fc > med, "top", "bot")
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "ex%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "total%": 100 * g["f24"].mean()})
    out["sig_fhalf_x_vol"] = S.groupby(["fh", "vq"]).apply(summ)
    out["allbars_grid_by_vol"] = A.groupby("vq").apply(summ)
    out["nonsig_settle_by_vol"] = D[D.fc <= 0].groupby("vq").apply(summ)
    out["sig_hot_by_year"] = S[S.vq == "hot"].groupby("year").apply(summ)
    out["sig_nothot_by_year"] = S[S.vq != "hot"].groupby("year").apply(summ)
    # book falls
    dd = []
    for c, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=c, wn=int(w[1:])))
    DD = pd.concat(dd)
    B = DD.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    v = (1 + B.book_return).cumprod(); dpk = v / v.cummax() - 1
    B["dd"] = dpk.values
    B["year"] = pd.to_datetime(B.index.get_level_values(1)).year
    out["book_by_year"] = B.groupby("year").apply(lambda g: pd.Series({"book_sum%": 100 * g.book_return.sum(), "hold_sum%": 100 * g.coin_return.sum(), "worst_dd": g.dd.min()}))
    # losing days: coin falling days
    B["cq"] = pd.qcut(B.coin_return, 5, labels=False)
    out["book_by_coin_day_quintile"] = B.groupby("cq")[["book_return", "coin_return"]].mean() * 100
    return out
