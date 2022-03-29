import os
import sys
import time
import numpy as np
from modele.factory import Factory
import random


class GeneticFactory(Factory):
    def __init__(self, cross_probability=0.7, mutations_probability=0.1):
        super().__init__()
        # 遗传种群
        self.orders = []
        self.orders_mid = []
        self.orders_end = []
        # 遗传种群的解
        self.results = []
        self.results_mid = []
        self.results_end = []
        # 交叉概率
        self.cross_probability = cross_probability
        # 变异概率
        self.mutations_probability = mutations_probability
        # 最终结果
        self.genetic_order = None
        self.genetic_result = None
        self.genetic_time = None

    def genetic_complete(self, epochs=50):
        self.clear_results()
        start_time = time.time()

        # 随机生成 n 个（工件数量）初始个体 作为初始种群
        job_num = len(self.jobs)
        self.generate_orders(job_num, job_num)
        # 从小到大排序
        self.__synchronous_sort(self.orders, self.results, False)

        for epoch in range(epochs):

            for _ in range(job_num):
                # 交叉
                if self.__try_trigger(self.cross_probability) is True:
                    # 从orders中随机选取两个序列
                    orders_num = len(self.results)
                    indexs = [idx for idx in range(orders_num)]
                    weights = [(orders_num - idx) / orders_num for idx in range(orders_num)]
                    idx1, idx2 = random.choices(indexs, weights, k=2)
                    while idx1 == idx2:
                        idx1, idx2 = random.choices(indexs, weights, k=2)
                    child_order1, child_order2 = self.cross_order(self.orders[idx1], self.orders[idx2])

                    # 把新的结果添加到中间群落里
                    res1 = self.complete(child_order1)
                    res2 = self.complete(child_order2)
                    self.orders_mid.append(child_order1)
                    self.orders_mid.append(child_order2)
                    self.results_mid.append(res1)
                    self.results_mid.append(res2)

                # 变异
                if self.__try_trigger(self.mutations_probability) is True:
                    # 从orders中随机选取一个序列
                    orders_num = len(self.results)
                    indexs = [idx for idx in range(orders_num)]
                    weights = [1 / idx for idx in range(1, orders_num + 1)]
                    idx = random.choices(indexs, weights)[0]
                    mut_order = self.mutations_order(self.orders[idx])
                    res = self.complete(mut_order)
                    self.orders_mid.append(mut_order)
                    self.results_mid.append(res)

            # 计算 result 和 mid result中的序列完工时间，进行排序，取前job_num个作为新的种群，清空 mid
            # 把结果全放到mid中进行计算
            orders_num = len(self.orders)
            for i in range(orders_num):
                self.orders_mid.append(self.orders[i])
                self.results_mid.append(self.results[i])
            # 对mid进行排序
            self.__synchronous_sort(self.orders_mid, self.results_mid)
            # 取前面orders_num个放回
            for i in range(orders_num):
                self.orders[i] = self.orders_mid[i]
                self.results[i] = self.results_mid[i]
            # 清空 mid
            self.orders_mid = []
            self.results_mid = []

            # 将最优结果存入end中
            self.orders_end.append(self.orders[0])
            self.results_end.append(self.results[0])

        # 50个epoch完成后 从end中筛选出最小的
        min_res = min(self.results_end)
        index = self.results_end.index(min_res)
        self.genetic_order = self.orders_end[index]
        self.genetic_result = self.results_end[index]
        self.genetic_time = time.time() - start_time
        print(self.results_end)

    def mutations_order(self, order):
        """
        变异，随机取两个位置进行交换
        :param order: 原序列
        :return: 变异后的序列
        """
        length = len(order)
        l = random.randint(0, length - 1)
        r = random.randint(0, length - 1)
        while l == r:
            r = random.randint(0, length - 1)
        mut_order = [item for item in order]
        mut_order[l], mut_order[r] = mut_order[r], mut_order[l]
        return mut_order

    def cross_order(self, order1, order2):
        """
        交叉两个序列，并且产生新的序列
        :param order1: 父序列 1
        :param order2: 父序列 2
        :return: 新的两个子序列
        """
        length = len(order1)
        # 初始化子序列
        child_order1 = [-1 for _ in range(length)]
        child_order2 = [-1 for _ in range(length)]

        def get_cut(order_len):
            l = random.randint(0, order_len)
            r = random.randint(0, order_len)
            while l == r:
                r = random.randint(0, order_len)
            if l > r:
                l, r = r, l
            return [l, r]

        # 选择第一个序列的截取段
        cut_1 = get_cut(length)
        # 选择第二个序列的截图段
        cut_2 = get_cut(length)

        # 将序列1的截取段放到子序列2中
        for i in range(cut_1[0], cut_1[1]):
            child_order2[i] = order1[i]
        # 将序列2的截取段放到子序列1中
        for i in range(cut_2[0], cut_2[1]):
            child_order1[i] = order2[i]

        def put_other(father_order, child_order, cut):
            cut_item = [child_order[idx] for idx in range(cut[0], cut[1])]
            i, j = 0, 0
            length = len(father_order)
            while i < length:
                if cut_item.__contains__(father_order[i]) is True:
                    i = i + 1
                    continue

                if j == cut[0]:
                    j = cut[1]
                    continue

                child_order[j] = father_order[i]
                i = i + 1
                j = j + 1

        # 将序列的其他元素放入子序列当中
        put_other(order1, child_order1, cut_2)
        put_other(order2, child_order2, cut_1)
        return child_order1, child_order2

    def generate_orders(self, job_num, generate_num):
        """
        随机生成generate_num个序列 添加到种群中
        :param job_num: 序列长度，等同于工件数量
        :param generate_num: 序列个数
        """
        n = 0
        while n < generate_num - 1:
            order = [i for i in range(job_num)]
            random.shuffle(order)
            result = self.complete(order)
            self.orders.append(order)
            self.results.append(result)
            n = n + 1
        order, result = self.neh_complete()
        self.orders.append(order)
        self.results.append(result)

    def __synchronous_sort(self, orders, results, reverse=False):
        """
        对self.orders和self.results进行同步排序，以self.results为准，从小到大排序
        :param reverse: 是否翻转
        """
        # 简单冒泡排序
        length = len(results)
        n = 0
        while n < length:
            i = 1
            while i < len(results):
                if results[i - 1] > results[i]:
                    results[i - 1], results[i] = results[i], results[i - 1]
                    orders[i - 1], orders[i] = orders[i], orders[i - 1]
                i = i + 1
            n = n + 1

        if reverse is True:
            self.results.reverse()
            self.orders.reverse()

    def clear_results(self):
        self.orders = []
        self.orders_mid = []
        self.orders_end = []
        self.results = []
        self.results_mid = []
        self.results_end = []
        self.genetic_order = None
        self.genetic_result = None
        self.genetic_time = None

    def __try_trigger(self, probability):
        """
        尝试触发, 触发成功概率为 probability, 如果成功触发 返回True，否则False
        :param probability: 触发成功概率
        :return: 结果
        """
        return True if probability > random.random() else False

    def save_results(self, filename):
        # 第一行写入顺序, 第二行写入结果, 第三行写入时间
        results = [self.genetic_order, self.genetic_result, self.genetic_time]
        np.savetxt(filename, results, fmt='%s', delimiter=',')
        print("save results to %s" % filename)

    def neh_complete(self):
        order = []
        result = None

        # 根据总加工时间降序排列
        temp_jobs = [job for job in self.jobs]
        temp_jobs.sort(key=lambda x: sum(x.work_times), reverse=True)

        # 获得所有工件 id
        jobs_num = len(self.jobs)
        ids = [job.id for job in temp_jobs]

        # 获取一个临时的 order
        tmp = [ids[0]]

        i = 1
        while i < jobs_num:
            min_res = sys.maxsize
            min_index = 0

            for idx in range(i + 1):
                # 插入对应位置
                tmp.insert(idx, ids[i])
                # 计算结果
                res = self.complete(tmp)
                if res < min_res:
                    min_res = res
                    min_index = idx

                # 回溯到原本状态
                tmp.pop(idx)

            # 每轮决定一个结果最小的插入位置，插入工件
            tmp.insert(min_index, ids[i])

            order = tmp
            result = min_res

            i = i + 1

        return order, result


if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    FACTORY_DATA_PATH = ROOT_DIR + '/data/fac/'
    GA_RESULT_PATH = ROOT_DIR + '/data/ga/'
    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)
    if os.path.exists(GA_RESULT_PATH) is False:
        os.makedirs(GA_RESULT_PATH)

    genetic_factory = GeneticFactory()

    # 读取数据
    os.chdir(FACTORY_DATA_PATH)
    filenames = os.listdir()
    for filename in filenames:
        genetic_factory.load_data(FACTORY_DATA_PATH + filename)

        # 计算结果
        genetic_factory.genetic_complete(epochs=500)

        # 存储结果
        res_filename = filename.split(".")[0] + '.res'
        genetic_factory.save_results(GA_RESULT_PATH + res_filename)
