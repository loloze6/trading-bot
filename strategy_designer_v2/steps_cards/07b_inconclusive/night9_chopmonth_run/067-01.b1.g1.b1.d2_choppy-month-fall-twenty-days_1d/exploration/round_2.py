def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    H = [5, 10, 20]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            fc = b["forecast"].fillna(0).values
            raw = b.get("debug_info.components.fall30.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            r30 = pd.Series(cl).pct_change(30).values * 100
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            lr = np.log(pd.Series(cl)).diff()
            v30 = lr.rolling(30).std()
            vmed = v30.rolling(90, min_periods=30).median().values
            v30 = v30.values
            for h in H:
                low = 0.0
                last_cell = -1
                for i in range(n):
                    mag = -fc[i]
                    if mag <= 0:
                        low = 0.0
                        continue
                    if mag - low >= 2:
                        cell = i // h
                        if cell != last_cell and i + h < n:
                            fwd = cl[i + h] / cl[i] - 1
                            rows.append(dict(coin=c, win=w, h=h, day=day[i], fc=fc[i], r30=r30[i], raw=raw[i],
                                             unus=-(fwd - drift[(c, h)]), tot=-fwd,
                                             agit=(v30[i] > vmed[i]) if not np.isnan(vmed[i]) else np.nan))
                            last_cell = cell
                        low = mag
    df = pd.DataFrame(rows)
    def summ(g):
        d = g.groupby("day")["unus"].sum()
        nd = len(d)
        m = g["unus"].mean()
        se = d.std(ddof=1) * np.sqrt(nd) / len(g) if nd > 1 else np.nan
        return pd.Series(dict(cases=len(g), days=nd, mean_unus=m, t_pooled=m / se if se else np.nan,
                              mean_total=g["tot"].mean(), mean_r30=g["r30"].mean()))
    out["cases_by_h"] = df.groupby("h").apply(summ)
    df["fcband"] = pd.cut(df["fc"], [-21, -10, -5, -2, 0], labels=["<=-10", "-10..-5", "-5..-2", ">-2"])
    out["cases_by_h_fc"] = df.groupby(["h", "fcband"]).apply(summ)
    df["r30band"] = pd.cut(df["r30"], [-1000, -20, -10, -5, 0, 1000], labels=["<-20", "-20..-10", "-10..-5", "-5..0", ">0"])
    out["cases_by_h_r30"] = df.groupby(["h", "r30band"]).apply(summ)
    out["cases_by_h_agit"] = df.dropna(subset=["agit"]).groupby(["h", "agit"]).apply(summ)
    d10 = df[df.h == 10]
    out["cases10_by_win"] = d10.groupby("win").apply(summ)
    out["corr_fc_unus_by_h"] = df.groupby("h").apply(lambda g: pd.Series(dict(corr_fc=np.corrcoef(-g["fc"], g["unus"])[0, 1],
                                                                             corr_r30=np.corrcoef(-g["r30"].fillna(0), g["unus"])[0, 1])))
    return out
