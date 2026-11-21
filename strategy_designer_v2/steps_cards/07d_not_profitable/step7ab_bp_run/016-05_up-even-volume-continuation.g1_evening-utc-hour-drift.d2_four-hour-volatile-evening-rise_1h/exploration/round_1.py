import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    # 1 trades
    rows = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            rows.append(pd.DataFrame({"coin": c, "gross": t["profit_loss_percent"], "net": t["net_profit_loss_percent"],
                                      "dur": t["duration_minutes"]}))
    tr = pd.concat(rows)
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("gross","size"), gross_mean=("gross","mean"),
                                                 net_mean=("net","mean"), dur_h=("dur", lambda x: x.mean()/60))
    # 2 evening cases, longer horizons, vol
    ev = []; hod = []; gj = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values.astype(float)
            n = len(b)
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            vol = pd.Series(r1).rolling(168, min_periods=100).std().values
            hr = ts.dt.hour.values
            def fwd(h):
                f = np.full(n, np.nan)
                f[:n-h] = cl[h:]/cl[:-h]-1
                return f
            f4, f24, f72 = fwd(4), fwd(24), fwd(72)
            idx = np.where(hr == 20)[0]
            ev.append(pd.DataFrame({"coin": c, "w": w, "k": np.arange(len(idx)), "vol": vol[idx],
                                    "f4": f4[idx], "f24": f24[idx], "f72": f72[idx]}))
            hod.append(pd.DataFrame({"coin": c, "hr": hr, "f4": f4, "vol": vol}))
            # grind vs jump at 72h, grid of 72 bars from window start
            ab = np.abs(r1)
            s = pd.Series(ab).rolling(72).sum().values
            mx = pd.Series(ab).rolling(72).max().values
            vv = pd.Series(b["volume"].astype(float)).rolling(72)
            vshare = (vv.max()/vv.sum()).values
            past = np.full(n, np.nan); past[72:] = cl[72:]/cl[:-72]-1
            g = np.arange(72, n-72, 72)
            gj.append(pd.DataFrame({"coin": c, "past": past[g], "jump": mx[g]/s[g], "vjump": vshare[g],
                                    "eff": np.abs(past[g])/s[g], "f72": f72[g]}))
    ev = pd.concat(ev); hod = pd.concat(hod); gj = pd.concat(gj)
    # drifts per coin
    res = {}
    for col in ["f4", "f24", "f72"]:
        d = ev.groupby("coin")[col].transform("mean")  # rough baseline
    hd = hod.groupby("coin")["f4"].mean()
    ev["u4"] = ev["f4"] - ev["coin"].map(hd)
    ev["volq"] = ev.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    sub72 = ev[ev["k"] % 3 == 0]
    out["evening_by_volq"] = ev.groupby("volq").agg(n=("f4","size"), f4_bps=("f4", lambda x: x.mean()*1e4),
        u4_bps=("u4", lambda x: x.mean()*1e4), f24_bps=("f24", lambda x: x.mean()*1e4),
        vol_h_bps=("vol", lambda x: x.mean()*1e4))
    out["evening_f72_by_volq"] = sub72.groupby("volq").agg(n=("f72","size"), f72_bps=("f72", lambda x: x.mean()*1e4),
        t=("f72", lambda x: x.mean()/(x.std()/np.sqrt(x.notna().sum()))))
    out["evening_by_coin"] = ev.groupby("coin").agg(f4_bps=("f4", lambda x: x.mean()*1e4), drift4_bps=("coin", lambda x: hd[x.iloc[0]]*1e4))
    out["hod_4h_bps"] = (hod.groupby("hr")["f4"].mean()*1e4).round(2)
    # grind vs jump
    gj = gj.dropna()
    dr72 = gj.groupby("coin")["f72"].transform("mean")
    gj["dirfwd"] = np.sign(gj["past"])*(gj["f72"]-dr72)
    gj["absq"] = gj.groupby("coin")["past"].transform(lambda x: pd.qcut(x.abs().rank(method="first"), 3, labels=False))
    gj["jq"] = gj.groupby("coin")["jump"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    gj["vq"] = gj.groupby("coin")["vjump"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    gj["eq"] = gj.groupby("coin")["eff"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    f = lambda x: x.mean()*1e4
    tt = lambda x: x.mean()/(x.std()/np.sqrt(len(x)))
    out["gj_by_absq_jq_bps"] = gj.pivot_table(index="absq", columns="jq", values="dirfwd", aggfunc=f)
    out["gj_by_jq"] = gj.groupby("jq")["dirfwd"].agg(["size", f, tt])
    out["gj_by_vq"] = gj.groupby("vq")["dirfwd"].agg(["size", f, tt])
    out["gj_by_eff"] = gj.groupby("eq")["dirfwd"].agg(["size", f, tt])
    out["gj_by_eff_up_down"] = gj.assign(up=gj["past"]>0).pivot_table(index="eq", columns="up", values="dirfwd", aggfunc=f)
    return out
