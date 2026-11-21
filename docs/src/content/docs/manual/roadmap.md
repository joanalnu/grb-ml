---
title: "Project Roadmap"
author: joanalnu & Claude
description: "Where GRB-ML stands, what is left for the v0.1 handover, who does what, and how tasks are managed."
---

> **Status:** draft for the 2026-11-21 team meeting. Dates, owners and decisions marked _proposed_ become final once the team confirms them. Last updated 2026-11-20.
>
> **Disclosure** (see the [AI Policy](/manual/ai-policy/)): drafted with LLM assistance (Claude). The audit figures in "Where things stand" were produced by running the repository's own code.

## Purpose and scope

GRB-ML is a simulation and benchmarking toolkit for gamma-ray burst (GRB) triggers on CubeSat-class detectors. It compares classical threshold triggers with lightweight `scikit-learn` classifiers on simulated photon-count streams.

**In scope for v0.1 (the handover release)**

- The five modules: `simulations`, `features`, `dataset`, `models`, `evaluate`.
- A detector configuration with placeholder values that the team can replace.
- A threshold baseline and two `scikit-learn` models.
- Evaluation per event, under a false-alarm budget.
- One runnable end-to-end example, tests with CI, and documentation.

**Out of scope for v0.1**

- Flight software and hardware-specific tuning.
- Absolute performance claims. No detector specification exists yet, so results are comparisons between methods.
- Validation on real data, and a PyPI release (both are in the backlog).

## Where things stand

Audited on 2026-11-20 by reading and running the code.

| Module | State | Notes |
| :--- | :--- | :--- |
| `simulations.py` | Implemented | Background, FRED-like burst, cosmic-ray spike, SAA swell, event injector. No tests. Global NumPy random state. Rates and bin width are hard-coded. |
| `features.py` | Implemented | Window splitting and 7 features (SNR twice, hardness ratio, peak-to-mean twice, asymmetry twice). No gap between background and foreground windows. |
| `dataset.py` | Partly implemented | `generate_labels` works and has one test. `generate_dataset` is a stub that returns `None`. |
| `models.py` | Empty | |
| `evaluate.py` | Empty | |
| Packaging, CI, docs | Partly | Documentation site and API generator exist. No CI, no `LICENSE` file, incomplete requirements. |

### Finding that affects everything downstream: background contamination

Features are computed against the 100 bins before each foreground window. Once a burst is under way, those bins contain the burst itself, so the background estimate is inflated and the signal-to-noise ratio collapses.

We checked this on the timeline from `tests/examples/simulations_example.py` (a 300-bin SAA crossing, a cosmic-ray spike and a 120-bin burst) over 20 random seeds, extracting features and labels and looking at the low-channel SNR of windows labelled as GRB. Of the roughly 121 positive windows per orbit, only about 8 reached an SNR of 5, and the median SNR of positive windows was slightly negative (about -0.4).

In other words, the labels mark the whole burst as positive while the features can only see its first few bins. A model trained on this data would be learning an inconsistent target. These figures describe this simulated setup, not a real detector. Task T-01 must be finished before models are trained or compared.

### Smaller issues found

- `generate_grb_pulse` computes a spectral-cooling curve for the high channel and then overwrites it with a constant hardness ratio, so spectral cooling is not actually implemented. Implement it or delete the dead lines.
- `generate_labels` requires an `is_grb` key although its docstring calls the key optional.
- The simulators cannot be seeded individually; they use the global NumPy random state.
- `setup.py` reads the version with `line.split()[-1]`, which returns the word "update" from the comment in `_version.py`. This has no effect yet because the `version=` argument is commented out. `package_data` still contains a placeholder (`package_name`).
- `requirements.txt` lacks `scikit-learn` and `matplotlib`, and `setup.py` passes the whole file, including development tools (`twine`, `wheel`, `pytest`, `numpydoc`), as runtime requirements.
- The package declares the MIT license, but the repository has no `LICENSE` file.
- `grb_ml/__init__.py` exports only `simulations`.

## Milestones (proposed)

| ID | Milestone | Target | Tasks | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| M0 | Decisions | 2026-11-28 | T-00 | Name settled, decisions confirmed, owners assigned |
| M1 | Trustworthy simulator | 2026-12-13 | T-01, T-02, T-03, T-10 | Features and labels agree, runs are reproducible, detector assumptions live in one place |
| M2 | Dataset and baseline | 2027-01-03 | T-04, T-05, T-09 | Dataset grouped by orbit, threshold baseline, tests and CI |
| M3 | Models and evaluation | 2027-01-24 | T-06, T-07, T-08 | One plot comparing baseline and ML at a fixed false-alarm budget |
| M4 | Handover | 2027-01-31 | T-11, T-12, T-13 | Docs in sync, walkthrough done, benchmark run by the team |

## Task board: Track A (v0.1 handover)

Size: S is up to 2 hours, M up to 4 hours, L up to a day. These are rough estimates for someone who knows the code: about 44 hours in total (without T-13), of which about 32 are the critical path owned by the maintainer. Tasks marked "open" are small and independent, suitable for other contributors.

| ID   | Task                                                                      | Module                | Size | Owner (proposed)                   | Status | Depends on                 |
|:-----|:--------------------------------------------------------------------------|:----------------------|:-----|:-----------------------------------|:-------|:---------------------------|
| T-00 | Decide the package name and rename                                        | all                   | S    | @joanalnu                          | Done   | none                       |
| T-01 | Make features and labels consistent (background contamination)            | features, dataset     | M    | @joanalnu                          | Todo   | none                       |
| T-02 | Reproducible randomness (seed or `Generator`)                             | simulations           | S    | open                               | Todo   | none                       |
| T-03 | Detector configuration with placeholder values                            | simulations, features | M    | @joanalnu                          | Todo   | T-02                       |
| T-04 | Build `generate_dataset` (Monte Carlo orbits, grouped by orbit)           | dataset               | M    | @joanalnu                          | Todo   | T-01, T-03                 |
| T-05 | Threshold baseline trigger                                                | models                | S    | open                               | Todo   | T-01                       |
| T-06 | `scikit-learn` models behind the same interface                           | models                | M    | @joanalnu                          | Todo   | T-04, T-05                 |
| T-07 | Event-level evaluation under a false-alarm budget                         | evaluate              | L    | @joanalnu                          | Todo   | T-05                       |
| T-08 | End-to-end example, from clone to comparison plot                         | examples              | M    | @joanalnu                          | Todo   | T-06, T-07                 |
| T-09 | Tests for simulations, features and dataset, plus CI                      | tests                 | M    | open                               | Todo   | T-02                       |
| T-10 | Packaging hygiene                                                         | setup                 | S    | open                               | Todo   | none                       |
| T-11 | Documentation sync                                                        | docs                  | S    | open                               | Todo   | T-08                       |
| T-12 | Handover walkthrough and checklist                                        | all                   | S    | @joanalnu and receiving maintainer | Todo   | T-01 to T-11               |
| T-13 | Run the benchmark with real detector parameters and write up the findings | docs                  | M    | collaborator (TBD)                 | Todo   | T-08, parameters available |

### Task details

Each task is done when everything listed under it is true, and the general Definition of Done below also holds.

**T-00 Decide the package name and rename.** The current name clashes with an existing repository (see [Naming](/manual/naming/)).
- A name is chosen and recorded in the decisions log.
- The repository, the `grb_ml` package directory, `setup.py`, README, documentation titles and imports are renamed. Do this early, before other tasks touch many files.

**T-01 Make features and labels consistent.**
- Choose and implement one fix: a buffer gap between background and foreground windows, a background estimate frozen before the foreground window, or labelling only the windows where the burst begins. Document the choice and why.
- Repeating the contamination check described above shows a median SNR of positive windows above zero.
- `generate_labels` treats a missing `is_grb` as 0.
- A test covers a burst longer than the foreground window.

**T-02 Reproducible randomness.**
- Every simulation function accepts a `numpy.random.Generator` or a seed and no longer uses the global state.
- The same seed gives identical output (tested); the example is updated.

**T-03 Detector configuration.**
- A single configuration object holds bin width, per-channel background rates, window sizes and channel labels. No such numbers remain hard-coded in the module bodies.
- Defaults are clearly marked as placeholders.
- Feature extraction handles a zero-variance background without raising an error.

**T-04 Build `generate_dataset`.**
- Returns the feature matrix, the labels and an orbit id for every row.
- Burst amplitude, rise and decay times, hardness ratio, SAA duration and cosmic-ray rate are drawn from documented ranges; the class ratio is configurable.
- Tests cover shapes and reproducibility.
- The documentation explains why splits must be grouped by orbit: neighbouring windows are almost identical, so splitting by row leaks information.

**T-05 Threshold baseline trigger.**
- A sigma-threshold trigger (default 5 sigma) with the same interface as the models; tested.

**T-06 `scikit-learn` models.**
- `RandomForestClassifier` and `HistGradientBoostingClassifier`, with class weights for the imbalance, trainable through one function or class.
- Scores come from `predict_proba`; docstrings and a test on a small dataset exist.

**T-07 Event-level evaluation.**
- A burst counts as detected if any flagged window falls inside it; a false alarm is a run of flagged windows outside any burst.
- Reports recall at a fixed false-alarm budget (per orbit and per hour, using the bin width), the precision-recall curve and its area, model size and per-window inference time.
- A hand-made test case checks the counting rules.

**T-08 End-to-end example.**
- One script or notebook goes from simulation to a plot comparing the baseline and both models, with a fixed seed.
- Someone other than the maintainer runs it from a fresh clone by following the README.

**T-09 Tests and CI.**
- Tests for every public function in `simulations` and `features` (shapes, bounds, error cases) and for `dataset`.
- GitHub Actions runs `pytest` on every push and pull request.

**T-10 Packaging hygiene.**
- Runtime and development requirements are separated; `scikit-learn` is added and `matplotlib` is optional.
- The version is read correctly from `_version.py` and passed to `setup`; the `package_data` placeholder is removed.
- A `LICENSE` file is added, the submodules are exposed in `__init__.py`, and the Python version floor (currently 3.12) is reviewed.

**T-11 Documentation sync.**
- README and the Getting Started page agree; this roadmap replaces the old one; the API reference is regenerated with `python generate_docs.py`.

**T-12 Handover walkthrough.** The handover checklist below is complete.

**T-13 Benchmark with real parameters.**
- Real detector parameters are in a configuration file in the repository.
- The results and a short interpretation of what they mean for the mission concept are written in the documentation.

## Backlog: Track B (after handover, owned by the team)

Each item needs an owner before it starts. None of these is part of the maintainer's handover commitment.

| ID | Item | Note |
| :--- | :--- | :--- |
| B-01 | Poisson-FOCuS baseline | Check for an existing open implementation and its licence before writing one. Reference: Dilillo et al. 2024, ApJ 962, 137. |
| B-02 | Multi-timescale SNR and a rise/decay skewness feature | Carried over from the previous roadmap. |
| B-03 | Anomaly detection (`IsolationForest`) | Does an unsupervised model flag transient types it has never seen? |
| B-04 | More realistic simulation | Spectral shapes, real light-curve templates, orbital background variation, and the spectral-cooling decision. |
| B-05 | Validation on real archival data | For example Fermi GBM through NASA's Gamma-ray Data Tools, or Swift/BAT. |
| B-06 | Onboard feasibility | Model export, quantization, latency and memory against real hardware limits. |
| B-07 | Release | PyPI, Zenodo DOI, `CITATION.cff`, possibly a JOSS submission. |
| B-08 | Multi-satellite timing and coincidence | Only if the dual-satellite concept goes ahead. |

## Working agreement

- **Source of truth.** One GitHub issue per task ID, on a Projects board with the columns Todo, Doing, Review, Done and Blocked. Until the issues exist, this page is the board.
- **Labels.** `track:A` or `track:B`, `module:<name>`, `size:S`, `size:M`, `size:L`, `good first task`, `blocked`.
- **Ownership.** One owner per task; claim a task by commenting on its issue. At most two tasks in progress per person.
- **Stale rule.** If a claimed task has no activity for three weeks it goes back to Todo and is unassigned, without blame.
- **Branches and pull requests.** Branch `task/T-04-generate-dataset`; the pull request title starts with the task ID; squash merge.
- **Reviews.** Every pull request gets a reviewer who did not write it. If nobody responds within seven days, the author may merge after a careful self-review and says so in the pull request.
- **Check-in.** A 20-minute call every two weeks, or an asynchronous post in a pinned "Status" issue: done, doing, blocked.
- **Definition of Done.** Acceptance criteria met; tests added or updated and `pytest` passing; NumPy-style docstrings written and the API reference regenerated; any AI assistance disclosed in the pull request, as the [AI Policy](/manual/ai-policy/) requires; board updated.

## Handover

The original maintainer is stepping back from feature work. The goal of this plan is that the team can run, understand and extend the project without them.

### Roles

| Role | Who | Responsibility |
| :--- | :--- | :--- |
| Maintainer until handover | @joanalnu | Owns the critical path in Track A, reviews pull requests, passes on knowledge. |
| Receiving maintainer | TBD at the meeting | After handover: triages issues, merges pull requests, owns the board and releases. |
| Detector liaison | TBD at the meeting | Supplies detector parameters (T-13) and interprets the results. |
| Contributors | Anyone on the team | Take open tasks. |

### The project is handed over when

- [ ] Every Track A task is done, or has been moved to Track B with a note.
- [ ] Someone other than the maintainer has gone from a fresh clone to the comparison plot by following the README (T-08).
- [ ] Continuous integration is green on the main branch.
- [ ] At least two active team members have admin rights, or the repository has moved to the team's GitHub organisation.
- [ ] The documentation build is described, including where the site is hosted (not documented yet).
- [ ] A walkthrough session of about 45 minutes has been held and recorded, and its notes are linked here.
- [ ] The README names the receiving maintainer.

### After handover (proposed)

The maintainer stops feature work and answers questions in GitHub issues for four weeks. They remain credited as author. Everything in Track B belongs to the team.

### How the code fits together

- A signal is a tuple `(low, high)` of 1-D integer arrays, one value per time bin and channel.
- An event is a dictionary with the keys `signal`, `start_bin`, `type` and `is_grb`.
- Pipeline: `generate_background` and the event generators, then `detector_counts`, then `feature_extraction_loop`, which returns the matrix `X` with shape (n, 7). `generate_labels` returns `y` with exactly the same rows.
- Feature order: SNR (low), SNR (high), hardness ratio, peak-to-mean (low, high), asymmetry (low, high).
- Window layout: the background window is the 100 bins before bin i, the foreground window the 10 bins from i. Valid windows therefore number `n_bins - 100 - 10 + 1`.
- Docs: NumPy-style docstrings feed `generate_docs.py`, which writes `docs/src/content/docs/reference/`. Never edit those pages by hand. Manual pages live in `docs/src/content/docs/manual/`.
- Tests live in `tests/`; runnable demos in `tests/examples/`.

## Decisions log (proposed)

| ID | Decision | Reason |
| :--- | :--- | :--- |
| D-01 | Keep `scikit-learn` models, but judge them against classical triggers. | A trigger is only worth flying if it beats or complements the simple alternative. |
| D-02 | All detector assumptions live in one configuration with placeholder defaults. | Nobody on the team knows the detector yet; real numbers can be dropped in later. |
| D-03 | Evaluate per event under a false-alarm budget, and split data by orbit. | Per-window scores flatter the model, and splitting by row leaks information. |
| D-04 | Fix feature and label consistency (T-01) before training any model. | See "Finding that affects everything downstream". |
| D-05 | Handover is the end point for the original maintainer. | A volunteer project needs a defined finish and several people who can run it. |

## Open questions for the meeting

1. Which detector parameters can the team provide, and by when?
2. Who becomes the receiving maintainer, and who is the detector liaison?
3. Should the repository move to the team's GitHub organisation?
4. What is the new package name (T-00)?
5. The AI policy says documentation written by an LLM is not accepted, yet this page was drafted with one. Either amend the policy (for example, allow disclosed, human-reviewed documentation) or rewrite such pages by hand.
6. Is a Python 3.12 floor acceptable for the whole team?
7. Where is the documentation site hosted, and who can deploy it?
8. Biweekly call or asynchronous status posts?

## Risks

| Risk | Mitigation |
| :--- | :--- |
| Few team members are active. | Keep tasks small and independent; use the stale rule; require a second person to run the example before handover. |
| No real detector parameters. | Present results as method comparisons; keep everything in the configuration (T-03). |
| The simulation is simpler than reality. | State the limitation; plan validation on real data (B-05). |
| Scope creep. | Anything outside Track A goes to Track B and needs an owner. |
| Name clash makes the project hard to find. | Rename early (T-00). |
