import Pyro4

class Master:
    def __init__(self):
        self.workers: set[Pyro4.Proxy] = set()

    def find_workers(self):
        with Pyro4.locateNS() as ns:
            for worker, worker_uri in ns.list(prefix="factorial.worker").items():
                print(worker, worker_uri)

if __name__ == "__main__":
    m = Master()
    m.find_workers()