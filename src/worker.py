import Pyro4
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-P", "--port", help="worker port to register with the Pyro daemon", type=int
)
args = parser.parse_args()


@Pyro4.expose
class Worker:
    def compute_factorial(self, start: int, end: int) -> int:
        res = 1
        for n in range(start, end + 1):
            res *= n

        return res


if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {Worker: f"worker.factorial.{args.port}"}, port=args.port, ns=True
    )
