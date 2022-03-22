import os
import random
import sys
import time

import numpy as np

from utils.order import random_order
from modele.factory import Factory


class CHEFactory(Factory):
    """
        CHE (Chaos Evolution)
        混沌进化法
    """
    def __init__(self):
        super().__init__()
        self.orders = []
        self.results = []

        self.che_order = None
        self.che_res = sys.maxsize
        self.che_time = None

    def che_complete(self):
        self.clear_results()

        start_time = time.time()

        # 随机生成一群个体 (n 个)
        jobs_nums = len(self.jobs)
        for _ in range(jobs_nums):
            order = random_order(jobs_nums)
            res = self.complete(order)

            self.orders.append(order)
            self.results.append(res)

        for epoch in range(jobs_nums):
            # 去除一半劣势个体
            len_orders = len(self.orders)
            for _ in range(len_orders // 2):
                r1 = random.randint(0, len(self.results) - 1)
                r2 = random.randint(0, len(self.results) - 1)
                if self.results[r1] < self.results[r2]:
                    self.orders.pop(r2)
                    self.results.pop(r2)
                else:
                    self.orders.pop(r1)
                    self.results.pop(r1)

            # 交叉生成 四分之一个个体 多个方法 取的方法 放的方法
            len_orders = len(self.orders)
            for _ in range(len_orders // 2):
                r1 = random.randint(0, len(self.results) - 1)
                r2 = random.randint(0, len(self.results) - 1)

                # 混合，得到子序列
                order = self.get_mix_order(self.orders[r1], self.orders[r2])

                res = self.complete(order)
                self.orders.append(order)
                self.results.append(res)

            # 随机生成 四分之一个个体
            for _ in range(len_orders // 2):
                order = random_order(jobs_nums)
                res = self.complete(order)

                self.orders.append(order)
                self.results.append(res)

        # 5个世代结束之后 输出结果
        self.che_res = min(self.results)
        idx = self.results.index(self.che_res)
        self.che_order = self.orders[idx]

        self.che_time = time.time() - start_time

        return self.che_res

    def get_mix_order(self, order1, order2):
        lenght = len(order1)
        lst = order1.copy()
        for i in range(lenght):
            lst[order1.index(order2[i])] = i

        order = order1.copy()
        for i in range(lenght // 2):
            idx = random.randint(0, lenght - 1)

            temp = order[lst[idx]]
            order[lst[idx]] = order[idx]
            order[idx] = temp

        return order

    def clear_results(self):
        self.orders = []
        self.results = []

        self.che_order = None
        self.che_res = sys.maxsize
        self.che_time = None

    def save_results(self, filename):
        # 第一行写入顺序, 第二行写入结果, 第三行写入时间
        results = [self.che_order, self.che_res, self.che_time]
        np.savetxt(filename, results, fmt='%s', delimiter=',')
        print("save results to %s" % filename)


if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    FACTORY_DATA_PATH = ROOT_DIR + '/data/fac/'
    TSS_RESULT_PATH = ROOT_DIR + '/data/che/'
    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)
    if os.path.exists(TSS_RESULT_PATH) is False:
        os.makedirs(TSS_RESULT_PATH)

    che_factory = CHEFactory()


    # 读取数据
    os.chdir(FACTORY_DATA_PATH)
    filenames = os.listdir()
    for filename in filenames:
        che_factory.load_data(FACTORY_DATA_PATH + filename)

        # 计算结果
        che_factory.che_complete()

        # 存储结果
        res_filename = filename.split(".")[0] + '.res'
        che_factory.save_results(TSS_RESULT_PATH + res_filename)