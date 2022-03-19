import os

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # 读取数据
    ROOT_DIR = os.getcwd()
    NEH_RESULT_PATH = ROOT_DIR + '/data/neh/'
    os.chdir(NEH_RESULT_PATH)
    filenames = os.listdir()
    res_dict = {}
    time_dict = {}
    for filename in filenames:
        filepath = NEH_RESULT_PATH + filename
        with open(filepath, "r", encoding="utf-8") as f:
            order = f.readline()
            res = eval(f.readline())
            time = eval(f.readline())
            res_dict[filename] = res
            time_dict[filename] = time

    # 分组绘图
    fig = plt.figure(figsize=(21, 14))
    groups = [10, 30, 50, 100, 200, 500]
    for index, group in enumerate(groups, start=1):
        # 画布分成两行三列，在第index个区域绘画
        ax1 = plt.subplot(2, 3, index)

        # 获取x轴(文件名字), 两个和y轴(完工时间， 算法执行时间)
        x_label = []
        y_res = []
        y_time = []
        for filename in filenames:
            if filename.split("_")[0] == str(group):
                x_label.append(filename.split(".")[0])
                y_res.append(res_dict[filename])
                y_time.append(time_dict[filename])
        x = [i for i in range(len(x_label))]

        # 开始绘图
        ax1.set_title("%s jobs" % group)
        ax1.plot(x, y_res, "bo-", label="neh_res")
        ax1.set_ylabel("neh_res")

        ax2 = ax1.twinx()
        ax2.plot(x, y_time, "go--", label="neh_time")
        ax2.set_ylabel("neh_time")

    fig.legend(labels=("neh_res", "neh_time"), loc="center")

    # 保存图片
    plt.savefig(ROOT_DIR + "/data/neh_res.png", format="png", bbox_inches="tight")
    plt.show()
