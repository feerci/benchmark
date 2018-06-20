FEERCI Benchmark
******************************************


**FEERCI** is an opinionated, easy-to-use package for calculating EERs and non-parametric confidence intervals efficiently. This repository contains scripts for running speed and accuracy benchmarks against a similar function in the `bob` toolkit. We provide a docker container which this benchmark can be run in.

Run
=======

The easiest way to run the benchmark is using Docker::

    docker build -t feerci_benchmark .
    docker run feerci_benchmark > results.csv

Otherwise, please ensure you are running an environment with `bob` installed. After this, run::

    pip install -r requirements.txt
    ./benchmark_run.sh > results.csv


We provide a script for plotting, it assumes the existence of `results.csv` in the working directory::

    pip install -r requirements_plots.txt
    python benchmark_plots.py
