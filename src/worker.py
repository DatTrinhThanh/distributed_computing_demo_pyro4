import Pyro4


@Pyro4.expose
class Worker:
    def compute_factorial(start: int, end: int) -> int:
        res = 1
        for n in range(start, end + 1):
            res *= n

        return res


if __name__ == "__main__":
    Pyro4.Daemon.serveSimple({Worker: "worker.factorial"}, ns=True)
