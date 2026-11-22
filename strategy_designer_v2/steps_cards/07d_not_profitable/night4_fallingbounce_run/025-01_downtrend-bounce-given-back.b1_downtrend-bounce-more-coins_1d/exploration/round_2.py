import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []; barrows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c)-5, 5):
                allr.append(c[i+5]/c[i]-1)
        dr5 = np.mean(allr)
        # daily mean coin return over all windows
        dd = []
        for w, df in wins.items():
            dd.append(df["close"].pct_change().dropna().values)
        dr1 = np.mean(np.concatenate(dd))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change(); sd = r1.rolling(20).std()
            z = r1/sd; r90 = c/c.shift(90)-1; r30 = c/c.shift(30)-1
            fwd = c.shift(-5)/c-1
            fc = df["forecast"]; al = df["postRebalance_current_allocation"]
            nxt = c.shift(-1)/c-1
            # cases: forecast <= -2 on grid
            for i in range(0, len(df)-5, 5):
                seg = fc.iloc[i:i+5]
                idx = seg[seg <= -2].index
                if len(idx):
                    j = idx[0]
                    if j+5 < len(df):
                        rows.append(dict(z=z[j], r90=r90[j], r30=r30[j], fc=fc[j],
                                         short_un=-(c[j+5]/c[j]-1-dr5), short_tot=-(c[j+5]/c[j]-1)))
            for i in range(len(df)-1):
                barrows.append(dict(al=al[i], fc=fc[i], gain=al[i]*nxt[i], mkt=al[i]*dr1,
                                    r90=r90[i], r30=r30[i], fresh=(fc[i] != 0)))
    d = pd.DataFrame(rows); b = pd.DataFrame(barrows).dropna(subset=["gain"])
    out = {}
    def s(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    d["zb"] = pd.cut(d.z, [0,1,2,3,99])
    out["cases short unusual by z"] = d.groupby("zb").apply(lambda g: s(g,"short_un"))
    out["cases short total by z"] = d.groupby("zb").apply(lambda g: s(g,"short_tot"))
    d["r30b"] = pd.cut(d.r30, [-9,-0.3,-0.15,0,0.15,9])
    out["cases short unusual by 30d ret"] = d.groupby("r30b").apply(lambda g: s(g,"short_un"))
    d["r90b"] = pd.cut(d.r90, [-9,-0.45,-0.25,-0.1,0])
    out["cases short unusual by 90d ret"] = d.groupby("r90b").apply(lambda g: s(g,"short_un"))
    out["cases short total by 90d ret"] = d.groupby("r90b").apply(lambda g: s(g,"short_tot"))
    sh = b[b.al < -1e-6]
    out["short bars: gain split"] = pd.Series({"n": len(sh), "mean_gain%": 100*sh.gain.mean(),
        "market_part%": 100*sh.mkt.mean(), "timing%": 100*(sh.gain-sh.mkt).mean(),
        "share_bars_forecast_zero": (~sh.fresh).mean(),
        "gain_fc_zero%": 100*sh[~sh.fresh].gain.mean(), "gain_fc_nonzero%": 100*sh[sh.fresh].gain.mean()})
    sh = sh.copy(); sh["r90b"] = pd.cut(sh.r90, [-9,-0.45,-0.25,-0.1,0,9])
    out["short bars gain by 90d ret"] = sh.groupby("r90b").gain.agg(["size","mean"])
    t = pd.concat([df for wins in data["trades"].values() for df in wins.values()])
    t["dd"] = t.duration_minutes/1440
    t["durb"] = pd.cut(t.dd, [0,5.5,10,20,999])
    out["trades by duration"] = t.groupby("durb").agg(n=("dd","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    out["trades by side"] = t.groupby("side").agg(n=("dd","size"), gross=("profit_loss_percent","mean"), days=("dd","mean"))
    return out
