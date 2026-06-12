## Invariants & footguns

7. All components of ALL regimes update every bar; inactive-regime histories are always warm at switch. Do not "optimize" update() to active-regime-only — it would reintroduce switch staleness.
