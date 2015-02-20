from __future__ import print_function
from yaml import load
from subprocess import check_output
from re import compile
from sys import stderr
import matplotlib.pyplot as plt
from distutils.spawn import find_executable

failed_request_regex = compile("Failed requests:\s*[1-9][0-9]*$")

non_two_hundred_responses_regex = compile("Non-2xx responses:\s*[1-9][0-9]*$")

time_per_request_regex = compile("^Time per request:\s*([0-9]*\.[0-9]*)\s*\[ms\]\s*\(mean\)$")

results = {}
errors = []

ab_path = find_executable('ab')

def print_error(*objs):
  print("ERROR: ", *objs, file=stderr)

with open("config.yaml", 'r') as stream:
  config = load(stream)
  print(config)
  for benchmark in config["benchmarks"]:
    benchmark_results = {}
    for c in config["c_steps"]:
      arguments = [ab_path, "-n", str(config["n"]), "-c", str(c)]
      arguments += benchmark["parts"]
      for r in range(config["repetitions"]):
        output = check_output(arguments)
        for line in output.split("\n"):
          if failed_request_regex.match(line) or non_two_hundred_responses_regex.match(line):
            errors.append("'{line}' rep: {r} c: {c} name: {benchmark}".format(line=line, r=r, c=c, benchmark=benchmark["name"]))
          match = time_per_request_regex.match(line)
          if (match):
            time_per_request = float(match.group(1))
            if c in benchmark_results:
              benchmark_results[c].append(time_per_request)
            else:
              benchmark_results[c] = [ time_per_request ]
      all_results = benchmark_results[c]
      benchmark_results[c] = sum(all_results) / float(len(all_results))
    results[benchmark["name"]] = benchmark_results

plt.xlabel('Concurrency')
plt.ylabel('Time per request')
handles = []

for err in errors:
  print_error(err)

for name, res in results.viewitems():
  xs = []
  ys = []
  for conc, time in res.viewitems():
    xs.append(conc)
    ys.append(time)
    print(name, conc, time)
  handle, = plt.plot(xs, ys, label=name)
  handles.append(handle)

plt.legend(handles, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

plt.savefig(config["output"])