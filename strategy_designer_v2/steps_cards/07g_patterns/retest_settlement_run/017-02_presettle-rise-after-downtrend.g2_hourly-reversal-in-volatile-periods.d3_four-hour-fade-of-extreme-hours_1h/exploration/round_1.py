def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp","close","volume","forecast"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["coin"] = coin; d["w"] = w
            d["pos"] = np.arange(len(d))
            c = d["close"]
            d["r1"] = c.pct_change()
            for h in [4,12,24,72,168]:
                d[f"f{h}"] = c.shift(-h)/c - 1
            for h in [24,72,168]:
                d[f"p{h}"] = c/c.shift(h) - 1
            d["vol24"] = d["r1"].rolling(24).std()
            d["vol720"] = d["r1"].rolling(720, min_periods=240).std()
            d["vratio"] = d["vol24"]/d["vol720"]
            d["z1"] = d["r1"]/d["vol720"]
            d["hour"] = d["ts"].dt.hour; d["wd"] = d["ts"].dt.weekday
            d["lv"] = np.log(d["volume"].replace(0,np.nan))
            d["lv_rel"] = d["lv"] - d["lv"].rolling(168, min_periods=48).mean()
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # 1. hour of day returns (bar start hour), pooled
    g = A.dropna(subset=["r1"]).groupby("hour")["r1"]
    hr = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    hr["vol_rel"] = A.groupby("hour")["lv_rel"].mean()
    hr["absr_bp"] = A.groupby("hour")["r1"].apply(lambda s: s.abs().mean()*1e4)
    out["by_hour"] = hr.round(3)
    # 2. reversal / continuation over horizons: signed by -sign(z1), graded slope on z1*vratio
    res = []
    for sit in ["z1","p24","p72","p168"]:
        for h in [4,12,24,72,168]:
            s = A[A["pos"] % h == 0].copy()
            mu = s.groupby("coin")[f"f{h}"].transform("mean")
            s["ex"] = s[f"f{h}"] - mu
            x = s[sit] if sit!="z1" else s["z1"]*s["vratio"]
            s["x"] = x
            s = s.dropna(subset=["x","ex"])
            s["xz"] = s.groupby("coin")["x"].transform(lambda v:(v-v.mean())/v.std())
            lr = stats.linregress(s["xz"], s["ex"])
            q = s["xz"].abs() >= s["xz"].abs().quantile(0.9)
            top = (np.sign(s.loc[q,"xz"])*s.loc[q,"ex"])
            res.append({"sit":sit,"h":h,"n":len(s),"slope_bp_per_sd":lr.slope*1e4,
                        "t":lr.slope/lr.stderr,"top10_signed_bp":top.mean()*1e4,
                        "top10_t":top.mean()/(top.std()/np.sqrt(len(top)))})
    out["horizon_grid"] = pd.DataFrame(res).round(3)
    # 3. brief: pre-settlement hours (start 7,15,23) return x sign(prior 24h), vs other hours
    B = A.dropna(subset=["r1","p24"]).copy()
    B["p24_prev"] = B.groupby(["coin","w"])["p24"].shift(1)
    B = B.dropna(subset=["p24_prev"])
    B["sr"] = B["r1"]*np.sign(B["p24_prev"])
    g = B.groupby("hour")["sr"]
    out["trend_signed_r_by_hour"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))}).round(3)
    # 4. weekday
    g = A.dropna(subset=["r1"]).groupby("wd")["r1"]
    out["by_weekday"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))}).round(3)
    # 5. book: per-coin per-window sharpe sign
    dd=[]
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            dd.append({"coin":coin,"w":w,"br":df["book_return"].mean(),"cr":df["coin_return"].mean()})
    dd=pd.DataFrame(dd)
    out["book_by_coin_bp"] = (dd.groupby("coin")[["br","cr"]].mean()*1e4).round(2)
    return out
