import numpy as np
from past.builtins import xrange
from modele.factory import Factory
import os

# # 随机生成job和mac文件
# if __name__ == '__main__':
#     num = 0
#     for i in xrange(3, 13):
#         for j in xrange(3, 13):
#             num = num + 1
#             f_name = str(num) + '.job'
#             m_name = str(num) + '.mac'
#             data = np.random.randint(1, 100, size=(i, j))
#             m_data = np.random.randint(1, 4, size=(1, j))
#             m_data[0][-1] = 0
#             while m_data[0][-2] == 2:
#                 m_data[0][-2] = np.random.randint(0, 4)
#             np.savetxt('./data/job/' + f_name, data, fmt='%d', delimiter=',')
#             np.savetxt('./data/machine/' + m_name, m_data, fmt='%d', delimiter=',')

if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    FACTORY_DATA_PATH = ROOT_DIR + '/data/fac/'

    if os.path.exists(FACTORY_DATA_PATH) is False:
        os.makedirs(FACTORY_DATA_PATH)

    factory = Factory()


    # 生成数据
    jobs_nums = [10, 30, 50, 100, 200]
    machines_num = 5
    for jobs_num in jobs_nums:
        for _ in range(10):
            factory.generate_data(jobs_num, machines_num)
            # 生成文件名字 工件数量-机器数量-时间戳.fac
            timestamp = str(_)
            filename = "%s_%s_%s.fac" % (jobs_num, machines_num, timestamp)
            factory.save_data(FACTORY_DATA_PATH + filename)
