# 生成tss结果和res（暴力破解）结果的比较图
from visualdl import LogWriter

if __name__ == '__main__':
    with LogWriter(logdir='./log/tss-res/tss') as writer:
        tss_path = './data/tss-res/'
        for i in range(1, 101):
            tss_file = tss_path + str(i) + '.tssres'
            with open(tss_file, mode='r', encoding='utf-8') as r:
                val = eval(r.readline().strip())
                writer.add_scalar(tag="tss-res", step=i, value=val)
    with LogWriter(logdir='./log/tss-res/res') as writer:
        res_path = './data/res/'
        for i in range(1, 101):
            res_file = res_path + str(i) + '.res'
            with open(res_file, mode='r', encoding='utf-8') as r:
                val = eval(r.readline().strip())
                writer.add_scalar(tag="tss-res", step=i, value=val)

# 查看结果的方法
# visualdl --logdir ./log/tss-res --port 8080