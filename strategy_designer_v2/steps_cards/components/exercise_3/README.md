# components, exercise 3: the second pass (2026-11-17, written before the run)

**Purpose.** The card's validation, second pass: the step answers the open wishes left after exercises 1 and 2
(36 open wishes: night_run, night_013_run, volume_run), with the rules ruled on since (rule 1: the same quantity against another
base, and a mirror, are one measure; rule 2: a new setting must change the output on real data, checked on real data).

**Call.** `build_component.py --runs <all runs> --python VENV` (only open wishes are asked).

**Pre-registered outcomes.**
- **A.** Quality: every built component passes every check and the proof.
- **B.** Standardization: no two classes for one measure once the call ends (read the catalogue); variants of an
  existing measure come back as exists or as a setting on it (a mean of several bars' volume, the median of the bars
  before t: settings on `VolumeRatioComponent`); a past high or its break, one or two new measures.
- **C.** Rule 2 refuses a setting that changes nothing (if one is proposed), and the model then answers exists.
- **D.** Few cannot build, each naming what is missing.
- **E.** A defect of the step: fixed if general, written here.
- Unblocking: counted after the call (the ideas whose wishes are all answered built or exists); rerunning them waits
  for the ranking discussion (topic 3).

## Reading
(written after the run)
