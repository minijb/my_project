import csv

values = []
with open("D:\list\Drilled_Holes.csv", 'r', encoding='GBK') as fp:
    reader = csv.reader(fp)
    index = 0
    for i, x in enumerate(reader):
        if i != 0:
            if x[0] != '':
                values.append([x[0], x[2], x[3], x[4], x[5]])
            else:
                values.append([x[1], x[2], x[3], x[4], x[5]])

print(values)
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# from get_headers import get_classfy_1, get_public_headers


engine = create_engine('mysql+pymysql://root:123123@localhost/total_data', pool_size=100)
# 定义模型类继承的父类及数据连接会话
metadata = MetaData(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
md = MetaData(bind=engine)
md = MetaData(bind=engine)



def get_data_ture(f):
    values = []
    try:
        prox = engine.execute('select id,expdivleg,site,hole from sediment_tbl_2 where %s' % f)
        for result in prox:

            cur = dict()
            for k, v in result.items():
                cur[k] = str(v)
            values.append(cur)
    except:
        values = []

    return values

def set_data(id,latitude,longitude):
    sql='UPDATE sediment_tbl_2 SET new_latitude= "%s",new_longitude="%s" where id= "%s"'%(latitude,longitude,id)
    print(sql)
    prox = engine.execute(sql)
    return
def m():
    sqls = []
    datas = []
    for i in values:
        print(i)
        if i[2] != '':
            sql = 'expdivleg="' + i[0] + '" and site="' + i[1] + '" and hole = "' + i[2] + '"'
        else:
            sql = 'expdivleg="' + i[0] + '" and site="' + i[1] + '" and hole = "*"'

        sqls.append(sql)
    print(len(sqls))
    for index,sql in enumerate(sqls):
        print(sql)
        results = get_data_ture(sql)
        if len(results)>=1:
            print(results)
            if len(results)>=2:
                print('!______id  '+str(index))
            for result in results:
                print([index,result['id']])
                datas.append([index,result['id']])
        else:
            print('error')
            print(results)
            print('---------')

    print(datas)
    for i in datas:
        set_data(i[1],values[i[0]][-2],values[i[0]][-1])
    # for i in datas:





session.close()
if __name__ == '__main__':
    m()
