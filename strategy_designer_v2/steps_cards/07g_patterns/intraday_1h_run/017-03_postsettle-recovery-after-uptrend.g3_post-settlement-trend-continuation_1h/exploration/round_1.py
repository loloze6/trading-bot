import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c in bars:
        # coin mean 2-bar return on grid
        g2 = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-2, 2)
            g2.append(cl[idx+2]/cl[idx]-1)
        m2 = np.concatenate(g2).mean()
        for w, b in bars[c].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour.values
            b["wd"] = ts.dt.weekday.values
            cl = b["close"]
            r72 = cl/cl.shift(72)-1
            z = (r72/ r72.abs().rolling(72, min_periods=20).mean().shift(1)).clip(-2,2)
            b["z"] = z
            b["fwd2"] = cl.shift(-2)/cl-1-m2
            b["fwd1"] = cl.shift(-1)/cl-1
            b["r1"] = cl/cl.shift(1)-1
            b["vol24"] = b["r1"].rolling(24).std()
            b["vrel"] = b["volume"]/b["volume"].rolling(168).median()
            b["gain"] = b["postRebalance_current_allocation"]*b["fwd1"]
            b["fee"] = b["total_portfolio_value"].shift(-1)  # placeholder
            b["coin"]=c; b["win"]=w
            rows.append(b[["coin","win","hour","wd","z","fwd2","fwd1","r1","vol24","vrel","gain","forecast","postRebalance_current_allocation","total_portfolio_value","postRebalance_total_value"]])
    d = pd.concat(rows, ignore_index=True)
    # slope of fwd2 on z by hour (one case per day per hour)
    res=[]
    for h, g in d.dropna(subset=["z","fwd2"]).groupby("hour"):
        s = stats.linregress(g["z"], g["fwd2"])
        sm = (np.sign(g["z"])*g["fwd2"])
        res.append((h, len(g), s.slope*1e4, s.slope/s.stderr, sm.mean()*1e4))
    out["slope_fwd2_on_z_by_hour(bp)"] = pd.DataFrame(res, columns=["hour","n","slope_bp","t","signmean_bp"]).set_index("hour")
    # mean 1h return by hour of the bar starting at hour+1 (fwd1 from bar t)
    hh = d.dropna(subset=["r1"]).groupby("hour")["r1"].agg(["mean","std","count"])
    hh["t"]=hh["mean"]/(hh["std"]/np.sqrt(hh["count"])); hh["mean"]*=1e4
    vr = d.dropna(subset=["vrel"]).groupby("hour")["vrel"].mean()
    hh["vrel"]=vr
    out["ret_of_bar_closing_at_hour_bp"]=hh[["mean","t","count","vrel"]]
    # book: gross vs fees
    fee = (d["total_portfolio_value"]-d["postRebalance_total_value"]).fillna(0)
    out["book_gross_gain_sum_per_coinwin_mean"] = float(d["gain"].sum()/ (6*24))
    out["fee_frac_sum_per_coinwin_mean"] = float((fee/d["total_portfolio_value"]).sum()/(6*24))
    act = d[d["postRebalance_current_allocation"].abs()>0]
    out["active_by_hour"]=act.groupby("hour")["gain"].agg(["count","mean"]).assign(mean_bp=lambda x:x["mean"]*1e4)[["count","mean_bp"]]
    # reversal after large 1h moves: fwd1 on r1 by vol tercile
    e = d.dropna(subset=["r1","fwd1","vol24"]).copy()
    e["zr"]=e["r1"]/e["vol24"]
    e["vq"]=e.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,3,labels=False))
    r=[]
    for q,g in e.groupby("vq"):
        s=stats.linregress(g["zr"].clip(-5,5),g["fwd1"]); r.append((q,len(g),s.slope*1e4,s.slope/s.stderr))
    out["fwd1_on_zr_by_vol_tercile"]=pd.DataFrame(r,columns=["vq","n","slope_bp","t_overlap_ok_1h"]).set_index("vq")
    wd = d.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["mean","std","count"])
    wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"])); wd["mean"]*=1e4
    out["ret_by_weekday_bp"]=wd[["mean","t"]]
    return out
