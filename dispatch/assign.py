import time

import numpy as np
from scipy.optimize import linear_sum_assignment
from setting import *



np.random.seed(seed)

#返回每个driver和order他们match到一起的reward
def match(orders: list, drivers: list, income=False):
    ordersRewards = np.zeros((len(drivers), len(orders))) - 10 #行是driver, 列是order
    if len(orders) == 0 or len(drivers) == 0: return ordersRewards
    driversLocation = np.array([[driver.x, driver.y] for driver in drivers])
    ordersLocation = np.array([[order.pickX, order.pickY] for order in orders]).T #注意.T(矩阵转置)
    if income == False:
        ordersReward = np.ones(len(orders)) #如果没有income,就将reward设置为1
    else:
        ordersReward = np.array([order.totalAmount for order in orders]) #如果有income,那就是order的totalAmount作为reward
    ordersSpeed = np.array([order.speed for order in orders])
    available = np.sum(np.abs(driversLocation[:,:,None] - ordersLocation[None,:,:]), axis=1) #任意一个order和driver之间的曼哈顿距离
    available = (available[:,] / ordersSpeed) > takeTime #复用了available，此后available是布尔变量
    ordersRewards[:,] = ordersReward #取每一行，给列上填充order的orderReward
    ordersRewards[available] = -10  #如果不能在规定时间内接到order（available为真），则reward为-10
    return ordersRewards




# def reinforce(orders: list, drivers: list, index):
#     available = -np.array(match(orders, drivers, index=index))
#     row_ind, col_ind = linear_sum_assignment(available)
#     res = []
#     for i, j in zip(row_ind, col_ind):
#         if available[i][j] != 0:
#             res.append((orders[j], drivers[i]))
#     return res




def bigrah_dispatch(orders: list, drivers: list, income: bool=False):
    available = -np.array(match(orders, drivers, income))
    row_ind, col_ind = linear_sum_assignment(available)
    res = []
    for i, j in zip(row_ind, col_ind):
        if available[i][j] != 0:
            res.append((orders[j], drivers[i]))
    return res

def random_dispatch(orders: list, drivers: list):
    np.random.shuffle(orders) #np.random.shuffle(X),只第一维度进行随机打乱，体现在训练好像就是就是打乱每个样本的顺序，经常在epoch之后使用，充分打乱数据这样可以增加训练的多样性
    np.random.shuffle(drivers)
    available = match(orders, drivers)
    res = []
    for i in range(len(drivers)):
        r = np.argwhere(available[i] == 1)
        if len(r) == 0: continue
        j = r[0][0]
        res.append((orders[j], drivers[i]))
        available[:, j] = 0
    return res



def best_dispatch(orders: list, drivers: list):
    orders.sort(key=lambda x: x.totalAmount)
    for order in orders:
        order.speed = 0
    np.random.shuffle(drivers)
    return list(zip(orders, drivers))