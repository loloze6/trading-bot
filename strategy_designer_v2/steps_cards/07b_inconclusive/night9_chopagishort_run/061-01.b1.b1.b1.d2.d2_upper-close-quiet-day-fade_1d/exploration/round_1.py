def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in [1,2,3,5,10,20]}
        for w, b in wins.items():
            c = b["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        usual[coin] = np.std(allr[H], ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values
            f = b["forecast"].fillna(0).values
            n = len(b)
            loc = np.where(hi > lo, (c-lo)/(hi-lo), np.nan)
            ret = pd.Series(c).pct_change()
            vsr = (ret/ret.rolling(20).std()).values
            low_since = 0.0
            last_cell = -1
            for t in range(n):
                s = -f[t]
                cell = t // H
                if cell != last_cell:
                    taken = False
                    last_cell = cell
                if s - low_since >= 2 and not taken:
                    taken = True
                    low_since = s
                    r = {"coin": coin, "win": w, "t": t, "fc": s, "loc": loc[t], "vsr": vsr[t],
                         "day": b["timestamp"].iloc[t], "regime": b["regime"].iloc[t]}
                    for h in [1,2,3,5,10,20]:
                        if t+h < n:
                            r[f"tot{h}"] = -(c[t+h]/c[t]-1)
                            r[f"un{h}"] = -(c[t+h]/c[t]-1-drift[coin][h])
                    r["str"] = r.get("un10", np.nan)/usual[coin]
                    rows.append(r)
                else:
                    low_since = min(low_since, s)
    d = pd.DataFrame(rows)
    def tc(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return (len(x), np.nan, np.nan)
        m = x[col].mean()
        g = (x[col]-m).groupby(x["day"]).sum()
        G = len(g)
        se = np.sqrt(G/(G-1)*(g**2).sum())/len(x) if G > 1 else np.nan
        return (len(x), m, m/se)
    out = {}
    hz = pd.DataFrame({h: tc(d, f"un{h}") for h in [1,2,3,5,10,20]}, index=["n","mean_un","t"]).T
    hz["mean_tot"] = [d[f"tot{h}"].mean() for h in [1,2,3,5,10,20]]
    out["by_horizon"] = hz
    out["by_coin"] = pd.DataFrame({k: tc(g, "un10") for k, g in d.groupby("coin")}, index=["n","mean_un","t"]).T
    out["by_window"] = pd.DataFrame({k: tc(g, "un10") for k, g in d.groupby("win")}, index=["n","mean_un","t"]).T
    d["year"] = pd.to_datetime(d["day"]).dt.year
    out["by_year"] = pd.DataFrame({k: tc(g, "un10") for k, g in d.groupby("year")}, index=["n","mean_un","t"]).T
    d["fq"] = pd.qcut(d["fc"], 4, labels=False, duplicates="drop")
    out["by_fc_quart"] = pd.DataFrame({k: tc(g, "un10") + (g["fc"].mean(),) for k, g in d.groupby("fq")}, index=["n","mean_un","t","fc"]).T
    d["lq"] = pd.cut(d["loc"], [0,0.6,0.7,0.8,0.9,1.01])
    out["by_loc"] = pd.DataFrame({str(k): tc(g, "un10") for k, g in d.groupby("lq")}, index=["n","mean_un","t"]).T
    d["vq"] = pd.cut(d["vsr"], [-10,0,0.25,0.5,0.75,1.0,10])
    out["by_vsr"] = pd.DataFrame({str(k): tc(g, "un10") for k, g in d.groupby("vq")}, index=["n","mean_un","t"]).T
    out["regime_counts"] = d["regime"].value_counts()
    out["corr_loc_un10"] = float(d[["loc","un10"]].dropna().corr().iloc[0,1])
    out["corr_fc_un10"] = float(d[["fc","un10"]].dropna().corr().iloc[0,1])
    out["mean_str"] = float(d["str"].mean())
    out["median_un10"] = float(d["un10"].median())
    out["share_pos_un10"] = float((d["un10"] > 0).mean())
    return out
