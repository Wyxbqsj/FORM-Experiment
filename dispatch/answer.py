import numpy as np

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
        print(currentTime)
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