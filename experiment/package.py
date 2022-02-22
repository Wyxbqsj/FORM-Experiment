import random
import time
from copy import deepcopy
from copy import deepcopy
from typing import List
import numpy as np
from datadeal.order import Order
from experiment.costSaving import ManhaDrop2Drop,ManhaPick2Drop,ManhaPick2Pick

from tqdm import tqdm

from setting import *
from datadeal.problem import ProblemInstance
from experiment.solve import solve,get_order
from experiment.costSaving import get_original_id_by_mapped, cost_saving, transfer_id_map
import sys

sys.path.append(algorithm_path)
from preference_util import verify_match, fairness_compute

def groupOrders(orders:List[Order], match, transfer_t, plan, id_map):
    packageList=[]
    newId=0
    i=0
    dataline='VTS,2000-1-1 0:00:0,2000-1-1 0:00:0'
    for _ in range(16):
        dataline+=',-1'

    while i<len(match):

        original_indexi=get_original_id_by_mapped(i,id_map)  # 相对ID为i的order的最初的绝对ID
        order_i=get_order(original_indexi,orders) # 找到最初的preference table中的order
        package = Order(dataline)
        if len(match[i])==0: # 由于各种限制，该order在本batch得不到匹配
            package = order_i
            packageList.append(package)
            package.id = newId
            newId += 1
        else:
            partner=match[i][0]
            # print(partner)
            if partner==None:
                i = i + 1
                continue
            original_index_partner=get_original_id_by_mapped(partner,id_map)
            order_partner=get_order(original_index_partner,orders)
            # if partner+1==i: # orders[i]没能匹配上对象，单独打包成一个package
            #     package=order_i
            #     packageList.append(package)
            #     package.id=newId
            #     newId+=1
            # else: #orders[i]匹配上了对象orders[match[i][0]]
            package.id=newId
            newId+=1
            # 获得i和他的partner采用的是哪种plan，并基于此设定package的其他属性
            package.pickTime = max(order_i.pickTime, order_partner.pickTime)  # 两个订单都出现了才能被打包
            package.dropoffTime = max(order_i.dropoffTime, order_partner.dropoffTime)
            package.passengerCount = order_i.passengerCount + order_partner.passengerCount
            package.tripDistance = order_i.tripDistance + order_partner.tripDistance
            package.maxWait = order_i.maxWait
            package.married = True

            partner_rank=find_index(transfer_t,i,partner+1)
            # import pdb
            # pdb.set_trace()
            planNumber=plan[i][partner_rank]

            comDistance=ManhaPick2Pick(order_i,order_partner)+ManhaDrop2Drop(order_i,order_partner)
            if planNumber==1:
                package.pickX=order_i.pickX
                package.pickY=order_i.pickY
                package.dropX=order_partner.dropX
                package.dropY=order_partner.dropY
                package.absluteDistance=ManhaPick2Drop(order_partner,order_i)+comDistance
            elif planNumber==2:
                package.pickX = order_i.pickX
                package.pickY = order_i.pickY
                package.dropX = order_i.dropX
                package.dropY = order_i.dropY
                package.absluteDistance = ManhaPick2Drop(order_partner, order_partner)+comDistance
            elif planNumber==3:
                package.pickX = order_partner.pickX
                package.pickY = order_partner.pickY
                package.dropX = order_partner.dropX
                package.dropY = order_partner.dropY
                package.absluteDistance = ManhaPick2Drop(order_i, order_i)+comDistance
            elif planNumber==4:
                package.pickX = order_partner.pickX
                package.pickY = order_partner.pickY
                package.dropX = order_i.dropX
                package.dropY = order_i.dropY
                package.absluteDistance = ManhaPick2Drop(order_i, order_partner)+comDistance

            package.durable= np.random.randint(200) + 200
            package.deadline= (package.absluteDistance/carSpeed)*1.5+package.durable
            package.totalAmount=order_i.totalAmount+order_partner.totalAmount #打包后的订单，司机服务他会得到的收益
            package.available=True
            package.speed = (order_i.speed+order_partner.speed)/2.0

            packageList.append(package)

            # 将order_i和order_partner打包成一个订单后，将他们的match上的partner都设为空值
            match[i][0]=None
            match[partner][0]=None

        i=i+1
    return packageList

def find_index(transfer_t,i,partner): # 找出partner在transfer_t[i]中的排名
    x=0
    while x<len(transfer_t[i]):
        if transfer_t[i][x]==partner:
            return x
        else:
            x+=1


if __name__ == '__main__':
    batch_gap = 60
    problemInstance = ProblemInstance(data_path, 1000)
    currentTime = problemInstance.startTime + batch_gap*2

    count_list = [0 for i in range(5)]
    empty = 0
    avg_count_len = 0

    debug = False
    count = 1000
    total_different_count = 0
    last_round_orders=[]
    # for round in tqdm(range(count)):
        # 以下是准备阶段
    orders, drivers = problemInstance.batch(currentTime)
    currentTime = currentTime + batch_gap


    match, t, transfer_t, id_map, plan = solve(orders=orders, current_time=currentTime,
                                                   last_round_orders=last_round_orders,
                                                   algorithm=1, with_G=True)
    # for i in match:
    #     if i and i[0]==i:
    #         print(i)
    res=groupOrders(orders,match,transfer_t,plan,id_map)
    #
    print(len(orders),len(match),len(res))
    # for i in match:
    #     print(i)
    count=0
    for i in res:
        if i.married==True:
            count+=2
        else:
            count+=1
    print(count)


    for i in res:
        summary = {'id':i.id,
                   'married': i.married,
                    'pick_time':i.pickTime,
                    'drop_time':i.dropoffTime,
                    'pickX':i.pickX,
                    'pickY':i.pickY,
                    'dropX':i.dropX,
                    'dropY':i.dropY,
                    'tripDistance':i.tripDistance,
                    'deadline':i.deadline,
                    'revenue':i.totalAmount,
                   'speed':i.speed
                       }
        print(summary)




