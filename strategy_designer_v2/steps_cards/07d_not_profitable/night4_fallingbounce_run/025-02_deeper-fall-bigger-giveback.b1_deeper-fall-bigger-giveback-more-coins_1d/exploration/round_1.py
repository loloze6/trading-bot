def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr) if allr else np.nan
        usual[coin] = np.std(allr) if allr else np.nan
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            z = r1 / sd.shift(1)
            r90 = c / c.shift(90) - 1
            fd = df.get("debug_info.components.fall_depth.last_history_value")
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(n):
                mr = df["regime"].iat[i] == "mean_reversion"
                zi = z.iat[i]
                if not mr and not (pd.notna(zi) and zi >= 2):
                    continue
                if i + H >= n:
                    continue
                rr = fd.iat[i] if (mr and fd is not None and pd.notna(fd.iat[i])) else r90.iat[i]
                f1 = c.iat[i + 1] / c.iat[i] - 1
                f5 = c.iat[i + H] / c.iat[i] - 1
                f10 = c.iat[i + 10] / c.iat[i] - 1 if i + 10 < n else np.nan
                rows.append(dict(coin=coin, w=w, cell=i // H, mr=mr, z=zi, r90=rr,
                                 r1=r1.iat[i], f1=f1, f5=f5, f10=f10,
                                 ex5=f5 - drift[coin], s5=(f5 - drift[coin]) / usual[coin],
                                 year=yr.iat[i], btc=None))
    d = pd.DataFrame(rows)
    d = d.drop_duplicates(["coin", "w", "cell"])
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), f1=g.f1.mean(), f5=g.f5.mean(), ex5=g.ex5.mean(),
                              t_ex5=g.ex5.mean() / (g.ex5.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              f10=g.f10.mean(), share_up5=(g.f5 > 0).mean()))
    mrd = d[d.mr]
    out["mr cases overall"] = summ(mrd).to_frame().T
    out["mr by r90 quintile"] = mrd.groupby(pd.qcut(mrd.r90, 5)).apply(summ)
    zz = d[d.z >= 2].dropna(subset=["r90"])
    zz = zz.assign(fall=np.where(zz.r90 < 0, "falling", "rising"))
    out["z>=2 bounces falling vs rising"] = zz.groupby("fall").apply(summ)
    out["falling by bounce size"] = zz[zz.fall == "falling"].groupby(pd.cut(zz[zz.fall == "falling"].z, [2, 2.5, 3, 4, 100])).apply(summ)
    out["mr by year"] = mrd.groupby("year").apply(summ)
    out["mr by coin"] = mrd.groupby("coin").apply(summ)
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            dd.append(df.assign(coin=coin, w=w))
    D = pd.concat(dd)
    out["days share in position"] = float((D.book_return.fillna(0) != 0).mean())
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = pd.Series(dict(n=len(tr), mean_pl=tr.profit_loss_percent.mean(),
                                   mean_net=tr.net_profit_loss_percent.mean(),
                                   win=(tr.profit_loss_percent > 0).mean()))
    return out
