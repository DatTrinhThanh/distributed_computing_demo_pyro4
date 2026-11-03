import Pyro4
from typing import List, Optional


class Master:
    def __init__(self):
        self.workers: set[Pyro4.Proxy] = self.find_workers()

    def distribute_factorial(self, n: int) -> Optional[List[tuple[int, int]]]:
        BASE_CASE = 1
        if n < BASE_CASE:
            return
        chunk_size = max(1, n // len(self.workers))
        tasks = []
        start = 1

        for i in range(len(self.workers)):
            end = start + chunk_size - 1 if i < len(self.workers) - 1 else n
            tasks.append((start, end))
            start = end + 1

        return tasks

    def find_workers(self) -> set[Pyro4.Proxy]:
        workers = set()
        with Pyro4.locateNS() as ns:
            for _, worker_uri in ns.list(prefix="worker.factorial").items():
                workers.add(Pyro4.Proxy(worker_uri))
        return workers


if __name__ == "__main__":
    m = Master()
