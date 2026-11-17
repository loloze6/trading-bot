import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            share = b.get("debug_info.components.rsi_share.last_history_value")
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            past14 = c / c.shift(14) - 1
            past30 = c / c.shift(30) - 1
            n = len(b)
            for i in range(0, n - 14, 14):
                rows.append(dict(coin=coin, win=w, share=share.iloc[i] if share is not None else np.nan,
                                 past14=past14.iloc[i], past30=past30.iloc[i], vol20=vol20.iloc[i],
                                 fwd14=c.iloc[i+14]/c.iloc[i]-1, fwd7=c.iloc[i+7]/c.iloc[i]-1,
                                 fc=b["forecast"].iloc[i]))
            for i in range(0, n - 1):
                drows.append(dict(coin=coin, win=w, r0=r1.iloc[i], fwd1=c.iloc[i+1]/c.iloc[i]-1,
                                  vol20=vol20.iloc[i], wd=pd.Timestamp(b["timestamp"].iloc[i+1]).weekday(),
                                  pos=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["dfwd"] = g["fwd14"] - g.groupby("coin")["fwd14"].transform("mean")
    out["n_grid"] = len(g)
    def qtab(col):
        d = g.dropna(subset=[col, "dfwd"]).copy()
        d["q"] = pd.qcut(d[col], 5, labels=False, duplicates="drop")
        t = d.groupby("q").agg(n=("dfwd","size"), x=(col,"mean"), dfwd=("dfwd","mean"), sd=("dfwd","std"))
        t["t"] = t.dfwd / (t.sd / np.sqrt(t.n))
        return t.drop(columns="sd")
    for col in ["share", "past14", "past30", "vol20"]:
        out["q_" + col] = qtab(col)
    for col in ["share", "past14", "past30", "vol20"]:
        d = g.dropna(subset=[col, "dfwd"])
        s = stats.linregress(d[col], d["dfwd"])
        out["slope_" + col] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(d)}"
    # per coin share slope
    pc = {}
    for coin, d in g.dropna(subset=["share"]).groupby("coin"):
        s = stats.linregress(d["share"], d["dfwd"]); pc[coin] = s.slope / s.stderr
    out["share_t_by_coin"] = pd.Series(pc)
    D = pd.DataFrame(drows).dropna(subset=["r0", "fwd1"])
    D["z"] = D["r0"] / D["vol20"]
    D["dfwd1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    d = D.dropna(subset=["z"]).copy()
    d["q"] = pd.qcut(d["z"], 10, labels=False)
    t = d.groupby("q").agg(n=("dfwd1","size"), z=("z","mean"), dfwd1=("dfwd1","mean"), sd=("dfwd1","std"))
    t["t"] = t.dfwd1 / (t.sd / np.sqrt(t.n)); out["next1_by_zmove_decile"] = t.drop(columns="sd")
    t = D.groupby("wd").agg(n=("dfwd1","size"), m=("dfwd1","mean"), sd=("dfwd1","std"))
    t["t"] = t.m / (t.sd/np.sqrt(t.n)); out["weekday"] = t.drop(columns="sd")
    # book: position sign vs returns
    D["pnl"] = D["pos"] * D["fwd1"]
    D["side"] = np.sign(D["pos"])
    out["book_by_side"] = D.groupby("side").agg(n=("pnl","size"), pnl=("pnl","mean"), fwd1=("fwd1","mean"), pos=("pos","mean"))
    out["pnl_by_window"] = D.groupby("win")["pnl"].mean().describe()
    return out
