# PyAF_Benchmarks

This repository contains/will contain benchmarks results/logs that are used to evaluate PyAF automatic forecasting tool.

Some benchmarks are official forecasting competitions : [M1, M2, M3, M4 , NN3 and NN5](https://en.wikipedia.org/wiki/Makridakis_Competitions)

Some are internal benchmarks (used mainly to evaluate new PyAF versions against previous ones) : YahooStocks (all stocks by index are forecast for 7 days).

We will run these benchmarks on a regular basis and update this repository when something changes.

Each log file gives the full log of PyAF execution, actual and predicted values as well as some performance measures (MAPE, RMSE, ...) and the total execution time.

Scripts used to run the benchmarks are included with PyAF : https://github.com/antoinecarme/pyaf/tree/master/benches
