from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session



engine = create_engine('mysql+pymysql://root:123123@localhost/total_data', pool_size=100)
# 定义模型类继承的父类及数据连接会话
metadata = MetaData(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
md = MetaData(bind=engine)


session.close()
import threading
import time
def get_data_ture():

    values = []
    try:
        prox = engine.execute('select id,bivalve,topOffsetCm from sediment_tbl ' )
        for result in prox:

            cur = dict()
            for k, v in result.items():
                # if (k in headers or k == 'id'or k =='new_latitude' or k=='new_longitude') :
                    # if k =='new_latitude':
                    #     cur['latitude']=str(v)
                    # elif k =='new_longitude':
                    #     cur['longitude'] = str(v)
                    # elif k!='latitude' and k!='longitude':
                if v==None:
                    v= 'null'
                cur[k] = str(v)
            values.append(cur)
    except:
        values = []



    if values != []:

        for i in values:
            sql = 'UPDATE sediment_tbl_1 SET bivalve= %s,topOffsetCm=%s where id= "%s"' % (i['bivalve'], i['topOffsetCm'], i['id'])

            try:
                prox = engine.execute(sql)
            except:
                sql = 'UPDATE sediment_tbl_1 SET bivalve= "%s",topOffsetCm="%s" where id= "%s"' % (i['bivalve'], i['topOffsetCm'], i['id'])
                prox = engine.execute(sql)
            # for k, v in values[i].items():
            #
            #     if k =='bivalve' and v!='':
            #         print(v)
                # if k not in new_headers:




    return values


session.close()
if __name__ == '__main__':
    values=get_data_ture()
    print(values[:20])