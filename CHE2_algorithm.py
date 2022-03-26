import os
import random
import sys
import time

import numpy as np


from modele.factory import Factory


class CHE2Factory(Factory):
    """
        CHE2 (Chaos Evolution 2)
        混沌进化法 2
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

        # 随机生成一群个体 (n 个), 用NEH生成初始序列
        jobs_nums = len(self.jobs)

        order, res = self.neh_complete()
        self.orders.append(order)
        self.results.append(res)

        # 破坏重构生成一堆种群
        for i in range(1, 10):
            order, res = self.destroy_and_construct(order, i)
            self.orders.append(order)
            self.results.append(res)

        for epoch in range(10):
            # 对种群进行筛选，去除结果不好的
            group_size = len(self.results)
            if group_size > 10:
                delete_num = group_size - 10
                for _ in range(delete_num):
                    bad_res = max(self.results)
                    idx = self.results.index(bad_res)
                    self.results.pop(idx)
                    self.orders.pop(idx)

            # 破坏重构
            for idx in range(1, len(self.results)):
                temp_order = self.orders[idx]
                for i in range(1, 11):
                    order, res = self.destroy_and_construct(temp_order, i)
                    self.orders.append(order)
                    self.results.append(res)

        # 几个世代结束之后 输出结果
        self.che_res = min(self.results)
        idx = self.results.index(self.che_res)
        self.che_order = self.orders[idx]

        self.che_time = time.time() - start_time

        return self.che_res

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
            min_index = None

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

    def destroy_and_construct(self, order, destroy_num):
        temp = [i for i in order]
        result = None

        # 从队列中取出 destroy_num 个工件，并重新选择地方插入放回
        destroyed_list = []
        for _ in range(destroy_num):
            idx = random.randint(0, len(temp) - 1)
            destroyed_list.append(temp.pop(idx))

        # 重新插入最佳位置
        for job_id in destroyed_list:
            min_res = sys.maxsize
            min_idx = 0

            # 每个工件都有 n 种插法
            for idx in range(len(temp)):
                temp.insert(idx, job_id)
                res = self.complete(temp)

                if res < min_res:
                    min_res = res
                    min_idx = idx

                # 返回原貌
                temp.pop(idx)

            # 放入结果最小的位置
            temp.insert(min_idx, job_id)
            result = min_res

        return temp, result


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
    CHE2_RESULT_PATH = ROOT_DIR + '/data/che2/'
    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)
    if os.path.exists(CHE2_RESULT_PATH) is False:
        os.makedirs(CHE2_RESULT_PATH)

    che_factory = CHE2Factory()

    # 读取数据
    os.chdir(FACTORY_DATA_PATH)
    filenames = os.listdir()
    for filename in filenames:
        che_factory.load_data(FACTORY_DATA_PATH + filename)

        # 计算结果
        che_factory.che_complete()

        # 存储结果
        res_filename = filename.split(".")[0] + '.res'
        che_factory.save_results(CHE2_RESULT_PATH + res_filename)
