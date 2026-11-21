def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; allgrid = []
    drift = {}
    for coin, wins in data["bars"].items():
        r18 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c)-18, 18)
            r18 += list(c[idx+18]/c[idx]-1)
        drift[coin] = (np.mean(r18), np.std(r18))
    for coin, wins in data["bars"].items():
        d18, s18 = drift[coin]
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            plow = l.shift(1).rolling(12).min(); phigh = h.shift(1).rolling(12).max()
            srange = (phigh - plow)/c
            mbr = ((h-l)/c).rolling(180).mean()
            narrow = mbr/srange
            ret180 = c/c.shift(180)-1
            ret30b = c/c.shift(6*7)-1
            f = {H: c.shift(-H)/c-1 for H in (18, 36, 72)}
            vol = c.pct_change().rolling(180).std()
            n = len(b)
            for start in range(0, n-18, 18):
                cell = b.iloc[start:start+18]
                # tested cases approx: first bar in cell with forecast <= -2
                m = np.where(cell["forecast"].values <= -2)[0]
                if len(m):
                    i = start+m[0]
                    rows.append(dict(coin=coin, w=w, yr=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i],'year') else pd.to_datetime(b["timestamp"].iloc[i]).year,
                        fc=b["forecast"].iloc[i], narrow=narrow.iloc[i], depth=(plow.iloc[i]-c.iloc[i])/c.iloc[i],
                        ret180=ret180.iloc[i], ret7=ret30b.iloc[i], vol=vol.iloc[i],
                        u18=-(f[18].iloc[i]-d18), t18=-f[18].iloc[i], t36=-f[36].iloc[i], t72=-f[72].iloc[i], s18=s18))
                # all-bars grid breakouts any regime
                i = start
                for side, cond in (("down", c.iloc[i] < plow.iloc[i]), ("up", c.iloc[i] > phigh.iloc[i])):
                    if cond and not np.isnan(ret180.iloc[i]):
                        allgrid.append(dict(side=side, up30=ret180.iloc[i] > 0, narrowq=narrow.iloc[i],
                                            r18=f[18].iloc[i]-d18, tot18=f[18].iloc[i], r72=f[72].iloc[i]))
    df = pd.DataFrame(rows)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["cases_overall"] = pd.DataFrame({c: summ(df, c) for c in ["u18", "t18", "t36", "t72"]}).T
    out["fc_dist"] = df["fc"].describe()
    for v in ["narrow", "depth", "ret180", "ret7", "vol"]:
        df["q"] = pd.qcut(df[v], 5, labels=False, duplicates="drop")
        out["by_"+v+"_q5"] = df.groupby("q").apply(lambda g: pd.Series({"med": g[v].median(), **summ(g, "t18").to_dict(), "t72%": 100*g["t72"].mean()}))
    out["by_year_t18"] = df.groupby("yr").apply(lambda g: summ(g, "t18"))
    out["by_window_t18"] = df.groupby("w").apply(lambda g: summ(g, "t18"))
    ag = pd.DataFrame(allgrid)
    out["breaks_any_regime"] = ag.groupby(["side", "up30"]).apply(lambda g: pd.Series({"n": len(g), "unus18% (long dir)": 100*g["r18"].mean(), "tot18%": 100*g["tot18"].mean(), "tot72%": 100*g["r72"].mean(), "t_tot18": g["tot18"].mean()/(g["tot18"].std()/np.sqrt(len(g)))}))
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    daily = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    wmap = D.groupby("day")["w"].first()
    daily["w"] = wmap.reindex(daily.index)
    out["book_by_window"] = daily.groupby("w").agg(book_mean_bps=("book_return", lambda x: 1e4*x.mean()), hold_mean_bps=("coin_return", lambda x: 1e4*x.mean()), days=("book_return", "size"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades"] = pd.Series({"n": len(T), "mean_gross%": T["profit_loss_percent"].mean(), "mean_net%": T["net_profit_loss_percent"].mean(), "win%": 100*(T["net_profit_loss_percent"] > 0).mean(), "med_dur_h": T["duration_minutes"].median()/60})
    return out
