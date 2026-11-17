def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            rsi[:14] = np.nan
            b["share"] = (rsi > 50).astype(float).where(rsi.notna()).rolling(30).mean()
            b["ret30"] = c/c.shift(30)-1
            b["ret60"] = c/c.shift(60)-1
            b["fwd14"] = c.shift(-14)/c-1
            b["fwd1"] = c.shift(-1)/c-1
            b["pos14"] = np.arange(len(b)) % 14 == 0
            b["coin"] = coin; b["win"] = w
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["fwd1"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu14 = B[B["pos14"]].groupby("coin")["fwd14"].mean()
    G = B[B["pos14"]].dropna(subset=["fwd14","share","ret30"]).copy()
    G["dm"] = G["fwd14"] - G["coin"].map(mu14)
    s = stats.linregress(G["share"], G["dm"])
    out["share_slope_all"] = pd.Series({"slope": s.slope, "t": s.slope/s.stderr, "n": len(G)})
    res = {}
    for name, g in [("ret30>0", G[G["ret30"] > 0]), ("ret30<=0", G[G["ret30"] <= 0])]:
        s = stats.linregress(g["share"], g["dm"])
        res[name] = [s.slope, s.slope/s.stderr, len(g), g["dm"].mean()]
    out["share_slope_by_ret30"] = pd.DataFrame(res, index=["slope","t","n","mean_dm"]).T
    G["sq"] = pd.qcut(G["share"].rank(method="first"), 4, labels=False)
    out["share_q_fwd14"] = G.groupby("sq").agg(share=("share","mean"), fwd14=("fwd14","mean"),
                                               dm=("dm","mean"), n=("dm","size"))
    # daily book by trend state and side
    D = B.dropna(subset=["fwd1","ret30"]).copy()
    D["tr"] = np.where(D["ret30"] > 0, "up30", "down30")
    D["side"] = np.sign(D["pos"])
    out["gain_by_trend_side"] = D.groupby(["tr","side"]).agg(gain=("gain","mean"),
        fwd1=("fwd1","mean"), n=("gain","size"))
    # alternative: drop shorts in up30
    D["gain_noshort_up"] = np.where((D["tr"]=="up30") & (D["pos"]<0), 0, D["gain"])
    D["gain_longonly"] = np.where(D["pos"] < 0, 0, D["gain"])
    daily = D.groupby(["win","timestamp"])[["gain","gain_noshort_up","gain_longonly"]].mean()
    out["daily_variants"] = pd.DataFrame({k: [daily[k].mean(), daily[k].mean()/daily[k].std()*np.sqrt(365)]
                                          for k in daily}, index=["mean","sharpe"]).T
    return out
