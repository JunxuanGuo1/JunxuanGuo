import json
import time
import requests
import random
import pandas as pd
import pymysql
# 设置随机User-Agent
headers={
            'Accept':'application/json,text/javascript,*/*; q=0.01',
            'Accept-Encoding':'gzip,deflate',
            'Connection':'keep-alive',
            'Host':'gs.amac.org.cn',
            'Content-Type':'application/json;charset=UTF-8',
            'Origin':'http://gs.amac.org.cn',
            'X-Requested-With':'XMLHttpRequest',
            'Referer':'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36'
            }
result=[]
for i in range(0,10):
    print('正在爬取第{}页'.format(i+1))
    r=random.random
    url='https://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand='+str(r)+'&page='+str(i)+'&size=20'
    data={'keyword':'中信银行股份有限公司'}
    data=json.dumps(data)
    response = requests.post(url = url,data=data ,headers =headers )
    # print(response.status_code)
    # print(response.text)
    time.sleep(0.5)
    datas=json.loads(response.text)["content"]
    # print(datas)
    alldata={}
    for data1 in datas:
        alldata = []
        #基金名称
        fundName=data1['fundName']
        #私募基金管理人名称
        managerName=data1['managerName']
        #托管人名称
        mandatorName=data1['mandatorName']
        # 成立时间
        putOnRecordDate=data1['establishDate']
        # 备案时间
        workingState=data1['putOnRecordDate']
        alldata.append(fundName)
        alldata.append(managerName)
        alldata.append(mandatorName)
        alldata.append(putOnRecordDate)
        alldata.append(workingState)
        result.append(alldata)
df=pd.DataFrame(result, columns=['基金名称', '私募基金管理人名称', '托管人名称', '成立时间', '备案时间'])

df['托管人名称']=df['托管人名称'].str.replace('<em>', '').str.replace('</em>', '')
df['托管人名称'] = df['托管人名称'].str.replace('中信银行股份', '中信银行')
df1=df[df['私募基金管理人名称'].str.contains('有限合伙')]
# pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
df1.to_excel('./shimujijin.xlsx',index=False)
print(df1)


# MySQL数据库连接配置
host = '127.0.0.1'  # 主机名
port = 3306  # 端口号
user = 'bit'  # 用户名
password = '123456'  # 密码
database = 'bigdata'  # 数据库名

connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
cursor = connection.cursor()

# 写入数据到MySQL表
for row in df1.itertuples(index=False):
    sql = "INSERT INTO zijin (fundName,managerName,mandatorName,establishDate,putOnRecordDate) VALUES (%s, %s, %s, %s, %s)"
    values = (row.fundName, row.managerName, row.mandatorName, row.establishDate, row.putOnRecordDate)
    cursor.execute(sql, values)

# 提交事务并关闭连接
connection.commit()
cursor.close()
connection.close()











