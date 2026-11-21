def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def build(H, off):
        recs = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.sort_values("timestamp").reset_index(drop=True)
                c = b["close"].values.astype(float); n = len(c)
                if n < H + 25: continue
                r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
                vol20 = pd.Series(np.log1p(r1)).rolling(20).std().values
                r3 = pd.Series(c).pct_change(3).values
                ret10 = pd.Series(c).pct_change(10).values
                ts = pd.to_datetime(b["timestamp"])
                for i in range(off, n - H, H):
                    recs.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, z1=r1[i]/vol20[i], z3=r3[i]/(vol20[i]*np.sqrt(3)),
                                     z10=ret10[i]/(vol20[i]*np.sqrt(10)), wd=ts[i].dayofweek, yr=ts[i].year, day=str(ts[i].date())))
        df = pd.DataFrame(recs)
        g = df.groupby("coin")["fwd"]
        df["unu"] = df["fwd"] - g.transform("mean"); df["str"] = df["unu"]/g.transform("std")
        for k in ["z1","z3","z10"]:
            df[k+"q"] = df.groupby("coin")[k].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        return df
    def summ(g):
        x = g["unu"].dropna()
        d = g.groupby("day")["unu"].mean()
        return pd.Series({"n": len(x), "days": len(d), "mean_unu": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))),
                          "t_by_day": d.mean()/(d.std()/np.sqrt(len(d))), "strength": g["str"].mean()})
    A = build(10, 0); B = build(10, 5); C = build(5, 0); E = build(20, 0)
    out["z1q_H10_off0"] = A.groupby("z1q").apply(summ)
    out["z1q_H10_off5"] = B.groupby("z1q").apply(summ)
    out["z1q_H5"] = C.groupby("z1q").apply(summ)
    out["z1q_H20"] = E.groupby("z1q").apply(summ)
    out["z3q_H10"] = A.groupby("z3q").apply(summ)
    out["z10q_H10_off0"] = A.groupby("z10q").apply(summ)
    out["z10q_H10_off5"] = B.groupby("z10q").apply(summ)
    out["z10q_H20"] = E.groupby("z10q").apply(summ)
    out["weekday_off5"] = B.groupby("wd").apply(summ)
    AB = pd.concat([A, B])
    out["z1_bottom_by_year"] = AB[AB["z1q"]==0].groupby("yr").apply(summ)
    out["z10_top_by_year"] = AB[AB["z10q"]==4].groupby("yr").apply(summ)
    big = ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]
    AB["grp"] = np.where(AB["coin"].isin(big), "old6", "new13")
    out["z1_bottom_by_group"] = AB[AB["z1q"]==0].groupby("grp").apply(summ)
    out["z10_top_by_group"] = AB[AB["z10q"]==4].groupby("grp").apply(summ)
    # graded: deciles of z1 within bottom
    for k in ["z1","z10"]:
        s = AB[[k,"str"]].dropna(); rho, p = stats.spearmanr(s[k], s["str"])
        out["spearman_"+k+"_both_offsets"] = f"rho={rho:.4f} p={p:.3g} n={len(s)}"
    # interaction: z1 bottom split by z10 sign
    sub = AB[AB["z1q"]==0].copy(); sub["z10pos"] = np.where(sub["z10"]>0,"z10>0","z10<=0")
    out["z1_bottom_by_z10sign"] = sub.groupby("z10pos").apply(summ)
    return out
