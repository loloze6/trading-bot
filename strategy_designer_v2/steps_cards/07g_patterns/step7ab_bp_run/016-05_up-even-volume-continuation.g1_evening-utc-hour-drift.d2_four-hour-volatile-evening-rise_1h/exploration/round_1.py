import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    hour_rows = []; cases = []; cases24 = []; wk = []
    for coin, wins in bars.items():
        # coin's normal drift / usual move on 72-bar and 24-bar grids
        g72 = []; g24 = []
        for w, df in wins.items():
            c = df["close"].values
            for H, g in ((72, g72), (24, g24)):
                idx = np.arange(0, len(c) - H, H)
                g.extend(list(c[idx + H] / c[idx] - 1))
        m72, s72 = np.mean(g72), np.std(g72)
        m24, s24 = np.mean(g24), np.std(g24)
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hr = pd.DataFrame({"h": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r})
            hr["coin"] = coin
            hour_rows.append(hr)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for H, L, m, s, store in ((72, 72, m72, s72, cases), (24, 72, m24, s24, cases24)):
                for t in range(L, len(c) - H, H):
                    seg = lr[t - L + 1:t + 1]; vs = v[t - L + 1:t + 1]
                    if np.isnan(seg).any(): continue
                    a = np.abs(seg); sa = a.sum()
                    if sa == 0 or vs.sum() == 0: continue
                    P = c[t] / c[t - L] - 1
                    eff = seg.sum() / sa
                    conc = np.sort(a)[-3:].sum() / sa
                    vconc = np.sort(vs)[-3:].sum() / vs.sum()
                    vol = np.std(seg)
                    F = c[t + H] / c[t] - 1
                    store.append((coin, w, P / s72, eff, conc, vconc, vol, (F - m) / s, F - m, F))
    H = pd.concat(hour_rows).dropna()
    hg = H.groupby("h")["r"].agg(["mean", "std", "count"])
    hg["t"] = hg["mean"] / (hg["std"] / np.sqrt(hg["count"]))
    out["hourly mean return by start hour (bps)"] = pd.DataFrame({"bps": hg["mean"] * 1e4, "t": hg["t"]}).round(2)
    wg = H.groupby("wd")["r"].agg(["mean", "std", "count"])
    out["hourly mean by weekday (bps/h)"] = pd.DataFrame({"bps": wg["mean"] * 1e4, "t": wg["mean"] / (wg["std"] / np.sqrt(wg["count"]))}).round(2)

    def analyse(cs, name):
        D = pd.DataFrame(cs, columns=["coin", "w", "Pz", "eff", "conc", "vconc", "vol", "Fz", "Fu", "F"])
        D["sgn"] = np.sign(D["Pz"])
        D["Fdir"] = D["Fz"] * D["sgn"]      # standardized unusual move in direction of past move
        D["Fudir"] = D["Fu"] * D["sgn"]
        res = {}
        D["Pq"] = D.groupby("coin")["Pz"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        res["by past-return quintile"] = D.groupby("Pq").agg(n=("Fz", "size"), Fz=("Fz", "mean"), Fu_bps=("Fu", lambda x: x.mean() * 1e4)).round(4)
        # among the larger moves (|Pz| top half per coin), path concentration thirds
        D["absq"] = D.groupby("coin")["Pz"].transform(lambda x: x.abs().rank(pct=True))
        big = D[D["absq"] > 0.5].copy()
        for col in ["conc", "vconc", "eff"]:
            big[col + "_t"] = big.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        tbl = []
        for col in ["conc", "vconc"]:
            g = big.groupby(col + "_t")["Fdir"]
            lo, hi = big.loc[big[col + "_t"] == 0, "Fdir"], big.loc[big[col + "_t"] == 2, "Fdir"]
            tt = stats.ttest_ind(hi, lo, equal_var=False)
            tbl.append({"split": col, "low3_Fdir": lo.mean(), "mid": g.mean().get(1), "high3_Fdir": hi.mean(),
                        "hi_minus_lo": hi.mean() - lo.mean(), "welch_t": tt.statistic, "n_each": len(lo),
                        "low3_bps": big.loc[big[col+"_t"]==0,"Fudir"].mean()*1e4, "high3_bps": big.loc[big[col+"_t"]==2,"Fudir"].mean()*1e4})
        res["big moves: future in move dir by concentration third"] = pd.DataFrame(tbl).round(4)
        # up vs down separately for concentration
        tb2 = []
        for sg in [1, -1]:
            b = big[big["sgn"] == sg]
            for k in range(3):
                x = b.loc[b["conc_t"] == k, "Fz"]
                tb2.append({"side": sg, "conc_third": k, "n": len(x), "Fz": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "bps": b.loc[b["conc_t"]==k,"Fu"].mean()*1e4})
        res["big moves by side and conc third (raw Fz)"] = pd.DataFrame(tb2).round(3)
        # volatility level thirds -> raw future
        D["volt"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        res["by past vol third: future total"] = D.groupby("volt").agg(n=("F", "size"), F_bps=("F", lambda x: x.mean() * 1e4), Fz=("Fz", "mean")).round(3)
        # by year stability of the concentration effect
        res = {name + ": " + k: v for k, v in res.items()}
        return res
    out.update(analyse(cases, "72h past -> next 72h"))
    out.update(analyse(cases24, "72h past -> next 24h"))
    # book
    bd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["w"] = w; bd.append(x)
    B = pd.concat(bd).dropna(subset=["book_return"])
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book daily mean by weekday (bps)"] = B.groupby("wd")[["book_return", "coin_return"]].mean().mul(1e4).round(2)
    return out
