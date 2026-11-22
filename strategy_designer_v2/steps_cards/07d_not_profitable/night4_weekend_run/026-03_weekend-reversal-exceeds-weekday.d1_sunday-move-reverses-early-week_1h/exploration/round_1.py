def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(b)
            for i in np.where((ts.dt.weekday == 6) & (ts.dt.hour == 23))[0]:
                if i - 24 < 0 or i + 48 >= n: continue
                f = b["forecast"].iloc[i]
                if not np.isfinite(f) or f == 0: continue
                r24 = c[i] / c[i-24] - 1
                r48p = c[i-24] / c[i-72] - 1 if i - 72 >= 0 else np.nan
                r7d = c[i] / c[i-168] - 1 if i - 168 >= 0 else np.nan
                r30d = c[i] / c[i-720] - 1 if i - 720 >= 0 else np.nan
                fwd = c[i+48] / c[i] - 1
                fwd24 = c[i+24] / c[i] - 1
                vol = np.nanstd(np.diff(np.log(c[max(0,i-720):i+1])))
                al = b["postRebalance_current_allocation"].iloc[i]
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, f=f, r24=r24, sat=r48p,
                                 r7d=r7d, r30d=r30d, fwd=fwd, fwd24=fwd24, vol=vol, al=al,
                                 gain=np.sign(f) * fwd))
    d = pd.DataFrame(rows)
    out["n_cases"] = len(d)
    out["mean_alloc_abs"] = float(d["al"].abs().mean())
    d["fq"] = pd.qcut(d["f"].abs(), 5, labels=False)
    out["by_absforecast_q"] = d.groupby("fq").agg(n=("gain","size"), gain=("gain","mean"),
        r24abs=("r24", lambda x: x.abs().mean()), alabs=("al", lambda x: x.abs().mean()))
    out["by_side"] = d.groupby(np.sign(d["f"])).agg(n=("gain","size"), gain=("gain","mean"), fwd=("fwd","mean"))
    d["sameside7d"] = np.sign(d["r7d"]) == np.sign(d["r24"])
    out["by_7d_agree"] = d.groupby("sameside7d").agg(n=("gain","size"), gain=("gain","mean"),
        t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    d["sameside30d"] = np.sign(d["r30d"]) == np.sign(d["r24"])
    out["by_30d_agree"] = d.groupby("sameside30d").agg(n=("gain","size"), gain=("gain","mean"),
        t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    d["satagree"] = np.sign(d["sat"]) == np.sign(d["r24"])
    out["by_sat_agree"] = d.groupby("satagree").agg(n=("gain","size"), gain=("gain","mean"),
        t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    d["volq"] = pd.qcut(d["vol"], 4, labels=False)
    out["by_volq"] = d.groupby("volq").agg(n=("gain","size"), gain=("gain","mean"),
        t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    d["g24"] = np.sign(d["f"]) * d["fwd24"]
    out["first24_vs_48"] = pd.Series({"gain24": d["g24"].mean(), "gain48": d["gain"].mean()})
    out["by_coin"] = d.groupby("coin").agg(n=("gain","size"), gain=("gain","mean"))
    out["by_year"] = d.groupby("year").agg(n=("gain","size"), gain=("gain","mean"))
    # book daily
    days = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=coin
            days.append(x)
    D = pd.concat(days).dropna()
    B = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_by_window"] = B.groupby("w").agg(book=("book_return","mean"), hold=("coin_return","mean"),
        bsd=("book_return","std"))
    out["book_by_weekday"] = B.assign(wd=pd.to_datetime(B["day"]).dt.weekday).groupby("wd")["book_return"].agg(["mean","std","count"])
    return out
