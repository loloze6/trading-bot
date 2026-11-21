import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for coin in bars:
        allr = []
        for w, b in bars[coin].items():
            allr.append(b["close"].pct_change().dropna().values)
        mud = np.concatenate(allr).mean()
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1)/c - 1
            pos = b["postRebalance_current_allocation"]
            vol = c.pct_change().rolling(30).std()
            r7 = c/c.shift(7)-1
            f = b["forecast"]
            # forecast at entry carried: use abs forecast at bar
            g = pos*nxt
            for i in range(len(c)-1):
                if pos.iloc[i] < 0 and not np.isnan(g.iloc[i]):
                    rows.append(dict(coin=coin, w=w, gain=g.iloc[i], mkt=pos.iloc[i]*mud,
                                     timing=g.iloc[i]-pos.iloc[i]*mud, absf=abs(f.iloc[i]),
                                     vol=vol.iloc[i], r7=r7.iloc[i], pos=pos.iloc[i]))
    d = pd.DataFrame(rows)
    out["n_short_bars"] = len(d)
    out["overall"] = d[["gain","mkt","timing","pos"]].mean()
    def qt(col):
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 4, labels=False, duplicates="drop")
        g = dd.groupby("q").agg(lo=(col,"min"), hi=(col,"max"), n=("gain","size"),
                                gain=("gain","mean"), mkt=("mkt","mean"), timing=("timing","mean"), pos=("pos","mean"))
        g["t_gain"] = dd.groupby("q")["gain"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        return g
    for col in ["absf","vol","r7"]:
        out["q_"+col] = qt(col)
    d["y"] = np.where(d["w"].str[1:].astype(int) <= 12, "first_half", "second_half")
    out["by_half"] = d.groupby("y")[["gain","timing"]].mean()
    return out
