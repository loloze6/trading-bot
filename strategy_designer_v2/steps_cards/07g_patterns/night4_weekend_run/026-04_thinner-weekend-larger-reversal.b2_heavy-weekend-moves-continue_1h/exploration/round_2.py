def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; hr = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            hr.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "hour": ts.dt.hour, "r": r1}))
            idx = np.where(ts.dt.hour.values == 23)[0]
            for i in idx:
                if i-168 < 0 or i+48 >= n: continue
                past24 = c[i]/c[i-24]-1; fut24 = c[i+24]/c[i]-1
                past48 = c[i]/c[i-48]-1; fut48 = c[i+48]/c[i]-1
                v24 = v[i-23:i+1].mean(); vb = v[i-167:i-23].mean()
                vr24 = v24/vb if vb > 0 else np.nan
                volw = v[i-47:i+1].mean(); volb = v[i-167:i-47].mean()
                vr48 = volw/volb if volb > 0 else np.nan
                rows.append((coin, w, ts.iloc[i].year, ts.iloc[i].weekday(), i, past24, fut24, past48, fut48, vr24, vr48))
    R = pd.DataFrame(rows, columns=["coin","w","year","wd","i","p24","f24","p48","f48","vr24","vr48"])
    R["sd24"] = R.groupby("coin")["p24"].transform("std")
    R["s24"] = np.sign(R.p24)*(R.f24 - R.groupby("coin")["f24"].transform("mean"))
    R["s48"] = np.sign(R.p48)*(R.f48 - R.groupby("coin")["f48"].transform("mean"))
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    R["mq"] = R.groupby("coin")["p24"].transform(lambda x: pd.qcut(x.abs(), 5, labels=False))
    out["s24_by_abs24_quintile"] = R.groupby("mq")["s24"].apply(tt).unstack()
    R["v24q"] = pd.qcut(R["vr24"], 5, labels=False)
    out["s24_by_vr24_quintile"] = R.groupby("v24q")["s24"].apply(tt).unstack()
    out["s24_top2_absmove_by_year"] = R[R.mq >= 3].groupby("year")["s24"].apply(tt).unstack()
    out["s24_top2_absmove_by_coin"] = R[R.mq >= 3].groupby("coin")["s24"].apply(tt).unstack()
    R["wgrp"] = R["w"].str[1:].astype(int).map(lambda k: "w1-8" if k <= 8 else ("w9-16" if k <= 16 else "w17-24"))
    out["s24_top2_absmove_by_wgroup"] = R[R.mq >= 3].groupby("wgrp")["s24"].apply(tt).unstack()
    # scaled return regression-like: mean of -f24 * sign weighted by |p24|/sd
    R["z"] = R.p24.abs()/R.sd24
    out["corr_z_s24"] = float(R[["z","s24"]].corr().iloc[0,1])
    # 48h continuation, non-overlapping (every other day), top vr48 quintile
    E = R[(R.i // 24) % 2 == 0].copy()
    E["v48q"] = pd.qcut(E["vr48"], 5, labels=False)
    out["s48_nonoverlap_by_vr48_quintile"] = E.groupby("v48q")["s48"].apply(tt).unstack()
    H = pd.concat(hr)
    H["r"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    H20 = H[H.hour.isin([20,21])]
    out["h20_21_by_year"] = H20.groupby("year")["r"].apply(tt).unstack()
    out["h20_21_by_coin"] = H20.groupby("coin")["r"].apply(tt).unstack()
    return out
