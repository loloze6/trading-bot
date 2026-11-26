def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allsd = []
        for w, b in wins.items():
            r = b["close"].astype(float).pct_change()
            allsd.append(r.rolling(30).std())
        med = pd.concat(allsd).median()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            rec = b["debug_info.components.vol_shift.last_history_value"] if "debug_info.components.vol_shift.last_history_value" in b else pd.Series(np.nan, index=b.index)
            vrr = vr.fillna(rec.astype(float))
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            falling = b["regime"] != "chop"
            alloc = b["postRebalance_current_allocation"].astype(float)
            for H in (5, 10, 20):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, fwd=fwd[i], vr=vrr[i], r20=r20[i], r60=r60[i],
                                     fall=bool(falling[i]), agit=(sd30[i] > med) if not np.isnan(sd30[i]) else np.nan,
                                     reg=b["regime"][i], pos=np.sign(alloc[i])))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin","H"])["fwd"].transform("mean")
    def sp(s, col):
        s = s.dropna(subset=[col,"ex"])
        if len(s) < 15: return (len(s), np.nan, np.nan)
        r = stats.spearmanr(s[col], s["ex"]); return (len(s), round(r[0],3), round(r[1],4))
    res = []
    for H in (5,10,20):
        d = df[df.H==H]
        for lab, s in [("fall", d[d.fall]), ("fall_calm", d[d.fall & (d.agit==False)]), ("fall_agit", d[d.fall & (d.agit==True)]),
                       ("fall_r20neg", d[d.fall & (d.r20<0)]), ("fall_r20pos", d[d.fall & (d.r20>=0)]),
                       ("notfall", d[~d.fall]), ("rising60", d[d.r60>0.1]), ("notfall_calm", d[~d.fall & (d.agit==False)]), ("notfall_agit", d[~d.fall & (d.agit==True)])]:
            n_, rho, p = sp(s, "vr"); res.append(dict(H=H, grp=lab, n=n_, rho_vr=rho, p=p))
            n_, rho, p = sp(s, "r20"); res[-1].update(rho_r20=rho, p20=p)
    out["spearman_grid"] = pd.DataFrame(res).set_index(["H","grp"])
    d = df[(df.H==10)]
    # r20 momentum by window and by year sign
    g = d.dropna(subset=["r20","ex"]).groupby("w").apply(lambda s: pd.Series(dict(n=len(s), rho=stats.spearmanr(s.r20, s.ex)[0]))).round(3)
    out["r20_rho_by_window"] = g
    gf = d[d.fall].dropna(subset=["vr","ex"]).groupby("w").apply(lambda s: pd.Series(dict(n=len(s), rho=stats.spearmanr(s.vr, s.ex)[0]) if len(s)>5 else pd.Series(dict(n=len(s), rho=np.nan)))).round(3)
    out["vr_fall_rho_by_window"] = gf
    # in falling, quartiles of vr, by agitation, H=10
    s = d[d.fall].dropna(subset=["vr","ex","agit"]).copy()
    s["q"] = pd.qcut(s.vr, 4, labels=False)
    t = s.groupby(["agit","q"])["ex"].agg(["count","mean","std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["vr_q_fall_by_agit_H10"] = t.round(4)
    # not-falling, vr quartiles H10 by agitation
    s = d[~d.fall].dropna(subset=["vr","ex","agit"]).copy()
    s["q"] = pd.qcut(s.vr, 4, labels=False)
    t = s.groupby(["agit","q"])["ex"].agg(["count","mean","std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["vr_q_notfall_by_agit_H10"] = t.round(4)
    # book: days by position side
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bb = data["bars"][coin][w].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            al = bb.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            x = dd.copy(); x["day"] = pd.to_datetime(x["day"]).dt.floor("D")
            x = x.merge(al.rename("al").reset_index(), on="day", how="left")
            bk.append(x)
    bk = pd.concat(bk).dropna(subset=["book_return"])
    bk["side"] = np.sign(bk["al"]).map({1:"long",-1:"short",0:"flat"})
    out["book_by_side"] = bk.groupby("side")["book_return"].agg(["count","mean","std"]).assign(mean_pct=lambda x: x["mean"]*100).round(5)
    return out
