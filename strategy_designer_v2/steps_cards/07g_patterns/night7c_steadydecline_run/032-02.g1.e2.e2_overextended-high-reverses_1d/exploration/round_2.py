import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            df = pd.DataFrame(index=b.index)
            df["coin"] = coin; df["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            df["day"] = ts.dt.floor("D"); df["wd"] = ts.dt.weekday; df["yr"] = ts.dt.year
            df["fwd5"] = c.shift(-5) / c - 1
            df["r28"] = c / c.shift(28) - 1
            df["r5p"] = c / c.shift(5) - 1
            df["r1p"] = c / c.shift(1) - 1
            df["dh28"] = c / c.rolling(28).max() - 1
            df["dl28"] = c / c.rolling(28).min() - 1
            lr = np.log(c).diff()
            df["vol20"] = lr.rolling(20).std()
            df["volrel"] = df["vol20"] / lr.rolling(60, min_periods=40).std()
            rr = (h - l) / c
            df["rng"] = rr.rolling(5).mean() / rr.rolling(60, min_periods=40).mean()
            vv = b["volume"].astype(float)
            df["vrel"] = vv.rolling(5).mean() / vv.rolling(60, min_periods=40).mean()
            df["r28s"] = df["r28"] / df["r28"].abs().rolling(365, min_periods=60).mean()
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["grid"] = (np.arange(len(b)) % 5) == 0
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D[D.grid].groupby("coin")["fwd5"].mean()
    sd = D[D.grid].groupby("coin")["fwd5"].std()
    D["ex"] = D["fwd5"] - D["coin"].map(drift)
    D["exz"] = D["ex"] / D["coin"].map(sd)
    G = D[D.grid & D.ex.notna()].copy()
    out = {"n_grid": len(G), "drift_sd_by_coin": pd.DataFrame({"drift": drift, "sd": sd}).round(4)}

    def qtab(var, q=5, sub=None):
        S = G if sub is None else sub
        S = S[S[var].notna()].copy()
        S["q"] = S.groupby("coin")[var].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = S.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_z=("exz", "mean"), mid=(var, "median"))
        t["t"] = S.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t.round(4)

    def corr(var, sub=None):
        S = G if sub is None else sub
        S = S[[var, "exz", "day", "coin"]].dropna().copy()
        S["rz"] = S.groupby("coin")[var].rank(pct=True) - 0.5
        S["p"] = S.rz * S.exz
        d = S.groupby("day")["p"].sum()
        return f"n={len(S)} days={len(d)} mean(rank*exz)={S.p.mean():.4f} t_day={d.mean()/(d.std()/np.sqrt(len(d))):.2f}"

    for v in ["r28s", "dh28", "dl28", "r5p", "r1p", "vol20", "volrel", "rng", "vrel"]:
        try:
            out["q_" + v] = qtab(v)
            out["c_" + v] = corr(v)
        except Exception as e:
            out["err_" + v] = str(e)[:80]
    out["wd"] = G.groupby("wd")["ex"].agg(["size", "mean"]).round(4)
    out["athigh_vs_not"] = G.groupby(G.dh28 >= 0)["ex"].agg(["size", "mean", "std"]).round(4)
    ah = G[G.dh28 >= 0]
    out["athigh_by_win"] = ah.groupby("win")["ex"].agg(["size", "mean"]).round(4)
    out["athigh_by_yr"] = ah.groupby("yr")["ex"].agg(["size", "mean"]).round(4)
    try:
        out["q_r28s_athigh"] = qtab("r28s", 3, ah); out["c_r28s_athigh"] = corr("r28s", ah)
        out["q_vrel_athigh"] = qtab("vrel", 3, ah); out["c_vrel_athigh"] = corr("vrel", ah)
        out["q_rng_athigh"] = qtab("rng", 3, ah); out["c_rng_athigh"] = corr("rng", ah)
    except Exception as e:
        out["err_ah"] = str(e)[:80]
    dec = G[G.r28 < 0]
    try:
        out["c_r28s_in_decline"] = corr("r28s", dec)
        calm = dec[dec.rng < dec.rng.median()]; wild = dec[dec.rng >= dec.rng.median()]
        out["c_r28s_calm_decline"] = corr("r28s", calm)
        out["c_r28s_wild_decline"] = corr("r28s", wild)
        out["calm_vs_wild_decline_ex"] = pd.Series({"calm": calm.ex.mean(), "wild": wild.ex.mean(),
            "t": stats.ttest_ind(calm.ex, wild.ex, equal_var=False).statistic, "n_calm": len(calm), "n_wild": len(wild)}).round(4)
    except Exception as e:
        out["err_dec"] = str(e)[:80]
    # near low (28d) by depth
    al = G[G.dl28 <= 0]
    out["atlow_vs_not"] = G.groupby(G.dl28 <= 0)["ex"].agg(["size", "mean", "std"]).round(4)
    # book: days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean": bk.mean(), "sd": bk.std(), "n": len(bk),
                                   "sharpe": bk.mean() / bk.std() * np.sqrt(365)}).round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    if tr:
        T = pd.concat(tr, ignore_index=True)
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
        T["ef"] = T["entry_forecast"].abs()
        T["fq"] = pd.qcut(T.ef.rank(method="first"), 3, labels=False)
        out["trades_by_forecast_tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["size", "mean"]).round(3)
        out["trades_win_share"] = float((T.net_profit_loss_percent > 0).mean())
    return out
