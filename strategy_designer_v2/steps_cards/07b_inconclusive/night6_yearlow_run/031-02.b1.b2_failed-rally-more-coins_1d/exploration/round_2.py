def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    H_list = [5, 10, 20, 40]
    rows = []
    cm = {}
    for coin, wins in bars.items():
        for H in H_list:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            cm[(coin, H)] = np.mean(rets) if rets else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            for H in H_list:
                for i in range(0, len(c) - H, H):
                    if reg[i] != "trending" or pd.isna(f[i]) or f[i] == 0:
                        continue
                    r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    ex = c[i + H] / c[i] - 1 - cm[(coin, H)]
                    rows.append(dict(coin=coin, H=H, f=f[i], ex=ex, r60=r60,
                                     year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)

    def tday(sub):
        s = sub.groupby("day")["ex"].sum()
        if len(s) < 3: return np.nan, len(s)
        return s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), len(s)

    out = {}
    res = []
    for H in H_list:
        s = d[d.H == H]
        for name, sub in [("f<=-3", s[s.f <= -3]), ("-3<f<0", s[(s.f > -3) & (s.f < 0)]),
                          ("0<f<3", s[(s.f > 0) & (s.f < 3)]), ("f>=3", s[s.f >= 3])]:
            t, nd = tday(sub)
            res.append(dict(H=H, grp=name, n=len(sub), days=nd, ex=sub.ex.mean(), t=t))
    out["excess by forecast group and horizon"] = pd.DataFrame(res)
    s = d[(d.H == 20) & (d.f < 0)].copy()
    out["H20 short side by year"] = s.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean"))
    s2 = s.dropna(subset=["r60"]).copy()
    if len(s2) > 20:
        s2["r60q"] = pd.qcut(s2.r60, 3, duplicates="drop")
        out["H20 short side by 60d return tercile"] = s2.groupby("r60q", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"))
    out["H20 short side share with r60 known"] = float(s.r60.notna().mean())
    return out
