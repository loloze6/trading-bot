import numpy as np, pandas as pd
from scipy import stats

def rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100/(1+up/dn)

def explore(data):
    bars = data["bars"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = rsi(c)
            share = (r > 50).astype(float).where(r.notna()).rolling(30, min_periods=30).mean()
            lh = df.get("debug_info.components.rsi_share.last_history_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [3, 7, 14, 30]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, wn=int(w[1:]), h=h, year=yr.iloc[i],
                                     fc=df["forecast"].iloc[i],
                                     lh=lh.iloc[i] if lh is not None else np.nan,
                                     share=share.iloc[i],
                                     ret=c.iloc[i+h]/c.iloc[i]-1))
    R = pd.DataFrame(rows)
    R["dret"] = R["ret"] - R.groupby(["coin","h"])["ret"].transform("mean")

    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "dret"])
        if len(g) < 8 or g[x].std() == 0: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(g[x], g["dret"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope/s.stderr})

    out["by_h"] = R.groupby("h").apply(slope)
    out["by_h_rawshare"] = R.groupby("h").apply(lambda g: slope(g, "share"))
    R14 = R[R.h == 14]
    out["h14_by_coin"] = R14.groupby("coin").apply(slope)
    out["h14_by_year"] = R14.groupby("year").apply(slope)
    R14 = R14.copy()
    R14["side"] = np.sign(R14["fc"])
    out["h14_by_fc_sign"] = R14.groupby("side")["dret"].agg(["count","mean","std"])
    R14["q"] = pd.qcut(R14["fc"], 5, labels=False, duplicates="drop")
    out["h14_by_fc_quint"] = R14.groupby("q").agg(n=("dret","count"), fc=("fc","mean"), dret=("dret","mean"), share=("share","mean"))
    R14["sq"] = pd.qcut(R14["share"], 5, labels=False, duplicates="drop")
    out["h14_by_share_quint"] = R14.groupby("sq").agg(n=("dret","count"), share=("share","mean"), dret=("dret","mean"))
    # regime: coin's past trend proxy -> by sign of fwd mean in the window? use share of window positive (known only ex post) -> skip; use vol
    out["corr_fc_share"] = float(R14[["fc","share"]].dropna().corr().iloc[0,1])
    out["corr_fc_lh"] = float(R14[["fc","lh"]].dropna().corr().iloc[0,1])
    out["n_windows_per_coin"] = R14.groupby("coin")["w"].nunique()
    return out
