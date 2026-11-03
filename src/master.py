import Pyro4


class Master:
    def __init__(self):
        self.workers: set[Pyro4.Proxy] = self.find_workers()

    def find_workers(self) -> set[Pyro4.Proxy]:
        workers = set()
        with Pyro4.locateNS() as ns:
            for _, worker_uri in ns.list(prefix="worker.factorial").items():
                workers.add(Pyro4.Proxy(worker_uri))
        return workers


if __name__ == "__main__":
    m = Master()
    print(m.workers)