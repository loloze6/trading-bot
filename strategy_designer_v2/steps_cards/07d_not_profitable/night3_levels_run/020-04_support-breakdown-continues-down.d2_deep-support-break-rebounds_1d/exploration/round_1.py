def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 5
    rows = []
    daily = []
    for coin, ws in data["bars"].items():
        # coin mean 5-bar return over all windows
        grid_rets = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            grid_rets += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(grid_rets); usual = np.std(grid_rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            f = b["forecast"].fillna(0)
            raw = b["debug_info.components.support_break.last_history_value"]
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r1 = c / c.shift(1) - 1
            vol20 = r1.rolling(20).std()
            ma50 = c.rolling(50).mean()
            dd = c / c.rolling(60, min_periods=10).max() - 1
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                fr = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, f=f.iloc[i], raw=raw.iloc[i], r20=r20.iloc[i],
                                 r60=r60.iloc[i], r1=r1.iloc[i], vol=vol20.iloc[i],
                                 abv=float(c.iloc[i] > ma50.iloc[i]) if not np.isnan(ma50.iloc[i]) else np.nan,
                                 dd=dd.iloc[i], fr=fr, un=fr - drift, st=(fr - drift) / usual))
        for w, d in data["days"][coin].items():
            bb = data["bars"][coin][w]
            daily.append(pd.DataFrame(dict(coin=coin, w=w, br=d["book_return"].values, cr=d["coin_return"].values)))
    df = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), un=g.un.mean(), t=g.un.mean() / (g.un.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              tot=g.fr.mean(), st=g.st.mean()))
    act = df[df.f > 0].copy()
    out["active_vs_all"] = pd.DataFrame({"active": summ(act), "inactive": summ(df[df.f <= 0]), "all": summ(df)})
    act["fq"] = pd.qcut(act.f.rank(method="first"), 5, labels=False)
    out["by_forecast_quint"] = act.groupby("fq").apply(summ)
    act["rq"] = pd.qcut(act.raw.rank(method="first"), 5, labels=False)
    out["by_raw_quint"] = act.groupby("rq").apply(summ)
    # raw>0 situation (support broken) broadly
    sit = df[df.raw > 0].copy()
    out["raw_pos_vs_zero"] = pd.DataFrame({"raw>0": summ(sit), "raw==0": summ(df[df.raw == 0])})
    sit["r20q"] = pd.qcut(sit.r20, 4, labels=False)
    out["sit_by_r20q"] = sit.groupby("r20q").apply(summ)
    out["sit_by_abv_ma50"] = sit.groupby("abv").apply(summ)
    sit["volq"] = pd.qcut(sit.vol, 4, labels=False)
    out["sit_by_volq"] = sit.groupby("volq").apply(summ)
    sit["ddq"] = pd.qcut(sit.dd, 4, labels=False)
    out["sit_by_ddq"] = sit.groupby("ddq").apply(summ)
    out["all_by_ddq"] = df.assign(ddq=pd.qcut(df.dd, 5, labels=False)).groupby("ddq").apply(summ)
    out["all_by_r1q"] = df.assign(q=pd.qcut(df.r1, 5, labels=False)).groupby("q").apply(summ)
    dd_ = pd.concat(daily)
    out["book_daily"] = pd.Series(dict(book_mean=dd_.br.mean(), coin_mean=dd_.cr.mean(), book_sd=dd_.br.std()))
    out["by_coin_active"] = act.groupby("coin").apply(summ)
    # exposure
    expo = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            expo.append(b["postRebalance_current_allocation"].fillna(0).values)
    e = np.concatenate(expo)
    out["exposure"] = pd.Series(dict(share_in=(e > 0).mean(), mean_alloc=e.mean(), mean_when_in=e[e > 0].mean()))
    return out
