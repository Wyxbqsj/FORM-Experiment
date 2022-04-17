import numpy as np
from copy import deepcopy
import time
from setting import *
#from reinforcement import stateValueInit, stateValueSave, assess

from datadeal.problem import ProblemInstance
from dispatch.assign import bigrah_dispatch,random_dispatch,best_dispatch
from experiment.solve import solve
from experiment.package import groupOrders


def solveDP(problem: ProblemInstance, total_round=3000, algorithm_strategy=algorithm, with_G_strategy=with_G):
    currentTime = problem.startTime
    index = 0
    # if algorithm[0] != "r" and algorithm[0] != "b":
    #     stateValueInit()
    last_round_orders = []
    # print(problem.endTime)
    while problem.waitOrder and currentTime < problem.endTime:
        # print(currentTime)
        orders, drivers = problem.batch(currentTime) #得到是每个batch的driver和order
        #import pdb
        #pdb.set_trace()
        orders += last_round_orders
        last_round_orders = []

        # 算法运行
        match, t, transfer_t, id_map, plan = solve(orders=orders, current_time=currentTime,
                                                   last_round_orders=last_round_orders,
                                                   algorithm=algorithm_strategy, with_G=with_G_strategy)
        # match, t, transfer_t, id_map, plan = solve(orders=orders, current_time=currentTime,
        #                                            last_round_orders=last_round_orders,
        #                                            algorithm=1, with_G=True)
        packages = groupOrders(orders, match, transfer_t, plan, id_map)

        if dispatch_algorithm == "random":
            solution = random_dispatch(packages, drivers)
        elif dispatch_algorithm == "best":
            solution = best_dispatch(packages, drivers)
        elif dispatch_algorithm == "bigraph":
            solution = bigrah_dispatch(packages, drivers)
        else:
            solution = bigrah_dispatch(packages, drivers, income=True)
        #else:
            #solution = reinforce(orders, drivers, index)
        for package, driver in solution:
            driver.serve(package, currentTime)
        # if evaluat:e
        #     assess(solution, index)
        currentTime += fragment #一个batch是60s
        index += 1
    # if evaluate:
    #     stateValueSave()


def compareTwoAlgo(problem: ProblemInstance, total_round=3000, algorithms=[1, 2], with_G_strategy=with_G):

    # 实验指标
    overall_measurement = [None, None]
    for i in range(len(overall_measurement)):
        overall_measurement[i] = {
            'size': 0,
            'total_cost_saving': 0,
        }

    # 实验开始
    current_time = problem.startTime
    index=0
    last_round_orders = []
    while problem.waitOrder and current_time<problem.endTime:
        orders, drivers = problem.batch(current_time)
        orders+=last_round_orders
        last_round_orders=[]

        orders_list = [deepcopy(orders), deepcopy(orders)]

        match_compare = [None, None]

        for i in range(2):
            match_compare[i], t, transfer_t, id_map, plan = solve(orders=orders_list[i], current_time=current_time,
                                                                  last_round_orders=last_round_orders,
                                                                  algorithm=algorithms[i], with_G=False)

        match_1 = match_compare[0] # algorithm[0]的match结果
        match_3 = match_compare[1] # algorithm[1]的match结果


        match_tmp = [None, None] # 记录两个算法中不同的match
        for i in range(2):
            match_tmp[i] = [[j] for j in range(len(match_1))]

        different_count = 0
        for i in range(len(match_1)):
            if match_1[i] != match_3[i]:
                match_tmp[0][i] = match_1[i]
                match_tmp[1][i] = match_3[i]
                different_count = different_count + 1

        del match_1, match_3

        for tmp_i in range(2):

            match = match_tmp[tmp_i]
            packages = groupOrders(orders, match, transfer_t, plan, id_map)
            if dispatch_algorithm == "random":
                solution = random_dispatch(packages, drivers)
            elif dispatch_algorithm == "best":
                solution = best_dispatch(packages, drivers)
            elif dispatch_algorithm == "bigraph":
                solution = bigrah_dispatch(packages, drivers)
            else:
                solution = bigrah_dispatch(packages, drivers, income=True)
            # else:
            # solution = reinforce(orders, drivers, index)
            for package, driver in solution:
                driver.serve(package, current_time)
            # if evaluat:e
            #     assess(solution, index)
            current_time += fragment  # 一个batch是60s
            index+=1