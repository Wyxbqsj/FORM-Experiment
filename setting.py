# 数据配置
month = 7
day = 7
data_dir_path = "D:/ExperimentData/"
data_path = data_dir_path + "raw_data//%02d/clear%d.csv" % (month, day)

# 算法路径
algorithm_path = r'D:\FORM\FORM-Implement-master'

# 车辆速度
carSpeed=0.0001 #每秒移动的经纬度,大约是66km/h

# 超参数
fragment = 120
base_wait_time = 60
wait_time_noise = 10


# 算法
total_round = 100
algorithm = 1
with_G = False


# 算法
dispatch_algorithm = "random"

bigDistance = 0.01271 * 3

# 随机种子
seed = 71437

# 司机数量
driverCount = 4000

#
takeTime = 60 * 3

# 区域分割
regionx = 10
regiony = 10


XREGION = (-74.01, -73.93)
YREGION = (40.70, 40.92)


NUM_GRID_X = 10
NUM_GRID_Y = 10




