def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = [5, 10, 26]
    rows = []
    usual = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            vol20 = r1.rolling(20).std()
            ret26 = s / s.shift(26) - 1
            ret5 = s / s.shift(5) - 1
            h26 = hi.rolling(26).max(); l26 = lo.rolling(26).min()
            pos26 = (s - l26) / (h26 - l26)
            mid9 = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            mid26 = (h26 + l26) / 2
            tk = (mid9 - mid26) / s
            fc = b["forecast"].astype(float).values
            reg = (b["regime"] == "trending").astype(int).values
            wd = pd.to_datetime(b["timestamp"]).dt.weekday.values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, fwd=c[i+h]/c[i]-1,
                        r1=r1.iloc[i], vol20=vol20.iloc[i], ret26=ret26.iloc[i], ret5=ret5.iloc[i],
                        pos26=pos26.iloc[i], tk=tk.iloc[i], fc=fc[i], reg=reg[i], wd=wd[i]))
    df = pd.DataFrame(rows)
    df["mu"] = df.groupby(["coin","h"])["fwd"].transform("mean")
    df["sd"] = df.groupby(["coin","h"])["fwd"].transform("std")
    df["ex"] = df["fwd"] - df["mu"]
    df["z"] = df["ex"] / df["sd"]
    res = []
    for h in H:
        d = df[df.h == h]
        for f in ["r1","ret5","ret26","pos26","tk","vol20","fc"]:
            dd = d.dropna(subset=[f,"z"])
            # per-coin rank of feature to quintile
            q = dd.groupby("coin")[f].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if len(x) >= 10 else np.nan)
            dd = dd.assign(q=q).dropna(subset=["q"])
            rho, p = stats.spearmanr(dd[f], dd["z"])
            top = dd[dd.q == 4]["z"]; bot = dd[dd.q == 0]["z"]
            t = stats.ttest_ind(top, bot, equal_var=False).statistic
            res.append(dict(h=h, feat=f, n=len(dd), rho=round(rho,3), p=round(p,4),
                            z_q0=round(bot.mean(),3), z_q2=round(dd[dd.q==2]["z"].mean(),3), z_q4=round(top.mean(),3),
                            ex_q0=round(dd[dd.q==0]["ex"].mean(),4), ex_q4=round(dd[dd.q==4]["ex"].mean(),4), t_q4_q0=round(t,2)))
    out["feature_quintiles"] = pd.DataFrame(res)
    # regime trending vs not
    rr = []
    for h in H:
        d = df[df.h == h].dropna(subset=["z"])
        a = d[d.reg==1]; b_ = d[d.reg==0]
        rr.append(dict(h=h, n_tr=len(a), n_un=len(b_), ex_tr=a.ex.mean(), ex_un=b_.ex.mean(),
                       t=stats.ttest_ind(a.z, b_.z, equal_var=False).statistic))
    out["regime"] = pd.DataFrame(rr)
    d5 = df[df.h == 5].dropna(subset=["z"])
    out["weekday_h5"] = d5.groupby("wd").agg(n=("z","size"), z=("z","mean"), ex=("ex","mean"))
    # daily bars: next-day return after large daily move, by vol tercile
    dl = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            s = b.sort_values("timestamp")["close"].astype(float).reset_index(drop=True)
            r = s.pct_change(); v = r.rolling(20).std().shift(1)
            zz = r / v
            dl.append(pd.DataFrame(dict(coin=coin, z=zz, nxt=r.shift(-1), nxt3=s.shift(-3)/s-1, v=v)))
    dl = pd.concat(dl).dropna()
    dl["nxt_ex"] = dl["nxt"] - dl.groupby("coin")["nxt"].transform("mean")
    dl["zb"] = pd.cut(dl["z"], [-99,-2,-1,0,1,2,99])
    g = dl.groupby("zb", observed=True)
    out["daily_after_move"] = g.agg(n=("nxt","size"), nxt_ex_bps=("nxt_ex", lambda x: x.mean()*1e4),
                                   t=("nxt_ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # book: daily returns by regime held
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, win=w))
    bk = pd.concat(bk)
    out["book_overall"] = pd.Series(dict(book_mean=bk.book_return.mean(), coin_mean=bk.coin_return.mean(),
                                         corr=bk[["book_return","coin_return"]].corr().iloc[0,1]))
    return out
