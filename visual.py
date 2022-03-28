import os
import matplotlib.pyplot as plt


def load_result_data(root_path, filename):
    result_dict = {}
    time_dice = {}
    result_dir = os.path.join(root_path, "data", filename)

    filenames = os.listdir(result_dir)
    for filename in filenames:
        file_path = os.path.join(result_dir, filename)
        with open(file_path, "r", encoding="utf8") as f:
            order = f.readline().strip()
            result = f.readline().strip()
            time = f.readline().strip()
            filename_prefix = filename.split(".")[0]
            result_dict[filename_prefix] = result
            time_dice[filename_prefix] = time

    return result_dict, time_dice


def draw_result(result_list, label_list, draw_type, save_dir, save_results=False):
    # 构建画布
    fig = plt.figure(figsize=(21, 14))
    for result_dict, name in zip(result_list, label_list):
        groups = [10, 30, 50, 100, 200, 500]
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        for index, group in enumerate(groups, start=1):
            # 分割画布
            ax = plt.subplot(2, 3, index)
            ax.set_title("%s jobs" % group)

            y = []
            keys = result_dict.keys()
            for key in keys:
                if key.split("_")[0] == str(group):
                    y.append(eval(result_dict[key]))
            x = [i for i in range(len(y))]

            ax.plot(x, y, colors[label_list.index(name) % 7] + "o-", label=name+"_"+draw_type)

    fig.legend(labels=label_list, loc="center")

    if save_results is True:
        if save_dir is None:
            print("save_dir is None")
        else:
            filename = ""
            for name in label_list:
                filename = filename + name + "_"
            save_path = os.path.join(save_dir, filename + draw_type + ".png")
            plt.savefig(save_path, format="png", bbox_inches="tight")
            print("sava in " + save_path)


if __name__ == '__main__':
    ROOT_DIR = os.getcwd()

    # 获取数据
    label_list = ['neh', 'ga', 'che2']
    result_list = []
    time_list = []
    for label in label_list:
        result_dict, time_dict = load_result_data(ROOT_DIR, label)
        result_list.append(result_dict)
        time_list.append(time_dict)

    # 绘图
    draw_result(result_list, label_list, "res", ROOT_DIR + "/data/", save_results=True)
    draw_result(time_list, label_list, "time", ROOT_DIR + "/data/", save_results=True)
