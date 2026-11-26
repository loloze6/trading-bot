def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["cl"] = (c - b["low"]) / rng
            r1 = c.pct_change()
            b["gain"] = r1 / r1.abs().rolling(20, min_periods=20).mean()
            b["tr60"] = (c / c.shift(60) - 1) * 100
            for h in (2, 5, 10):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["pos"] = np.arange(len(b))
            b["cell"] = b["pos"] // H
            b["inprof"] = b["regime"].astype(str) != "chop"
            b["coin"] = coin; b["w"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","day","year","pos","cell","cl","gain","tr60","f2","f5","f10","inprof","regime","postRebalance_current_allocation"]])
    A = pd.concat(rows, ignore_index=True)
    # drift per coin on grid
    drift = {}; usual = {}
    for h in (2,5,10):
        g = A[A["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        usual[h] = g.groupby("coin")[f"f{h}"].std()
    def measure(mask, h=5, side=-1):
        S = A[mask & A[f"f{h}"].notna()].copy()
        S["cellh"] = S["pos"] // h
        S = S.sort_values("pos").groupby(["coin","w","cellh"]).head(1)
        if len(S) < 3: return pd.Series({"n": len(S)})
        un = side * (S[f"f{h}"] - S["coin"].map(drift[h]))
        tot = side * S[f"f{h}"]
        d = un - un.mean()
        ds = d.groupby(S["day"]).sum()
        D = len(ds)
        se = np.sqrt((ds**2).sum() * D/(D-1)) / len(S) if D > 1 else np.nan
        return pd.Series({"n": len(S), "days": D, "unusual": un.mean(), "total": tot.mean(),
                          "t": un.mean()/se if se else np.nan,
                          "strength": (un / S["coin"].map(usual[h])).mean()})
    hi = A["cl"] >= 0.8; up = A["gain"] > 0; small = A["gain"] < 1
    sig = hi & up & small
    ip = A["inprof"]
    chop_tr = A["tr60"].abs() <= 10
    res = {}
    tab = {}
    tab["sig_inprof"] = measure(sig & ip)
    tab["noSig_inprof"] = measure(~sig & ip)
    tab["sig_outprof_all"] = measure(sig & ~ip)
    tab["sig_out_choppyTrend(calm)"] = measure(sig & ~ip & chop_tr)
    tab["sig_out_trending"] = measure(sig & ~ip & A["tr60"].notna() & ~chop_tr)
    tab["sig_out_rising"] = measure(sig & ~ip & (A["tr60"] > 10))
    tab["sig_out_falling"] = measure(sig & ~ip & (A["tr60"] < -10))
    tab["hi_up_any_gain_inprof"] = measure(hi & up & ip)
    tab["hi_bigup_inprof"] = measure(hi & (A["gain"] >= 1) & ip)
    tab["cl>=0.6_up_small_inprof"] = measure((A["cl"] >= 0.6) & up & small & ip)
    tab["cl>=0.6_up_small_all"] = measure((A["cl"] >= 0.6) & up & small)
    tab["sig_all"] = measure(sig)
    tab["hi_any_inprof"] = measure(hi & ip)
    tab["sig_inprof_h2"] = measure(sig & ip, 2)
    tab["sig_inprof_h10"] = measure(sig & ip, 10)
    tab["sig_all_h10"] = measure(sig, 10)
    res["groups"] = pd.DataFrame(tab).T
    res["share_inprof_bars"] = float(ip.mean())
    res["share_sig_bars_all"] = float(sig.mean())
    # gain bins in profile, high close
    gb = pd.cut(A["gain"], [-10, 0, 0.33, 0.66, 1, 2, 10])
    res["gain_bins_hiclose_inprof"] = pd.DataFrame({str(k): measure(hi & ip & (gb == k)) for k in gb.cat.categories}).T
    res["gain_bins_hiclose_all"] = pd.DataFrame({str(k): measure(hi & (gb == k)) for k in gb.cat.categories}).T
    # book falls: per window book chain
    dd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    Dd = pd.concat(dd)
    br = Dd.groupby(["w","day"])["book_return"].mean().fillna(0)
    byw = br.groupby(level=0).agg(["sum","min","count"])
    eq = (1+br).cumprod(); mdd = (eq/eq.cummax()-1)
    res["book_by_window"] = byw
    res["book_maxdd"] = float(mdd.min())
    res["worst_book_days"] = br.sort_values().head(8).reset_index(drop=True)
    return res
