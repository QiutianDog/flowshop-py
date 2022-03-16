import numpy as np
from past.builtins import xrange
# 随机生成job和mac文件
if __name__ == '__main__':
    num = 0
    for i in xrange(3, 13):
        for j in xrange(3, 13):
            num = num + 1
            f_name = str(num) + '.job'
            m_name = str(num) + '.mac'
            data = np.random.randint(1, 100, size=(i, j))
            m_data = np.random.randint(1, 4, size=(1, j))
            m_data[0][-1] = 0
            while m_data[0][-2] == 2:
                m_data[0][-2] = np.random.randint(0, 4)
            np.savetxt('./data/job/' + f_name, data, fmt='%d', delimiter=',')
            np.savetxt('./data/machine/' + m_name, m_data, fmt='%d', delimiter=',')