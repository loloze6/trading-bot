def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    ev = []
    wk = []
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            a = df["close"].values[::48]
            g48.extend(list(a[1:] / a[:-1] - 1))
        sd48 = np.nanstd(g48); mu48 = np.nanmean(g48)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            hr = ts.dt.hour.values; tsv = ts.values.astype("datetime64[h]").astype(np.int64)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            n = len(c)
            for t in np.where(hr == 21)[0]:
                if t - 168 < 0 or t + 1 >= n: continue
                if tsv[t + 1] - tsv[t - 168] != 169: continue
                evr = c[t + 1] / c[t - 1] - 1
                rv = np.nanstd(r1[t - 167:t - 1])
                vr = v[t - 21:t - 1].mean() / max(v[t - 168:t - 21].mean(), 1e-12)
                # control: same 2h earlier (bars 17,18)
                ctl = c[t - 3] / c[t - 5] - 1
                ev.append((coin, w, ts.iloc[t].year, evr, evr / (rv * np.sqrt(2)), vr, ctl / (rv * np.sqrt(2))))
            for t in np.where(hr == 23)[0]:
                if ts.iloc[t].weekday() != 6: continue
                if t - 168 < 0 or t + 48 >= n: continue
                if tsv[t + 48] - tsv[t - 168] != 216: continue
                past = (c[t] / c[t - 48] - 1) / sd48
                vr = v[t - 47:t + 1].mean() / max(v[t - 167:t - 47].mean(), 1e-12)
                f24 = (c[t + 24] / c[t] - 1 - mu48 / 2) / sd48
                f48 = (c[t + 48] / c[t] - 1 - mu48) / sd48
                wk.append((coin, w, ts.iloc[t].year, past, vr, f24, f48))
    E = pd.DataFrame(ev, columns=["coin", "win", "yr", "r", "z", "vr", "ctl"])
    E["lvr"] = np.log(E.vr)
    s = stats.linregress(E.lvr, E.z)
    out["evening z on log day-vol-ratio: slope,t,n"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}, {len(E)}"
    s = stats.linregress(E.lvr, E.ctl)
    out["control 17-19h z on log vr: slope,t"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}"
    rows = []
    for coin, d in E.groupby("coin"):
        s = stats.linregress(d.lvr, d.z)
        rows.append({"coin": coin, "slope": s.slope, "t": s.slope / s.stderr, "n": len(d)})
    out["evening z on log vr by coin"] = pd.DataFrame(rows)
    wm = E.groupby("win").r.mean()
    out["evening: windows with mean>0 / total"] = f"{(wm>0).sum()} / {len(wm)}"
    W = pd.DataFrame(wk, columns=["coin", "win", "yr", "pz", "vr", "f24", "f48"])
    W["x"] = W.pz / W.vr
    for y in ["f24", "f48"]:
        s = stats.linregress(W.x, W[y]); out[f"Sunday {y} on pz/vr: slope,t,n"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}, {len(W)}"
    W["half"] = np.where(W.yr <= 2021, "2018-21", "2022-25")
    rows = []
    for h, d in W.groupby("half"):
        s = stats.linregress(d.x, d.f48); rows.append({"half": h, "slope": s.slope, "t": s.slope / s.stderr, "n": len(d)})
    out["Sunday f48 on pz/vr by half"] = pd.DataFrame(rows)
    rows = []
    for coin, d in W.groupby("coin"):
        s = stats.linregress(d.x, d.f48); rows.append({"coin": coin, "slope": s.slope, "t": s.slope / s.stderr})
    out["Sunday f48 on pz/vr by coin"] = pd.DataFrame(rows)
    return out
