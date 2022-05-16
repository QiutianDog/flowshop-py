from modele.factory import Factory

if __name__ == '__main__':
    '''
       0 WB 没有约束
       1 RCB 工件在下一台机器上离开时释放当前机器
       2 RSB 工件在下一台机器上开始加工时释放当前机器
       3 RCBn 工件在下一台机器上完成加工时释放当前机器
    '''
    factory = Factory()
    # factory.generate_data(5, 5)
    # 读取数据
    factory.load_data('temp.txt')

    # 设置工件序列
    order = [1, 2, 0]
    res = factory.complete(order)
    factory.show_gantt()
    print(res)
