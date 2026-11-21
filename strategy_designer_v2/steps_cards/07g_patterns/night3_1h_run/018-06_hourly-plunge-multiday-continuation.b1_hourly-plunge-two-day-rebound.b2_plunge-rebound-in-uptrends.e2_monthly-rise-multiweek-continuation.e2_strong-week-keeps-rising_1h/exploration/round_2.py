import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    out = {}
    def build(H, k, volwin=720):
        rows = []
        for c, ws in bars.items():
            rets = []; per = {}
            for w, df in ws.items():
                cl = df["close"].astype(float).reset_index(drop=True)
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                past = cl / cl.shift(k) - 1
                lr = np.log(cl).diff()
                sdk = lr.rolling(volwin, min_periods=168).std() * np.sqrt(k)
                z = np.log(cl / cl.shift(k)) / sdk
                vol7 = lr.rolling(168).std()
                idx = np.arange(0, len(cl) - H, H)
                r = cl.values[idx + H] / cl.values[idx] - 1
                rets.extend(r.tolist())
                per[w] = (r, past.values[idx], z.values[idx], vol7.values[idx], ts.dt.year.values[idx])
            mu, sd = np.mean(rets), np.std(rets)
            for w, (r, p, z, v, y) in per.items():
                for a, b, zz, vv, yy in zip(r, p, z, v, y):
                    rows.append((c, w, yy, a - mu, (a - mu) / sd, a, b, zz, vv))
        d = pd.DataFrame(rows, columns=["coin", "w", "yr", "unus", "str", "tot", "past", "z", "vol"]).dropna()
        return d
    def tab(d, by):
        g = d.groupby(by).agg(n=("str", "size"), unus=("unus", "mean"), tot=("tot", "mean"), strength=("str", "mean"), sd=("str", "std"))
        g["t"] = g["strength"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd")
    for H in [24, 48, 72]:
        d = build(H, 24)
        d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
        out[f"fwd{H}h_by_z1d_decile"] = tab(d, "zq")
        if H == 24:
            low = d[d["zq"] <= 1]
            out["fwd24h_low2dec_by_coin"] = tab(low, "coin")
            out["fwd24h_low2dec_by_year"] = tab(low, "yr")
            low = low.copy()
            low["vq"] = low.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
            out["fwd24h_low2dec_by_vol_tercile"] = tab(low, "vq")
            out["slope_str_on_z_neg_side"] = float(np.polyfit(d.loc[d.z < 0, "z"], d.loc[d.z < 0, "str"], 1)[0])
            out["slope_str_on_z_pos_side"] = float(np.polyfit(d.loc[d.z > 0, "z"], d.loc[d.z > 0, "str"], 1)[0])
            hi = d[d["zq"] >= 8]
            out["fwd24h_top2dec_by_year"] = tab(hi, "yr")
            # fraction of windows with positive mean in low deciles
            wm = low.groupby(["coin", "w"])["str"].mean()
            out["low2dec_share_coinwindows_positive"] = float((wm > 0).mean())
    # hour 20-21 by year
    hr = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"]); cl = df["close"].astype(float)
            r = cl.shift(-1) / cl - 1
            hr.append(pd.DataFrame({"h": ts.dt.hour.values, "yr": ts.dt.year.values, "r": r.values, "z": (r / r.std()).values}))
    hr = pd.concat(hr).dropna()
    e = hr[hr.h.isin([20, 21])]
    g = e.groupby("yr")["z"].agg(["mean", "std", "size"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    g["mean_ret_bps"] = e.groupby("yr")["r"].mean() * 1e4
    out["hours20_21_by_year"] = g
    return out
