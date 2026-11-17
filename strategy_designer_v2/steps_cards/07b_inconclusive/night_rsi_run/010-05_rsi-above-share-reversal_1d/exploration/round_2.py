import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            lh = df["debug_info.components.rsi_share.last_history_value"]
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            tr = c / c.shift(30) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [3, 7, 14]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr.iloc[i], fc=df["forecast"].iloc[i],
                                     lh=lh.iloc[i], vol=vol.iloc[i], tr=tr.iloc[i],
                                     ret=c.iloc[i+h]/c.iloc[i]-1))
    R = pd.DataFrame(rows)
    R["dret"] = R["ret"] - R.groupby(["coin","h"])["ret"].transform("mean")

    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "dret"])
        if len(g) < 8 or g[x].std() == 0: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(g[x], g["dret"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope/s.stderr})

    out["by_h_rawlh"] = R.groupby("h").apply(lambda g: slope(g, "lh"))
    out["lh_describe"] = R[R.h==14]["lh"].describe()
    R["volq"] = R.groupby("h")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_h_volq"] = R.groupby(["h","volq"]).apply(slope)
    R["trs"] = np.sign(R["tr"])
    out["by_h_trendsign"] = R.groupby(["h","trs"]).apply(slope)
    R["fs"] = np.sign(R["fc"])
    out["by_h_fcside"] = R.groupby(["h","fs"]).apply(slope)
    out["h3_by_year"] = R[R.h==3].groupby("year").apply(slope)
    out["h7_by_coin"] = R[R.h==7].groupby("coin").apply(slope)
    # book timing by coin
    tm = []
    for coin, ws in bars.items():
        allr = pd.concat([d["close"].pct_change() for d in ws.values()])
        mu = allr.mean()
        for w, df in ws.items():
            nx = df["close"].shift(-1)/df["close"]-1
            p = df["postRebalance_current_allocation"]
            tm.append(dict(coin=coin, gain=(p*nx).mean(), timing=(p*(nx-mu)).mean(), pos=p.mean()))
    T = pd.DataFrame(tm)
    out["book_by_coin"] = T.groupby("coin").mean()
    return out
