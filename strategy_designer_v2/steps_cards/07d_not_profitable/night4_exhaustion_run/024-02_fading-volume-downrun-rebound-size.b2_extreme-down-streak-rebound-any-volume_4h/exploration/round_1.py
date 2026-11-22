import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 18
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily, chained in window order
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    chain = []; perwin = []
    for w in wins:
        frames = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return", "coin_return"]].mean().dropna()
        g["w"] = w
        chain.append(g)
    ch = pd.concat(chain)
    v = (1 + ch["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    ch["dd"] = dd.values
    yrs = len(ch) / 365
    out["book summary"] = pd.Series({"mean": ch.book_return.mean(), "sd": ch.book_return.std(),
        "yearly": v.iloc[-1] ** (1 / yrs) - 1, "maxdd": dd.min(), "hold_mean": ch.coin_return.mean(),
        "corr_book_coin": ch.book_return.corr(ch.coin_return), "days": len(ch)})
    pw = ch.groupby("w").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                            coin=("coin_return", lambda x: (1 + x).prod() - 1),
                            worst_dd=("dd", "min"))
    out["per window"] = pw
    # ---- bar-level: per coin features and cases
    rows = []; barrows = []
    for c in bars:
        drift_list = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            drift_list += list(cl[idx + H] / cl[idx] - 1)
        drift = np.mean(drift_list); usual = np.std(drift_list)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            ret30 = cl / cl.shift(180) - 1
            ret7 = cl / cl.shift(42) - 1
            ret3 = cl / cl.shift(18) - 1
            vol30 = r.rolling(180).std(); vol5 = r.rolling(30).std()
            fwd = cl.shift(-H) / cl - 1
            f = b["forecast"].fillna(0)
            alloc = b["postRebalance_current_allocation"].fillna(0)
            gain = alloc * (cl.shift(-1) / cl - 1)
            # case: forecast rise >=2 vs previous bar, first per cell
            rise = (f - f.shift(1)) >= 2
            cell = np.arange(len(b)) // H
            dfc = pd.DataFrame({"rise": rise, "cell": cell, "fwd": fwd, "f": f, "ret30": ret30,
                                "ret7": ret7, "ret3": ret3, "vr": vol5 / vol30})
            cs = dfc[dfc.rise].groupby("cell").head(1).dropna(subset=["fwd"])
            cs = cs.assign(coin=c, w=w, unusual=cs.fwd - drift, strength=(cs.fwd - drift) / usual)
            rows.append(cs)
            barrows.append(pd.DataFrame({"coin": c, "w": w, "alloc": alloc, "gain": gain,
                                         "ret30": ret30, "ret7": ret7, "vr": vol5 / vol30}))
    cs = pd.concat(rows); br = pd.concat(barrows)
    def grp(col, q=5):
        x = cs.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        return x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("unusual", "size"),
                                  total=("fwd", "mean"), unusual=("unusual", "mean"),
                                  t=("unusual", lambda s: s.mean() / s.std() * np.sqrt(len(s))),
                                  hit=("fwd", lambda s: (s > 0).mean()))
    out["cases by 30d ret"] = grp("ret30")
    out["cases by 7d ret"] = grp("ret7")
    out["cases by 3d ret"] = grp("ret3")
    out["cases by vol ratio 5d/30d"] = grp("vr")
    out["cases by forecast"] = grp("f")
    out["cases by coin"] = cs.groupby("coin").agg(n=("unusual", "size"), total=("fwd", "mean"),
                            unusual=("unusual", "mean"), t=("unusual", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    # bar gains when long by regime
    lb = br[br.alloc > 0].dropna(subset=["ret30"]).copy()
    lb["q30"] = pd.qcut(lb.ret30, 5, labels=False)
    out["long bars gain by 30d ret"] = lb.groupby("q30").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                            sum_gain=("gain", "sum"), mean_alloc=("alloc", "mean"), lo=("ret30", "min"), hi=("ret30", "max"))
    out["exposure"] = pd.Series({"share bars long": (br.alloc > 0).mean(), "mean alloc when long": lb.alloc.mean(),
                                 "max alloc": br.alloc.max()})
    return out
