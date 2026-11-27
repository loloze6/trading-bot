import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    # coin drift per horizon on non-overlapping grids, all windows
    drift = {}
    usual = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else 0.0
            usual[(c, h)] = np.std(rs) if rs else np.nan
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; hi = df["high"]; lo = df["low"]
            loc = (cl - lo) / (hi - lo)
            pe5 = cl / cl.shift(5) - 1
            pe60 = cl / cl.shift(60) - 1
            r1 = cl.pct_change()
            vol30 = r1.rolling(30).std()
            vol10 = r1.rolling(10).std()
            f = df["forecast"].fillna(0)
            sig = (f <= -2) & ((f.shift(1).fillna(0) - f) >= 2)
            n = len(df)
            seen = set()
            for i in np.where(sig.values)[0]:
                cell = i // 5
                if cell in seen:
                    continue
                seen.add(cell)
                if i + 5 >= n:
                    continue
                rec = dict(coin=c, window=w, i=i, day=str(df["timestamp"].iloc[i])[:10],
                           year=str(df["timestamp"].iloc[i])[:4], loc=loc.iloc[i], pe5=pe5.iloc[i],
                           pe60=pe60.iloc[i], f=abs(f.iloc[i]), v30=vol30.iloc[i], v10=vol10.iloc[i],
                           dayret=r1.iloc[i])
                for h in H:
                    if i + h < n:
                        ret = cl.iloc[i + h] / cl.iloc[i] - 1
                        rec[f"u{h}"] = -(ret - drift[(c, h)])
                        rec[f"tot{h}"] = -ret
                        rec[f"s{h}"] = rec[f"u{h}"] / usual[(c, h)]
                rows.append(rec)
    d = pd.DataFrame(rows)

    def ct(x, days):
        m = x.notna(); x = x[m]; days = days[m]
        n = len(x)
        if n < 3: return (np.nan, n, 0)
        mu = x.mean()
        S = (x - mu).groupby(days).sum()
        G = len(S)
        se = np.sqrt((S ** 2).sum() * G / (G - 1)) / n
        return (mu, n, G, mu / se)

    out = {}
    hz = pd.DataFrame({f"h{h}": ct(d[f"u{h}"], d["day"]) for h in H}, index=["mean", "n", "days", "t"]).T
    hz["tot_mean"] = [d[f"tot{h}"].mean() for h in H]
    hz["strength"] = [d[f"s{h}"].mean() for h in H]
    out["by_horizon"] = hz

    def grp(col, labels=None):
        res = {}
        for k, g in d.groupby(col, observed=True):
            r = ct(g["u5"], g["day"])
            r2 = ct(g["u2"], g["day"])
            res[str(k)] = dict(mean5=r[0], n=r[1], days=r[2], t5=r[3] if len(r) > 3 else np.nan,
                               mean2=r2[0], t2=r2[3] if len(r2) > 3 else np.nan)
        return pd.DataFrame(res).T

    out["by_coin"] = grp("coin")
    out["by_window"] = grp("window")
    out["by_year"] = grp("year")
    d["pe5_q"] = pd.qcut(d["pe5"], 5, labels=False)
    out["by_pe5_quintile"] = grp("pe5_q")
    d["loc_b"] = pd.cut(d["loc"], [0.74, 0.85, 0.95, 1.01])
    out["by_loc"] = grp("loc_b")
    d["pe60_q"] = pd.qcut(d["pe60"], 4, labels=False)
    out["by_pe60_quartile"] = grp("pe60_q")
    d["vr"] = d["v10"] / d["v30"]
    d["vr_q"] = pd.qcut(d["vr"], 3, labels=False)
    out["by_vol10_over_vol30_tercile"] = grp("vr_q")
    d["dr_q"] = pd.qcut(d["dayret"], 3, labels=False)
    out["by_signal_day_return_tercile"] = grp("dr_q")
    out["pe5_quintile_means"] = d.groupby("pe5_q")[["pe5", "f"]].mean()
    out["n_cases"] = len(d)
    return out
