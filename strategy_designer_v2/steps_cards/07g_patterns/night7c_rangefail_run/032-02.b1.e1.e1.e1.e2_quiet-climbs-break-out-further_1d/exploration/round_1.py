import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 20
    rows = []      # breakout cases
    grid = []      # non-overlapping 20d grid, all bars
    after = []     # daily: return next 1d/5d after large moves
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            lr = np.r_[np.nan, c[1:]/c[:-1]-1]
            for i in range(0, n-H, H):
                grid.append((coin, w, c[i+H]/c[i]-1))
            # cases: first breakout per grid cell
            for g0 in range(0, n-H, H):
                for i in range(max(g0, 60), min(g0+H, n-H)):
                    pm = c[i-60:i].max()
                    if c[i] > pm:
                        r60 = c[i-1]/c[i-61]-1 if i >= 61 else np.nan
                        vol20 = np.nanstd(lr[i-19:i+1])
                        vol120 = np.nanstd(lr[max(1,i-119):i+1])
                        rng = c[i-60:i].max()/c[i-60:i].min()-1
                        r5 = c[i]/c[i-5]-1
                        rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(),
                            fwd=c[i+H]/c[i]-1, fwd5=c[i+5]/c[i]-1 if i+5<n else np.nan,
                            r60=r60, dist=c[i]/pm-1, volratio=vol20/vol120, rng60=rng,
                            r1=lr[i], r5=r5, wd=ts.iloc[i].weekday(),
                            fc=b["forecast"].iloc[i]))
                        break
    cs = pd.DataFrame(rows)
    gd = pd.DataFrame(grid, columns=["coin","w","r"])
    drift = gd.groupby("coin")["r"].mean(); sd = gd.groupby("coin")["r"].std()
    cs["ex"] = cs["fwd"] - cs["coin"].map(drift)
    cs["exz"] = cs["ex"]/cs["coin"].map(sd)
    out = {}
    out["n_cases"] = len(cs)
    def q(col, k=4):
        d = cs.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), k, labels=False)
        return d.groupby("q").agg(n=("ex","size"), lo=(col,"min"), hi=(col,"max"),
                                  ex=("ex","mean"), exz=("exz","mean"), hit=("fwd", lambda x:(x>0).mean()))
    for col in ["r60","dist","volratio","rng60","r1","r5"]:
        out["by_"+col] = q(col)
        d = cs.dropna(subset=[col])
        r, p = stats.spearmanr(d[col], d["ex"])
        out["spear_"+col] = f"rho {r:.3f} p {p:.3f} n {len(d)}"
    out["by_coin"] = cs.groupby("coin").agg(n=("ex","size"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["by_window"] = cs.groupby("w").agg(n=("ex","size"), ex=("ex","mean"))
    # non-breakout baseline: grid return after big 20d move
    big = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].astype(float).values; n=len(c)
            for i in range(20, n-H, H):
                big.append((coin, c[i]/c[i-20]-1, c[i+H]/c[i]-1 - drift[coin], c[i]/c[max(0,i-60):i].max()-1))
    bg = pd.DataFrame(big, columns=["coin","past20","ex","fromhigh"])
    bg["q"] = pd.qcut(bg["past20"].rank(method="first"), 5, labels=False)
    out["grid_by_past20"] = bg.groupby("q").agg(n=("ex","size"), lo=("past20","min"), hi=("past20","max"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    bg["q2"] = pd.qcut(bg["fromhigh"].rank(method="first"), 5, labels=False)
    out["grid_by_fromhigh60"] = bg.groupby("q2").agg(n=("ex","size"), lo=("fromhigh","min"), hi=("fromhigh","max"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # book days
    dd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            x = d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    dd["yr"] = pd.to_datetime(dd["day"]).dt.year
    out["book_by_year"] = dd.groupby("yr").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    out["coin_by_weekday"] = dd.groupby("wd")["coin_return"].agg(["mean","count", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    # top book days share
    br = dd.dropna(subset=["book_return"])
    br = br[br.book_return != 0]
    s = br.book_return.sort_values()
    out["book_tail"] = pd.Series({"n_active_days": len(s), "sum_all": s.sum(), "sum_top10": s.iloc[-10:].sum(), "sum_bottom10": s.iloc[:10].sum()})
    return out
