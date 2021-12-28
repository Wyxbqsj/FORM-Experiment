import time
from datetime import datetime

from setting import *
from datadeal.problem import ProblemInstance
from dispatch.answer import solveDP
from tqdm import tqdm
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
        count += 1
        totalAmount += order.totalAmount
        serveTime += order.dropoffTime - order.pickTime
    d = datetime.now()

    target_folder = "D:/FORMnew/FORM-Experiment/result/%02d" % month # 第一个"%"后面的内容为显示的格式说明,第二个"%"后面为显示的内容来源
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    with open(os.path.join(target_folder,
                           "%s_%s_%d_%d_%d_%s.txt" % (algorithm, dispatch_algorithm, month, day, fragment, d.strftime("%d-%H-%M"))),
                           "w", encoding="utf8") as f:
        f.write("execute:%f  count:%d  time:%f  income:%f" % (t2-t1, count, serveTime, totalAmount))

if __name__ == '__main__':
    main()