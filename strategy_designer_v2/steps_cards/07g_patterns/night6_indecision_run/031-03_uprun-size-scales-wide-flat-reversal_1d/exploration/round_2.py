def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; H = 5
    rows = []; drift = {}
    for coin, wins in bars.items():
        gr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True); c = df["close"].values; n = len(df)
            for i in range(0, n - H, H): gr.append(c[i+H]/c[i]-1)
            rng = df["high"] - df["low"]
            mr20 = rng.rolling(20, min_periods=20).mean()
            r1 = df["close"].pct_change()
            vol20 = r1.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "day": ts.dt.floor("D"), "year": ts.dt.year,
                "width": rng/mr20, "body": (df["close"]-df["open"]).abs()/rng.replace(0, np.nan),
                "sbody": (df["close"]-df["open"])/rng.replace(0, np.nan),
                "clv": ((df["close"]-df["low"])/rng.replace(0, np.nan))*2-1,
                "prior5": df["close"]/df["close"].shift(5)-1, "vol20": vol20, "r1": r1,
                "z1": r1/vol20.shift(1),
                "fwd": df["close"].shift(-H)/df["close"]-1,
                "fwd1": df["close"].shift(-1)/df["close"]-1,
                "alloc": df["postRebalance_current_allocation"], "fc": df["forecast"],
            }))
        drift[coin] = np.mean(gr)
    D = pd.concat(rows, ignore_index=True)
    D["unus"] = D["fwd"] - D["coin"].map(drift); D["cell"] = D["pos"]//H
    D["z5"] = D.prior5/(D.vol20*np.sqrt(5))
    def ct(sub, col="unus"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 3: return (len(sub), np.nan, np.nan, np.nan)
        m = sub[col].mean(); dev = (sub[col]-m).groupby(sub["day"]).sum(); G = len(dev)
        se = np.sqrt((dev**2).sum()*G/max(G-1,1))/len(sub)
        return (len(sub), G, m, m/se if se > 0 else np.nan)
    fpc = lambda s: s.sort_values("pos").groupby(["coin","win","cell"]).head(1)
    out = {}
    # A: wide flat days, graded by z5 (continuation along prior run?)
    wf = fpc(D[(D.width>=1.5)&(D.body<=0.1)]).dropna(subset=["z5","unus"]).copy()
    wf["dunus"] = wf.unus*np.sign(wf.prior5)
    out["wideflat_unus_in_prior_dir"] = pd.Series(ct(wf,"dunus"), index=["n","days","mean","t"])
    wf["q"] = pd.qcut(wf.z5, 4, labels=False); res=[]
    for q,S in wf.groupby("q"): res.append([q,S.z5.mean(),*ct(S)])
    out["wideflat_by_z5"] = pd.DataFrame(res, columns=["q","z5","n","days","mean_unus","t"])
    out["wideflat_spearman_z5_unus"] = pd.Series(stats.spearmanr(wf.z5, wf.unus), index=["rho","p"])
    # B: wide days, signed body continuation graded by |sbody| and width
    wd = fpc(D[D.width>=1.5]).dropna(subset=["sbody","unus"]).copy()
    wd["dunus"] = wd.unus*np.sign(wd.sbody)
    wd["bq"] = pd.qcut(wd.sbody.abs(), 4, labels=False); res=[]
    for q,S in wd.groupby("bq"): res.append([q,S.sbody.abs().mean(),*ct(S,"dunus")])
    out["wide_by_absbody_fwd_in_body_dir"] = pd.DataFrame(res, columns=["q","absbody","n","days","mean","t"])
    res=[]
    for y,S in wd[wd.sbody.abs()>=0.5].groupby("year"): res.append([y,*ct(S,"dunus")])
    out["wide_strongbody_by_year"] = pd.DataFrame(res, columns=["year","n","days","mean","t"])
    # C: grid: after large 1-day moves (z1), fwd5 in move direction, graded
    G0 = D[D.pos%H==0].dropna(subset=["z1","unus"]).copy()
    G0["d"] = G0.unus*np.sign(G0.z1)
    G0["q"] = pd.qcut(G0.z1.abs(), 5, labels=False); res=[]
    for q,S in G0.groupby("q"): res.append([q,S.z1.abs().mean(),*ct(S,"d")])
    out["grid_fwd5_in_dir_of_today_by_absz1"] = pd.DataFrame(res, columns=["q","absz1","n","days","mean","t"])
    # D: book: positions and trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
        "win_share": (T.net_profit_loss_percent>0).mean(), "median_net": T.net_profit_loss_percent.median(),
        "mean_gross": T.profit_loss_percent.mean()})
    out["trades_by_coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count","mean"])
    # E: weekday 1-day, split halves of years for stability (Saturday)
    D["wd"] = pd.to_datetime(D.day).dt.weekday
    D["u1"] = D.r1 - D.groupby("coin").r1.transform("mean")
    res=[]
    for half,S in D[D.wd==5].groupby(D.year<=D.year.median()): res.append([half,*ct(S,"u1")])
    out["saturday_by_half"] = pd.DataFrame(res, columns=["early","n","days","mean","t"])
    return out
