import os

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # 读取数据
    ROOT_DIR = os.getcwd()
    TSS_RESULT_PATH = ROOT_DIR + '/data/tss/'
    NEH_RESULT_PATH = ROOT_DIR + '/data/neh/'
    CHE_RESULT_PATH = ROOT_DIR + '/data/che/'

    os.chdir(TSS_RESULT_PATH)
    tss_filenames = os.listdir()

    os.chdir(NEH_RESULT_PATH)
    neh_filenames = os.listdir()

    os.chdir(CHE_RESULT_PATH)
    che_filenames = os.listdir()

    tss_res_dict = {}
    neh_res_dict = {}
    che_res_dict = {}

    tss_time_dict = {}
    neh_time_dict = {}
    che_time_dict = {}

    for filename in tss_filenames:
        filepath = TSS_RESULT_PATH + filename
        with open(filepath, "r", encoding="utf-8") as f:
            order = f.readline()
            res = eval(f.readline())
            time = eval(f.readline())
            tss_res_dict[filename] = res
            tss_time_dict[filename] = time

    for filename in neh_filenames:
        filepath = NEH_RESULT_PATH + filename
        with open(filepath, "r", encoding="utf-8") as f:
            order = f.readline()
            res = eval(f.readline())
            time = eval(f.readline())
            neh_res_dict[filename] = res
            neh_time_dict[filename] = time

    for filename in che_filenames:
        filepath = CHE_RESULT_PATH + filename
        with open(filepath, "r", encoding="utf-8") as f:
            order = f.readline()
            res = eval(f.readline())
            time = eval(f.readline())
            che_res_dict[filename] = res
            che_time_dict[filename] = time

    # 分组绘图, 先画第一张结果比对图
    fig = plt.figure(figsize=(21, 14), dpi=80)
    groups = [10, 30, 50, 100, 200, 500]
    for index, group in enumerate(groups, start=1):
        # 画布分成两行三列，在第index个区域绘画
        ax = plt.subplot(2, 3, index)

        # 获取x轴(文件名字), 两个和y轴(完工时间)
        x_label = []
        y_tss_res = []
        y_neh_res = []
        y_che_res = []
        for filename in tss_filenames:
            if filename.split("_")[0] == str(group):
                x_label.append(filename.split(".")[0])
                y_tss_res.append(tss_res_dict[filename])

        for filename in neh_filenames:
            if filename.split("_")[0] == str(group):
                y_neh_res.append(neh_res_dict[filename])

        for filename in che_filenames:
            if filename.split("_")[0] == str(group):
                y_che_res.append(che_res_dict[filename])

        x = [i for i in range(len(x_label))]

        # 开始绘图
        ax.set_title("%s jobs" % group)
        ax.plot(x, y_tss_res, "bo-", label="tss_res")
        ax.plot(x, y_neh_res, "go-", label="neh_res")
        ax.plot(x, y_che_res, "ro-", label="che_res")

    fig.legend(labels=("tss_res", "neh_res", "che_res"), loc="center")

    # 保存图片
    plt.savefig(ROOT_DIR + "/data/che_tss_neh_res.png", format="png", bbox_inches="tight")
    # plt.show()

    # 分组绘图, 第二张时间对比图
    fig = plt.figure(figsize=(21, 14), dpi=80)
    groups = [10, 30, 50, 100, 200, 500]
    for index, group in enumerate(groups, start=1):
        # 画布分成两行三列，在第index个区域绘画
        ax = plt.subplot(2, 3, index)

        # 获取x轴(文件名字), 两个和y轴(完工时间)
        x_label = []
        y_tss_time = []
        y_neh_time = []
        y_che_time = []
        for filename in tss_filenames:
            if filename.split("_")[0] == str(group):
                x_label.append(filename.split(".")[0])
                y_tss_time.append(tss_time_dict[filename])

        for filename in neh_filenames:
            if filename.split("_")[0] == str(group):
                y_neh_time.append(neh_time_dict[filename])

        for filename in neh_filenames:
            if filename.split("_")[0] == str(group):
                y_che_time.append(che_time_dict[filename])

        x = [i for i in range(len(x_label))]

        # 开始绘图
        ax.set_title("%s jobs" % group)
        ax.plot(x, y_tss_time, "bo--", label="tss_time")
        ax.plot(x, y_neh_time, "go--", label="neh_time")
        ax.plot(x, y_che_time, "ro--", label="che_time")

    fig.legend(labels=("tss_time", "neh_time", "che_time"), loc="center")

    # 保存图片
    plt.savefig(ROOT_DIR + "/data/che_tss_neh_time.png", format="png", bbox_inches="tight")
    # plt.show()
