import Pyro4
from typing import List, Optional
import concurrent.futures
import sys
import time

sys.set_int_max_str_digits(0)

sys.excepthook = Pyro4.util.excepthook


class Master:
    def __init__(self):
        self.worker_uris = self.find_worker_uris()
        self.__BASE_CASE = 1

    def calc_factorial(self, n: int) -> int:
        tasks = self.split_factorial(n)
        if not tasks:
            return self.__BASE_CASE
        factorial = 1
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for worker_uri, (start, end) in zip(self.worker_uris, tasks):
                with Pyro4.Proxy(worker_uri) as worker:
                    futures.append(executor.submit(worker.compute_factorial, start, end))

            for future in concurrent.futures.as_completed(futures):
                factorial *= future.result()

        return factorial

    def split_factorial(self, n: int) -> Optional[List[tuple[int, int]]]:
        if n < self.__BASE_CASE:
            return
        chunk_size = max(1, n // len(self.worker_uris))
        tasks = []
        start = 1

        for i in range(len(self.worker_uris)):
            end = start + chunk_size - 1 if i < len(self.worker_uris) - 1 else n
            tasks.append((start, end))
            start = end + 1

        return tasks

    def find_worker_uris(self) -> set[str]:
        worker_uris = set()
        with Pyro4.locateNS() as ns:
            for _, worker_uri in ns.list(prefix="worker.factorial").items():
                worker_uris.add(worker_uri)
        return worker_uris


if __name__ == "__main__":
    m = Master()
    start_time = time.time()
    print(m.calc_factorial(59200))
    end_time = time.time()
    print(f"Factorial Computed after: {end_time - start_time:.2f} seconds")
