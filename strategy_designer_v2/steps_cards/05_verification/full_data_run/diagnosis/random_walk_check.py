"""The window-mean reference on pure random walks (no effect exists). 141 windows of 122 daily bars (as the record),
a 50/200 SMA state, 10-bar forward returns on the non-overlapping grid, excess of the "on" blocks against (a) the mean of
the same window, (b) zero, the walk's true mean. 20 simulated datasets, fixed seed. Not market data."""
import numpy as np, pandas as pd
rng = np.random.default_rng(7)
H, W, WARM, NWIN, SIG = 10, 122, 250, 141, 0.035
def run(window_baseline):
    ex = []
    for _ in range(NWIN):
        p = pd.Series(np.exp(np.cumsum(rng.normal(0, SIG, WARM + W + H))))
        state = (p.rolling(50).mean() > p.rolling(200).mean()).astype(float).iloc[WARM:WARM + W].reset_index(drop=True)
        win = p.iloc[WARM:WARM + W + H].reset_index(drop=True)
        fw = (win.shift(-H) / win - 1).iloc[:W].where(np.arange(W) <= W - 1 - H)
        g = pd.DataFrame({"s": state, "fw": fw}).iloc[::H].dropna()
        ex += list(g.fw[g.s == 1] - (fw.mean() if window_baseline else 0.0))
    ex = np.array(ex); return ex.mean() / (ex.std(ddof=1) / np.sqrt(len(ex)))
for b in (True, False):
    ts = [run(b) for _ in range(20)]
    print(f"{'window mean' if b else 'true zero':11}: mean t {np.mean(ts):+.2f} (min {min(ts):+.2f}, max {max(ts):+.2f})")
