import os
import sys
import time

import numpy as np

from modele.factory import Factory


class TSSFactory(Factory):
    def __init__(self):
        super().__init__()
        self.tss_time = None
        self.tss_order = None
        self.tss_res = sys.maxsize

    def tss_complete(self):
        """
        Tss 启发式构造方法解决问题
        :return:
        """
        self.clear_results()

        start_time = time.time()

        # 获得所有工件的编号
        jobs_num = len(self.jobs)
        ids = [i for i in range(jobs_num)]

        # 获取一个临时 order
        tmp = []

        # 遍历 jobs_num 次, 每次取出最合适的放入tmp
        i = 0
        while i < jobs_num:

            min_res = sys.maxsize
            min_id = None
            tmp.append(0)
            for job_id in ids:
                tmp[i] = job_id
                res = self.complete(tmp)
                if res < min_res:
                    min_res = res
                    min_id = job_id

            # 每一轮决定一个最小值
            tmp[i] = min_id
            ids.remove(min_id)

            self.tss_order = tmp
            self.tss_res = min_res

            i = i + 1

        self.tss_time = time.time() - start_time

        return self.tss_res

    def clear_results(self):
        self.tss_time = None
        self.tss_order = None
        self.tss_res = sys.maxsize

    def save_results(self, filename):
        # 第一行写入顺序, 第二行写入结果, 第三行写入时间
        results = [self.tss_order, self.tss_res, self.tss_time]
        np.savetxt(filename, results, fmt='%s', delimiter=',')
        print("save results to %s" % filename)


if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    FACTORY_DATA_PATH = ROOT_DIR + '/data/fac/'
    TSS_RESULT_PATH = ROOT_DIR + '/data/tss/'
    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)
    if os.path.exists(TSS_RESULT_PATH) is False:
        os.makedirs(TSS_RESULT_PATH)

    tss_factory = TSSFactory()

    """
    # 生成数据
    jobs_nums = [10, 30, 50, 100, 200, 500]
    machines_num = 10
    for jobs_num in jobs_nums:
        for _ in range(10):
            tss_factory.generate_data(jobs_num, machines_num)
            # 生成文件名字 工件数量-机器数量-时间戳.fac
            timestamp = str(time.time())[-4:]
            filename = "%s_%s_%s.fac" % (jobs_num, machines_num, timestamp)
            tss_factory.save_data(FACTORY_DATA_PATH + filename)
    """

    # 读取数据
    os.chdir(FACTORY_DATA_PATH)
    filenames = os.listdir()
    for filename in filenames:
        tss_factory.load_data(FACTORY_DATA_PATH + filename)

        # 计算结果
        tss_factory.tss_complete()

        # 存储结果
        res_filename = filename.split(".")[0] + '.res'
        tss_factory.save_results(TSS_RESULT_PATH + res_filename)
