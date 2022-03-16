from visualdl import LogWriter

if __name__ == '__main__':
    with LogWriter(logdir='./log/3') as writer:
        with open(file="demo.txt", mode="r", encoding="utf-8") as file:
            step = 0
            for line in file.readlines():
                value = eval(line.strip())
                writer.add_scalar(tag="time", step=step, value=value)
                step = step + 1