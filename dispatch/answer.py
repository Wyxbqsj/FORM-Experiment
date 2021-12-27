import numpy as np

import time
from setting import *
#from reinforcement import stateValueInit, stateValueSave, assess

from datadeal.problem import ProblemInstance
from dispatch.assign import bigrah_dispatch,random_dispatch,best_dispatch


def solve(problem: ProblemInstance):
    currentTime = problem.startTime
    index = 0
    # if algorithm[0] != "r" and algorithm[0] != "b":
    #     stateValueInit()
    while problem.waitOrder and currentTime < problem.endTime:
        orders, drivers = problem.batch(currentTime) #得到是每个batch的driver和order
        #import pdb
        #pdb.set_trace()
        if algorithm == "random":
            solution = random_dispatch(orders, drivers)
        elif algorithm == "best":
            solution = best_dispatch(orders, drivers)
        elif algorithm == "bigraph":
            solution = bigrah_dispatch(orders, drivers)
        else:
            solution = bigrah_dispatch(orders, drivers, income=True)
        #else:
            #solution = reinforce(orders, drivers, index)
        for order, driver in solution:
            driver.serve(order, currentTime)
        # if evaluate:
        #     assess(solution, index)
        currentTime += fragment #一个batch是60s
        index += 1
    # if evaluate:
    #     stateValueSave()