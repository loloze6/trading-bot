import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = d["ts"].dt.hour
            d["year"] = d["ts"].dt.year
            d["coin"] = coin; d["win"] = w
            d["wn"] = int(w[1:])
            d["pos"] = np.arange(len(d))
            c = d["close"]
            r1 = c.pct_change()
            d["vol24"] = r1.rolling(24).std()
            d["vol720"] = r1.rolling(720, min_periods=240).std()
            d["past24"] = c / c.shift(24) - 1
            d["past72"] = c / c.shift(72) - 1
            for h in [1,24,72]:
                d[f"fwd{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in [1,24,72]:
        A[f"x{h}"] = A[f"fwd{h}"] - A.groupby("coin")[f"fwd{h}"].transform("mean")
    out = {}
    def tt(g, zc="z", col="x24"):
        g = g.dropna(subset=[zc, col]); g = g[np.isfinite(g[zc])]
        if len(g) < 30: return pd.Series({"n": len(g), "slope_bp": np.nan, "t": np.nan})
        sl, ic, rr, p, se = stats.linregress(g[zc], g[col]); return pd.Series({"n":len(g),"slope_bp":sl*1e4,"t":sl/se})
    # 24->24 on grid, vol tercile per coin, and vol relative to own 30d vol
    s = A[A["pos"] % 24 == 0].copy()
    s["z"] = s["past24"]/(s["vol24"]*np.sqrt(24))
    s = s.dropna(subset=["z","x24","vol24"])
    s["vt"] = s.groupby("coin")["vol24"].transform(lambda v: pd.qcut(v, 3, labels=False))
    s["vratio"] = s["vol24"]/s["vol720"]
    s["vrt"] = pd.qcut(s["vratio"], 3, labels=False)
    out["24to24_by_vol_vs_own30d_tercile"] = s.groupby("vrt").apply(tt).round(3)
    hv = s[s["vt"] == 2]
    out["24to24_highvol_by_year"] = hv.groupby("year").apply(tt).round(3)
    out["24to24_highvol_by_coin"] = hv.groupby("coin").apply(tt).round(3)
    hv = hv.copy(); hv["half"] = np.where(hv["wn"] <= 12, "w1-w12", "w13-w24")
    out["24to24_highvol_by_halves"] = hv.groupby("half").apply(tt).round(3)
    # size in high vol: reversal move by |z| quintile
    hv["zq"] = pd.qcut(hv["z"].abs(), 5, labels=False)
    rev_tot = -np.sign(hv["z"]) * hv["fwd24"]; rev_x = -np.sign(hv["z"]) * hv["x24"]
    hv["rt"] = rev_tot; hv["rx"] = rev_x
    g = hv.groupby("zq")
    out["24to24_highvol_reversal_by_absz_quintile"] = pd.DataFrame({
        "n": g.size(), "mean_absz": g["z"].apply(lambda v: v.abs().mean()),
        "total_rev_bp": g["rt"].mean()*1e4, "unusual_rev_bp": g["rx"].mean()*1e4,
        "t": g["rx"].mean()/(g["rx"].std()/np.sqrt(g.size())),
        "usual_move_bp": g["fwd24"].std()*1e4}).round(3)
    # same with 72h horizon, high vol, grid 72
    s7 = A[A["pos"] % 72 == 0].copy()
    s7["z"] = s7["past24"]/(s7["vol24"]*np.sqrt(24))
    s7 = s7.dropna(subset=["z","x72","vol24"])
    s7["vt"] = s7.groupby("coin")["vol24"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["24to72_by_voltercile"] = s7.groupby("vt").apply(lambda g: tt(g, col="x72")).round(3)
    # hour-of-day next1h by year halves for hours 13, 20, 21, 2
    A["half"] = np.where(A["wn"] <= 12, "w1-w12", "w13-w24")
    sub = A[A["hour"].isin([1,2,13,14,20,21])].dropna(subset=["x1"])
    g = sub.groupby(["hour","half"])["x1"]
    out["next1h_selected_hours_by_half"] = pd.DataFrame({"mean_bp": g.mean()*1e4,
        "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # trend-signed (24h) next1h by hour of day, by half
    A["sx1"] = A["x1"] * np.sign(A["past24"])
    g = A.dropna(subset=["sx1"]).groupby(["hour"])["sx1"]
    t_all = g.mean()/(g.std()/np.sqrt(g.count()))
    g1 = A[A["half"]=="w1-w12"].dropna(subset=["sx1"]).groupby("hour")["sx1"]
    g2 = A[A["half"]=="w13-w24"].dropna(subset=["sx1"]).groupby("hour")["sx1"]
    out["trend_signed_next1h_by_hour"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": t_all,
        "t_w1_12": g1.mean()/(g1.std()/np.sqrt(g1.count())),
        "t_w13_24": g2.mean()/(g2.std()/np.sqrt(g2.count()))}).round(3)
    return out
