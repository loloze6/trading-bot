def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    hs = [1,2,3,5,10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in hs}
        for w, b in wins.items():
            c = b["close"].values
            for h in hs:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values
            f = b["forecast"].fillna(0).values
            n = len(b)
            loc = np.where(hi > lo, (c-lo)/(hi-lo), np.nan)
            low_since = 0.0; last_cell = -1; taken = False
            for t in range(n):
                s = -f[t]; cell = t // 10
                if cell != last_cell:
                    taken = False; last_cell = cell
                if s - low_since >= 2 and not taken:
                    taken = True; low_since = s
                    r = {"coin": coin, "win": w, "loc": loc[t], "fc": s, "day": b["timestamp"].iloc[t]}
                    for h in hs:
                        if t+h < n:
                            r[f"un{h}"] = -(c[t+h]/c[t]-1-drift[coin][h])
                    rows.append(r)
                else:
                    low_since = min(low_since, s)
    d = pd.DataFrame(rows)
    def tc(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return (len(x), np.nan, np.nan)
        m = x[col].mean()
        g = (x[col]-m).groupby(x["day"]).sum(); G = len(g)
        se = np.sqrt(G/(G-1)*(g**2).sum())/len(x)
        return (len(x), m, m/se)
    out = {}
    d["hiclose"] = np.where(d["loc"] >= 0.8, "loc>=0.8", "loc<0.8")
    out["loc_split_by_horizon"] = pd.DataFrame({(k, h): tc(g, f"un{h}") for k, g in d.groupby("hiclose") for h in hs}, index=["n","mean_un","t"]).T
    hi = d[d["loc"] >= 0.8]
    out["hi_by_coin"] = pd.DataFrame({k: tc(g, "un10") for k, g in hi.groupby("coin")}, index=["n","mean_un","t"]).T
    hi = hi.assign(year=pd.to_datetime(hi["day"]).dt.year)
    out["hi_by_year"] = pd.DataFrame({k: tc(g, "un10") for k, g in hi.groupby("year")}, index=["n","mean_un","t"]).T
    out["corr_loc_fc"] = float(d[["loc","fc"]].corr().iloc[0,1])
    lo_ = d[d["loc"] < 0.8]
    out["lo_by_year"] = pd.DataFrame({k: tc(g, "un10") for k, g in lo_.assign(year=pd.to_datetime(lo_["day"]).dt.year).groupby("year")}, index=["n","mean_un","t"]).T
    return out
