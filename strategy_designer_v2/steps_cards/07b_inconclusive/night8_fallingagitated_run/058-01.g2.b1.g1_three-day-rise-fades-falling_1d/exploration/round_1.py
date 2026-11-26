import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 7, 10]
    # coin drift and usual move per horizon, non-overlapping grid over all visible windows
    drift = {}; usual = {}
    for c, ws in bars.items():
        for h in H:
            r = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            r = np.array(r)
            drift[(c, h)] = r.mean(); usual[(c, h)] = r.std(ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for start in range(0, n, 3):
                cell = [i for i in range(start, min(start + 3, n)) if fc[i] <= -2]
                if not cell: continue
                i = cell[0]
                rec = {"coin": c, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                       "absf": -fc[i], "pos": i / n}
                # 3-day prior rise scaled
                if i >= 30:
                    dr = pd.Series(cl).pct_change().values
                    sd = np.nanstd(dr[i-29:i+1], ddof=1)
                    rec["rise3"] = cl[i] / cl[i-3] - 1 if i >= 3 else np.nan
                    rec["zrise"] = rec["rise3"] / sd
                for h in H:
                    if i + h < n:
                        tot = -(cl[i + h] / cl[i] - 1)
                        rec[f"tot{h}"] = tot
                        rec[f"unu{h}"] = tot + drift[(c, h)]
                        rec[f"str{h}"] = (tot + drift[(c, h)]) / usual[(c, h)]
                rows.append(rec)
    d = pd.DataFrame(rows)

    def clt(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return (len(s), np.nan, np.nan, np.nan)
        dev = s[col] - s[col].mean()
        g = dev.groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / len(s)
        return (len(s), G, s[col].mean(), s[col].mean() / se if se > 0 else np.nan)

    out = {}
    hz = []
    for h in H:
        n, G, m, t = clt(d, f"unu{h}")
        _, _, mt, tt = clt(d, f"tot{h}")
        hz.append({"h": h, "cases": n, "days": G, "unusual": m, "t": t, "total": mt, "t_tot": tt,
                   "strength": d[f"str{h}"].mean()})
    out["by_horizon"] = pd.DataFrame(hz)
    def grp(key):
        res = []
        for k, s in d.groupby(key):
            n, G, m, t = clt(s, "unu3")
            n5, G5, m5, t5 = clt(s, "unu5")
            res.append({key: k, "cases": n, "days": G, "unu3": m, "t3": t, "unu5": m5, "t5": t5})
        return pd.DataFrame(res)
    out["by_coin"] = grp("coin")
    out["by_window"] = grp("win")
    out["by_year"] = grp("year")
    d["fq"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["by_forecast_quartile"] = grp("fq")
    d["zq"] = pd.qcut(d["zrise"], 4, labels=False, duplicates="drop")
    out["by_zrise_quartile"] = grp("zq")
    out["zrise_q_bounds"] = d.groupby("zq")["zrise"].agg(["min", "max", "mean"])
    out["corr_absf_zrise"] = float(d[["absf", "zrise"]].corr().iloc[0, 1])
    s = d.dropna(subset=["unu3", "zrise"])
    out["slope_unu3_on_zrise"] = str(stats.linregress(s["zrise"], s["unu3"])[:4])
    out["share_negative_zrise"] = float((d["zrise"] <= 0).mean())
    return out
