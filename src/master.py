import Pyro4
from typing import List, Optional
import concurrent.futures
import sys
import time

sys.set_int_max_str_digits(0)

sys.excepthook = Pyro4.util.excepthook


class Master:
    def __init__(self):
        self.workers = self.find_workers()
        self.__BASE_CASE = 1

    def calc_factorial(self, n: int) -> int:
        tasks = self.split_factorial(n)
        if not tasks:
            return self.__BASE_CASE
        factorial = 1
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for worker, (start, end) in zip(self.workers, tasks):
                futures.append(executor.submit(worker.compute_factorial, start, end))

            for future in concurrent.futures.as_completed(futures):
                factorial *= future.result()

        return factorial

    def split_factorial(self, n: int) -> Optional[List[tuple[int, int]]]:
        if n < self.__BASE_CASE:
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
    start_time = time.time()
    print(m.calc_factorial(59200))
    end_time = time.time()
    print(f"Factorial Computed after: {end_time - start_time:.2f} seconds")
