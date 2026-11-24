def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            b["r1"] = c.shift(-1) / c - 1
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["fc"] = b["forecast"].astype(float)
            b["wd"] = b["ts"].dt.weekday
            b["gain"] = b["alloc"] * b["r1"]
            b["monthu"] = c.shift(1) / c.shift(4) - 1
            b["vol20"] = c.pct_change().rolling(20).std()
            b["z"] = b["monthu"] / (b["vol20"] * np.sqrt(3))
            lo = c.rolling(250, min_periods=60).min(); hi = c.rolling(250, min_periods=60).max()
            b["rpos"] = (c - lo) / (hi - lo)
            b["coin"] = coin; b["w"] = w; b["wn"] = int(w[1:]); b["day"] = b["ts"].dt.floor("D")
            b["year"] = b["ts"].dt.year
            rows.append(b[["coin","w","wn","day","year","wd","fc","alloc","r1","gain","monthu","z","rpos"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(mu)
    cost = 0.0019
    F = B[(B.wd == 4) & B.r1.notna()].copy()
    # per-coin-saturday net gains: round trip cost * |alloc|
    F["net"] = F["gain"] - cost * F["alloc"].abs()
    F["net_long"] = np.where(F.alloc > 0, F["net"], 0.0)
    F["net_short"] = np.where(F.alloc < 0, F["net"], 0.0)
    F["net_long_strong"] = np.where((F.alloc > 0) & (F.fc >= F.loc[F.fc>0,"fc"].median()), F["net"], 0.0)
    # build approximate daily book: every coin-day, 0 except Saturday gains; mean over 6 coins
    allday = B[B.r1.notna()][["coin","wn","day"]].copy()
    allday = allday.merge(F[["coin","wn","day","net","net_long","net_short","net_long_strong"]], on=["coin","wn","day"], how="left").fillna(0)
    bk = allday.groupby(["wn","day"])[["net","net_long","net_short","net_long_strong"]].mean().sort_index()
    res = {}
    for col in ["net","net_long","net_short","net_long_strong"]:
        r = bk[col]
        v = (1 + r).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(r) / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        res[col] = {"yearly%": 100*yr, "maxdd%": 100*dd, "calmar": yr/abs(dd), "sharpe": r.mean()/r.std()*np.sqrt(365)}
    out["approx_book_variants"] = pd.DataFrame(res).T
    # drawdown windows 5-10: gain by side
    G = F.copy(); G["side"] = np.where(G.alloc > 0, "long", np.where(G.alloc < 0, "short", "flat"))
    G["grp"] = np.where(G.wn.between(5, 10), "w5-w10", "other")
    out["net_by_side_ddwindows_%"] = G.groupby(["grp","side"])["net"].agg(["count","mean","sum"]) * [1,100,100]
    # condition check: Saturday excess on all Fridays by z sign (unscaled), and z quartile
    F["zq"] = pd.qcut(F.z, 5, labels=False)
    out["sat_ex_by_midweek_z_quintile"] = F.groupby("zq")["ex"].agg(lambda s: pd.Series([100*s.mean(), s.mean()/(s.std()/np.sqrt(len(s))), len(s)]).tolist())
    # range position: Saturday excess unsigned by rpos tercile, and the long-side by rpos
    F["rq"] = pd.qcut(F.rpos, 3, labels=False)
    def st(s): return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    out["sat_ex_all_by_rpos"] = F.groupby("rq")["ex"].apply(st).unstack()
    F["pos_mt"] = F.z > 0
    out["sat_ex_by_rpos_midweek_sign"] = F.groupby(["rq","pos_mt"])["ex"].apply(st).unstack()
    # unconditional saturday excess
    out["sat_ex_all"] = st(F["ex"])
    return out
