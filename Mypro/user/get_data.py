from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# from get_headers import get_classfy_1, get_public_headers
from get_headers import get_public_headers

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


# public_headers=get_public_headers()





def get_data_ture(f, headers,src_check):
    sql = ['id']+headers+['new_latitude','new_longitude']
    sql = ','.join(sql)
    values = []
    start_time=time.time()
    try:
        prox = engine.execute('select %s from sediment_tbl_1 where %s' % (sql,f))
        z_time=time.time()
        print('select %s from sediment_tbl_1 where %s' % (sql,f))
        print('时间')
        print(z_time-start_time)
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
                    v=''
                cur[k] = str(v)
            values.append(cur)
    except:
        values = []
    if src_check:
        try:
            prox = engine.execute('select %s from sediment_tbl_2 where %s' % (sql,f))
            for result in prox:

                cur = dict()
                for k, v in result.items():

                    if v == None:
                        v = ''
                    cur[k] = str(v)
                values.append(cur)
        except:
            pass
    end_time=time.time()
    print('查询时间')
    print(end_time-start_time)
    # print(values)
    start_time = time.time()
    site_count = []
    hole_count = []
    leg_count=[]
    new_values=[]
    public_headers=get_public_headers()
    # print('public_headers')
    # print(public_headers)
    if values != []:
        for v in values:
            if 'new_latitude' in v.keys():
                v['latitude'] = v['new_latitude']
                del v['new_latitude']
            if 'new_longitude'in v.keys():
                v['longitude'] = v['new_longitude']
                del v['new_longitude']
        for i in range(0, len(values)):
            ks = []

            for k, v in values[i].items():

                if k not in public_headers and v!='':
                    ks += [k]
                # if k not in new_headers:
                #     new_headers += [k]
                if k == 'site' and v not in site_count:
                    site_count.append(v)
                if k == 'hole' and v not in hole_count:
                    hole_count.append(v)
                if k=='expdivleg' and v not  in leg_count:
                    leg_count.append(v)

            if len(ks)>=1:
                new_values.append(values[i])
            # ks = [j for j in ks if j not in public_headers]

    print('site_count: ')
    print(len(site_count))
    print('site_count: ')
    print(len(hole_count))
    print('leg_count')
    print(len(leg_count))
    value_count=len(new_values)
    print('sanple_count')
    print(value_count)
    end_time = time.time()
    print('操作时间')
    print(end_time - start_time)
    return new_values, headers,[len(leg_count),len(site_count),len(hole_count),value_count]




if __name__ == '__main__':
    f = '((expdivleg="5"))'
    values, _ ,a= get_data_ture(f, ['id', 'site', 'hole','expdivleg'])
    print(values)
