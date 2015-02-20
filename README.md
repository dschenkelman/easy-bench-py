# easy-bench-py
Small python program to perform simple benchmarks with `ab` and plot the results.

## Setup
Assuming you have `pip` installed:
```
make init
```

## Configuration
The configuration for the benchmarks is in the __config.yaml__ file. The accepted values are:
* `c_steps` - Concurrency steps. A list of concurrency values to be used.
* `n` - The total number of requests to perform in each `ab` run.
* `repetitions` - How many times each `(c_step, n)` pair must be executed. The average of the mean __Time per request__ for the repetitions is the result for the pair.
* `output` - The name of the file that will hold the resulting chart.
* `benchmarks` - An array of benchmarks.
  * `name` - The name of the benchmark. Displayed in the charts legend.
  * `parts` - An array of strings that are to be provided to `ab` when invoking it. Each element in the array must be a separate parameter for `ab`. For example, if you want to send an auth header for basic auth `-H "Authorization: Basic ZG9udDpsb29r"` you would use:
  ```yaml
  parts:
    - "-H"
    - "Authorization: Basic ZG9udDpsb29r"
    - "http://mysite.com"
  ```

## Executing
To run the program simply:
```
python main.py
```

Once it finishes some output will be printed via `stdout` and the chart will be stored in the `output` file.

With the existing `config.yaml` file the results look like this:
![res](https://cldup.com/cB4Q036nbe.png)

##Errors
Failed requests and non 2xx responses are considered errors and reported via `stderr`. Each error has the following format:
```
"Error: '{line}' rep: {r} c: {c} name: {benchmark}"
```
