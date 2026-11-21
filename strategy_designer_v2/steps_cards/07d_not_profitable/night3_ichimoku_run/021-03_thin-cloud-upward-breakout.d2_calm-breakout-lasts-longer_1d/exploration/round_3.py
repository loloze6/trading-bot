import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]; n = len(b)
            ten = (hi.rolling(9).max()+lo.rolling(9).min())/2
            kij = (hi.rolling(26).max()+lo.rolling(26).min())/2
            spa = (ten+kij)/2
            spb = (hi.rolling(52).max()+lo.rolling(52).min())/2
            lr = np.log(cl).diff()
            reg = b["regime"]
            cross = (reg=="trending") & (reg.shift(1)!="trending")
            alloc = b["postRebalance_current_allocation"].fillna(0)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in np.where(cross)[0]:
                j = min(i+40, n-1)
                if j-i < 10: continue
                path = cl.iloc[i:j+1]/cl.iloc[i]-1
                g = (alloc.iloc[i:j]*(cl.shift(-1)/cl-1).iloc[i:j]).sum()
                recs.append(dict(coin=c, window=w, year=yr.iloc[i], fwd=path.iloc[-1], mae=path.min(),
                    gain=g, full=(j-i)==40,
                    r30=cl.iloc[i]/cl.iloc[i-30]-1 if i>=30 else np.nan,
                    r60=cl.iloc[i]/cl.iloc[i-60]-1 if i>=60 else np.nan,
                    off60=cl.iloc[i]/hi.iloc[max(0,i-60):i+1].max()-1 if i>=40 else np.nan,
                    futcloud=(spa.iloc[i]/spb.iloc[i]-1) if not np.isnan(spb.iloc[i]) else np.nan,
                    kslope=kij.iloc[i]/kij.iloc[i-10]-1 if i>=36 else np.nan,
                    vol20=lr.iloc[i-19:i+1].std()*np.sqrt(365) if i>=20 else np.nan))
    X = pd.DataFrame(recs)
    out["n_cross"] = len(X)
    out["by_year"] = X.groupby("year").agg(n=("fwd","size"), fwd=("fwd","mean"), mae=("mae","mean"), gain=("gain","sum"))
    for col in ["r30","r60","off60","futcloud","kslope","vol20"]:
        d = X.dropna(subset=[col])
        k = pd.qcut(d[col], 3, labels=False, duplicates="drop")
        gg = d.groupby(k).agg(n=("fwd","size"), lo=(col,"min"), hi=(col,"max"), fwd=("fwd","mean"),
                              mae=("mae","mean"), gain=("gain","mean"), worst_mae=("mae","min"))
        out["by_"+col] = gg
        out["rho_"+col] = d[[col,"fwd","mae","gain"]].corr(method="spearman")[col].drop(col)
    d = X.dropna(subset=["futcloud"])
    a = d[d.futcloud>0]; bb = d[d.futcloud<=0]
    out["futcloud_sign"] = pd.DataFrame({"n":[len(a),len(bb)],"fwd":[a.fwd.mean(),bb.fwd.mean()],
        "mae":[a.mae.mean(),bb.mae.mean()],"gain":[a.gain.mean(),bb.gain.mean()]}, index=["rising","falling"])
    out["futcloud_mae_t"] = float(stats.ttest_ind(a.mae, bb.mae, equal_var=False).statistic)
    out["futcloud_fwd_t"] = float(stats.ttest_ind(a.fwd, bb.fwd, equal_var=False).statistic)
    return out
