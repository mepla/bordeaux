import threading
import time
import random
from multiprocessing.pool import ThreadPool


class Searcher1():
    def search(self):
        item_count = 10
        tp = ThreadPool(processes=2)
        for i in range(item_count):
            tp.apply_async(self.do, (i,), callback=self.callback_res)

        tp.close()
        tp.join()

    def do(self, x):
        time.sleep(random.random())
        return 'S1 number {}'.format(x)

    def callback_res(self, res):
        print res


class Searcher2():
    def search(self):
        item_count = 15
        tp = ThreadPool(processes=2)
        for i in range(item_count):
            tp.apply_async(self.do, (i,), callback=self.callback_res)

        tp.close()
        tp.join()

    def do(self, x):
        time.sleep(random.random())
        return 'S2 number {}'.format(x)

    def callback_res(self, res):
        print res

if __name__ == '__main__':
    s1 = Searcher1()
    s2 = Searcher2()

    t1 = threading.Thread(target=s1.search)
    t2 = threading.Thread(target=s2.search)

    t1.start()
    t2.start()
