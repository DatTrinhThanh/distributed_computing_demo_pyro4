import Pyro4
import argparse
import math
import sys

sys.set_int_max_str_digits(0)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-P", "--port", help="worker port to register with the Pyro daemon", type=int
)
args = parser.parse_args()


@Pyro4.expose
class Worker:
    def compute_factorial(self, start: int, end: int) -> int:
        return math.prod(range(start, end + 1))


if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {Worker: f"worker.factorial.{args.port}"}, port=args.port, ns=True
    )
