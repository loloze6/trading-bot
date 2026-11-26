def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
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
            for h in (3, 5, 7, 10, 15):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["pos"] = np.arange(len(b))
            b["inprof"] = b["regime"].astype(str) != "chop"
            b["coin"] = coin; b["w"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(b[["coin","w","day","year","pos","cl","gain","tr60","f3","f5","f7","f10","f15","inprof","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    drift = {}; usual = {}
    for h in (3,5,7,10,15):
        g = A[A["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        usual[h] = g.groupby("coin")[f"f{h}"].std()
    def sel(mask, h):
        S = A[mask & A[f"f{h}"].notna()].copy()
        S["cellh"] = S["pos"] // h
        return S.sort_values("pos").groupby(["coin","w","cellh"]).head(1)
    def measure(mask, h=5, side=-1):
        S = sel(mask, h)
        if len(S) < 3: return pd.Series({"n": len(S)})
        un = side * (S[f"f{h}"] - S["coin"].map(drift[h]))
        tot = side * S[f"f{h}"]
        d = un - un.mean()
        ds = d.groupby(S["day"]).sum(); D = len(ds)
        se = np.sqrt((ds**2).sum() * D/(D-1)) / len(S) if D > 1 else np.nan
        return pd.Series({"n": len(S), "days": D, "unusual": un.mean(), "total": tot.mean(),
                          "t": un.mean()/se, "strength": (un / S["coin"].map(usual[h])).mean(),
                          "hit": (tot > 0).mean()})
    ip = A["inprof"]; up = A["gain"] > 0; small = A["gain"] < 1
    tab = {}
    for h in (3,5,7,10,15):
        tab[f"sig_inprof_h{h}"] = measure((A["cl"]>=0.8)&up&small&ip, h)
        tab[f"cl60_up_small_inprof_h{h}"] = measure((A["cl"]>=0.6)&up&small&ip, h)
        tab[f"noSig_inprof_h{h}"] = measure(~((A["cl"]>=0.6)&up&small)&ip, h)
        tab[f"cl60_up_small_choppycalm_h{h}"] = measure((A["cl"]>=0.6)&up&small&~ip&(A["tr60"].abs()<=10), h)
    tab["cl60_up_small_choppy_any_h10"] = measure((A["cl"]>=0.6)&up&small&(A["tr60"].abs()<=10), 10)
    tab["cl50_up_small_inprof_h10"] = measure((A["cl"]>=0.5)&up&small&ip, 10)
    res = {"groups": pd.DataFrame(tab).T}
    # close-location bins in profile, up small days, h10
    cb = pd.cut(A["cl"], [0,0.4,0.6,0.8,1.0001])
    res["cl_bins_upsmall_inprof_h10"] = pd.DataFrame({str(k): measure(up&small&ip&(cb==k),10) for k in cb.cat.categories}).T
    gb = pd.cut(A["gain"], [0,0.33,0.66,1])
    res["gain_bins_cl60_inprof_h10"] = pd.DataFrame({str(k): measure((A["cl"]>=0.6)&ip&(gb==k),10) for k in gb.cat.categories}).T
    # by year, h10 broad
    S = sel((A["cl"]>=0.6)&up&small&ip, 10)
    un = -(S["f10"] - S["coin"].map(drift[10]))
    res["by_year_cl60_h10"] = un.groupby(S["year"]).agg(["count","mean"])
    res["by_coin_cl60_h10"] = un.groupby(S["coin"]).agg(["count","mean"])
    # book's position: what in profile days held short and their outcome
    res["share_bars_short"] = float((A["alloc"] < 0).mean())
    res["mean_abs_alloc_when_short"] = float(A.loc[A["alloc"]<0,"alloc"].abs().mean())
    return res
