import sys
import os
import time

import numpy as np
from modele.factory import Factory


class NEHFactory(Factory):
    def __init__(self):
        super().__init__()
        self.neh_time = None
        self.neh_order = None
        self.neh_res = sys.maxsize

    def neh_complete(self):
        """
        NEH 启发式构造方法解决问题
        :return: 局部最短完工时间
        """
        self.clear_results()

        start_time = time.time()

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

            self.neh_res = min_res
            self.neh_order = tmp

            i = i + 1

        self.neh_time = time.time() - start_time

        return self.neh_res

    def clear_results(self):
        self.neh_time = None
        self.neh_order = None
        self.neh_res = sys.maxsize

    def save_results(self, filename):
        # 第一行写入顺序, 第二行写入结果, 第三行写入时间
        results = [self.neh_order, self.neh_res, self.neh_time]
        np.savetxt(filename, results, fmt='%s', delimiter=',')
        print("save results to %s" % filename)


if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    FACTORY_DATA_PATH = ROOT_DIR + '/data/fac/'
    NEH_RESULT_PATH = ROOT_DIR + '/data/neh/'
    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)
    if os.path.exists(NEH_RESULT_PATH) is False:
        os.makedirs(NEH_RESULT_PATH)

    neh_factory = NEHFactory()

    # 读取数据
    os.chdir(FACTORY_DATA_PATH)
    filenames = os.listdir()
    for filename in filenames:
        neh_factory.load_data(FACTORY_DATA_PATH + filename)

        # 计算结果
        neh_factory.neh_complete()

        # 存储结果
        res_filename = filename.split(".")[0] + '.res'
        neh_factory.save_results(NEH_RESULT_PATH + res_filename)
