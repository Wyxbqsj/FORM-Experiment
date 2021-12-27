# FORM-Experiment
FORM related experiment
项目结构略有些混乱
### datadeal：数据处理+一些实体类
data_deal.py: 读取csv文件中的order，并将一个月的数据分割成31天
<br>clear_data.py: 清洗数据，删除一些噪声数据
<br>driver.py: 司机类
<br>order.py: 乘客类
<br>problem.py: 问题实例

### experiment:乘客匹配
costSaving.py: 构造preference table
<br>gas.py: state-of-the-art passenger matching algorithm
<br>slove.py: 用设计的算法匹配乘客
<br>myResults.py:静态模型下，乘客匹配的结果
<br>package.py: 将匹配上的乘客打包成一个order

### dispatch: 匹配司机和打包好的乘客
<br>assign.py: 三个常见的order dispatch的方法
<br>answer.py: 匹配司机和乘客
<br>finalResult.py: 司乘匹配收益结果
