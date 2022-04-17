import time
from datetime import datetime
from copy import deepcopy

from setting import *
from datadeal.problem import ProblemInstance
from dispatch.answer import solveDP
from tqdm import tqdm
from experiment.solve import solve
from experiment.package import groupOrders2
from dispatch.assign import bigrah_dispatch,random_dispatch,best_dispatch
import os

def main():

    problem = ProblemInstance(data_path, driverCount)
    t1 = time.time()
    print(2)
    solveDP(problem)
    print(3)
    t2 = time.time()
    serveredOrder = []
    print(1)
    for driver in tqdm(problem.drivers):
        serveredOrder.extend(driver.severedOrder)

    count = 0
    totalAmount = 0
    serveTime = 0
    for order in tqdm(serveredOrder):
        if order.married==True:
            count+=2
        else:
            count += 1
        totalAmount += order.totalAmount
        serveTime += order.dropoffTime - order.pickTime
    d = datetime.now()

    target_folder = "D:/FORMnew/FORM-Experiment/result/%02d" % month # 第一个"%"后面的内容为显示的格式说明,第二个"%"后面为显示的内容来源
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    with open(os.path.join(target_folder,
                           "%s_%s_%d_%d_%d_%d_%s_%s.txt" % (algorithm, dispatch_algorithm, month, day, driverCount, fragment, d.strftime("%d-%H-%M"),with_G)),
                           "w", encoding="utf8") as f:
        f.write("execute:%f  count:%d  time:%f  income:%f" % (t2-t1, count, serveTime, totalAmount))


def compareTwoAlgo(total_round=1000, algorithms=[1, 2]):
    problem = ProblemInstance(data_path, 100000)

    skip_bug = True

    # 实验指标
    overall_measurement = [None, None]
    for i in range(len(overall_measurement)):
        overall_measurement[i] = { # 记录一天数据跑出来的结果
            'size': 0,
            'total_cost_saving': 0,
            'count': 0,
            'profit': 0,
            'serveTime': 0
        }

    # 实验开始
    current_time = problem.startTime
    last_round_orders = []
    while problem.waitOrder and current_time<problem.endTime:

        measurement = [None, None]
        for i in range(len(measurement)): # measurement 记录每一个round的结果
            measurement[i] = {
                'size': 0,
                'total_cost_saving': 0,
                'count': 0,
                'profit': 0,
                'serveTime': 0
            }

        orders, drivers = problem.batch(current_time)
        orders+=last_round_orders
        last_round_orders=[]

        orders_list = [deepcopy(orders), deepcopy(orders)]
        drivers_list=[deepcopy(drivers),deepcopy(drivers)]

        match_compare = [None, None]

        for i in range(2):
            match_compare[i], t, transfer_t, id_map, plan = solve(orders=orders_list[i], current_time=current_time,
                                                                  last_round_orders=last_round_orders,
                                                                  algorithm=algorithms[i], with_G=False)

        match_1 = match_compare[0] # algorithm[0]的match结果
        match_3 = match_compare[1] # algorithm[1]的match结果


        match_tmp = [None, None]
        for i in range(2):
            match_tmp[i] = [[j] for j in range(len(match_1))]

        different_count = 0
        for i in range(len(match_1)):
            if match_1[i] != match_3[i]:
                print(i)
                match_tmp[0][i] = match_1[i]
                match_tmp[1][i] = match_3[i]
                different_count = different_count + 1

        del match_1, match_3

        for tmp_i in range(2):

            match = match_tmp[tmp_i]
            packages = groupOrders2(orders, match, transfer_t, plan, id_map)
            if dispatch_algorithm == "random":
                solution = random_dispatch(packages, drivers_list[tmp_i])
            elif dispatch_algorithm == "best":
                solution = best_dispatch(packages, drivers_list[tmp_i])
            elif dispatch_algorithm == "bigraph":
                solution = bigrah_dispatch(packages, drivers_list[tmp_i])
            else:
                solution = bigrah_dispatch(packages, drivers_list[tmp_i], income=True)

            for package, driver in solution:
                driver.serve(package, current_time)

            current_time += fragment  # 一个batch是60s

            serveredOrder = [[],[]]
            print("here")
            for driver in tqdm(drivers_list[tmp_i]):
                serveredOrder[tmp_i].extend(driver.severedOrder)

            measurement[tmp_i]['size'] = different_count

            overall_measurement[tmp_i]['size'] += measurement[tmp_i]['size']
           # overall_measurement[tmp_i]['total_cost_saving'] += measurement[tmp_i]['total_cost_saving']

            count = 0
            totalAmount = 0
            serveTime = 0
            for order in tqdm(serveredOrder[tmp_i]):
                if order.married == True:
                    count += 2
                else:
                    count += 1
                totalAmount += order.totalAmount
                serveTime += order.dropoffTime - order.pickTime
            overall_measurement[tmp_i]['count']+=count
            overall_measurement[tmp_i]['profit']+=totalAmount
            overall_measurement[tmp_i]['serveTime']+=serveTime

    print(overall_measurement[0])
    print(overall_measurement[1])




if __name__ == '__main__':
    compareTwoAlgo()