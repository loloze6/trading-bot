import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]; r1 = c.pct_change()
            std30 = r1.rolling(30).std()
            rng = (d["high"] - d["low"])
            width = rng / c / std30
            loc = (d["high"] - c) / rng.replace(0, np.nan)
            z = r1 / std30.shift(1)
            tr60 = c / c.shift(60) - 1
            out = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(d)),
                                "ts": pd.to_datetime(d["timestamp"]),
                                "width": width, "loc": loc, "z": z, "tr60": tr60,
                                "inprof": d["regime"] != "chop", "regime": d["regime"],
                                "std30": std30})
            for h in (1, 3, 5):
                out[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    # normal drift per coin per h on grid
    drift = {}
    for h in (1, 3, 5):
        g = A[A["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(drift[h])
    def summ(mask, h):
        s = A[mask & (A["pos"] % h == 0)][f"u{h}"].dropna()
        n = len(s)
        if n < 3: return (n, np.nan, np.nan)
        return (n, s.mean(), s.mean() / (s.std() / np.sqrt(n)))
    wide = A["width"] >= 2
    lowc = A["loc"] >= 0.75; highc = A["loc"] <= 0.25
    up = A["tr60"] > 0.10; dn = A["tr60"] < -0.10; ch = A["tr60"].between(-0.10, 0.10)
    cats = {
        "all": A["width"].notna(),
        "wideLow_inprof": wide & lowc & A["inprof"],
        "wideLow_outprof": wide & lowc & ~A["inprof"],
        "wideLow_out_up": wide & lowc & ~A["inprof"] & up,
        "wideLow_out_chop": wide & lowc & ~A["inprof"] & ch,
        "wideLow_out_down": wide & lowc & ~A["inprof"] & dn,
        "wideHigh_inprof": wide & highc & A["inprof"],
        "wideHigh_outprof": wide & highc & ~A["inprof"],
        "wideHigh_up": wide & highc & up,
        "wideHigh_down": wide & highc & dn,
        "wideHigh_chop": wide & highc & ch,
        "wideLow_up": wide & lowc & up,
        "wideLow_down": wide & lowc & dn,
        "wideLow_chop": wide & lowc & ch,
    }
    ev = []
    for k, m in cats.items():
        rec = {"cat": k}
        for h in (1, 3, 5):
            n, mu, t = summ(m, h)
            rec[f"n{h}"] = n; rec[f"u{h}"] = mu; rec[f"t{h}"] = t
        ev.append(rec)
    ev = pd.DataFrame(ev).set_index("cat").round(4)
    # big moves by z
    A["zb"] = pd.cut(A["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    zt = []
    for b, g in A.groupby("zb", observed=True):
        rec = {"zbin": str(b)}
        for h in (1, 3):
            s = g[g["pos"] % h == 0][f"u{h}"].dropna()
            rec[f"n{h}"] = len(s); rec[f"u{h}"] = s.mean(); rec[f"t{h}"] = s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        zt.append(rec)
    zt = pd.DataFrame(zt).set_index("zbin").round(4)
    # width tercile all days, by close location tercile, next 1 and 3 day
    A["wb"] = pd.qcut(A["width"], 4, labels=["w_q1","w_q2","w_q3","w_q4"])
    A["lb"] = pd.cut(A["loc"], [-0.01, 0.25, 0.75, 1.01], labels=["nearHigh","mid","nearLow"])
    g3 = A[A["pos"] % 3 == 0].dropna(subset=["u3"])
    grid = g3.groupby(["wb","lb"], observed=True)["u3"].agg(["count","mean","std"])
    grid["t"] = grid["mean"]/(grid["std"]/np.sqrt(grid["count"]))
    grid = grid.drop(columns="std").round(4)
    # weekday, next day
    A["wd"] = A["ts"].dt.dayofweek
    wdt = A.dropna(subset=["u1"]).groupby("wd")["u1"].agg(["count","mean","std"])
    wdt["t"] = wdt["mean"]/(wdt["std"]/np.sqrt(wdt["count"])); wdt = wdt.drop(columns="std").round(5)
    # vol level: std30 tercile per coin, next 3d unusual
    A["vq"] = A.groupby("coin")["std30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    vt = g3.assign(vq=A.loc[g3.index,"vq"]).groupby(["vq"])["u3"].agg(["count","mean","std"])
    vt["t"] = vt["mean"]/(vt["std"]/np.sqrt(vt["count"])); vt = vt.drop(columns="std").round(4)
    # trades
    T = []
    for coin, wins in trades.items():
        for w, t in wins.items():
            if t is None or len(t)==0: continue
            tt = t.copy(); tt["coin"]=coin; tt["win"]=w; T.append(tt)
    T = pd.concat(T, ignore_index=True)
    T["fb"] = pd.qcut(T["entry_forecast"], 3, duplicates="drop")
    tf = T.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    tc = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    ty = T.groupby("yr")["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    return {"events_unusual": ev, "after_z_moves": zt, "width_x_loc_u3": grid,
            "weekday_u1": wdt, "vol_tercile_u3": vt, "trades_by_forecast": tf,
            "trades_by_coin": tc, "trades_by_year": ty,
            "n_bars": len(A), "share_inprof": float(A["inprof"].mean())}
