# GRB-ML

## Installation

```bash
pip install -e .
```



## What is GRB-ML?

GRB-ML is a Python package that uses simulations and machine learning to rapidly. This is necessary and useful since [GRB]() monitoring CubeSats and other satellites have to quickly decide whether to trigger an event alert to the [GCN]() or whether the signal was a false alert. The goal is to train a lightweight and efficient, but highly accurate machine model (based on [`sklearn`]() tools) to quickly predict whether a photon count signal is likely to be a GRB or rather noise, [cosmic rays]() or other radiation (e.g., [SAA]()).

## Who is GRB-ML For?

GRB-ML was first developed for GRB CubeSats, for instance initiatives like EIRSAT or ... . Therefore, it was created to run with limited resources. However, these characteristics also makes it suitable for anyone to run on their personal computers and easily implementable in other pipelines.

## Authorship

This package was developed by [Alcaide-Núñez J.](https://joanalnu.pages.dev) and (...) in the context of the [CAPIBARA Collaboration]()'s GAMMA Team.

## Citation

Currently this package does not have a scientific citation. However, if you use this in your research, we would appreciate if you acknowledge it's use.

