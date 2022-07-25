import io
import json
import re
from decimal import Decimal

from django.shortcuts import render

# Create your views here.


from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import hashlib

import os

from django.http import HttpResponse, HttpResponseRedirect, response, JsonResponse, StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from xlwt.compat import xrange
import xlsxwriter
from Mypro.settings import BASE_DIR
from get_headers import get_headers, get_classfy, get_all_headers, get_classfy_c, get_classfy_1, get_its_headers
from user.get_data import get_data_ture
from user.models import User

root_path = os.path.abspath(os.path.dirname(__file__)).split('ImgPro')[0] + 'ImgPro\\'


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        query = User.objects.filter(username=username)
        if query:
            return HttpResponse('用户名已注册')
        # md5 密码编码
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        try:
            User.objects.create(username=username, password=password_m)
        except Exception as e:
            print('crate user error %s' % e)
            return HttpResponse('用户名已注册')
        request.session['username'] = username

        return HttpResponseRedirect('/user/Home')


def check(request):
    username = request.GET['username']
    query = User.objects.filter(username=username)
    if query:
        list = {'msg': '用户名已注册'}

    return JsonResponse(list)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        if not user:
            return HttpResponse("用户不存在")
        m = hashlib.md5()
        m.update(request.POST['password'].encode())
        if m.hexdigest() != user.password:
            return HttpResponse('密码错误')

        request.session['username'] = user.username
        request.session['userid'] = user.id

        return render(request, 'user/index2.html', locals())


def index(request):
    return render(request, 'user/index2.html')


def about(request):
    return render(request, 'user/search2.html')


def search(request):
    return HttpResponseRedirect('/user/check_login')


def check_login(request):
    try:
        name = request.session['username']
        print(request.session['username'])
        return render(request, 'user/search.html')
    except:
        return HttpResponseRedirect('/user/login')


def check_user(request):
    print('check_user')
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        user_flag = 0
        pass_flat = 0
        result = {"user_flag": user_flag, "pass_flag": pass_flat}
        print(result)
        return JsonResponse(result)

    user_flag = 1
    pass_flat = 1
    if not user:
        user_flag = 0
    else:
        request.session['username'] = user.username
        request.session['userid'] = user.id
    m = hashlib.md5()
    m.update(request.POST['password'].encode())
    if m.hexdigest() != user.password:
        pass_flat = 0
    result = {"user_flag": user_flag, "pass_flag": pass_flat}
    print(result)
    return JsonResponse(result)

    return render(request, 'user/index2.html', locals())


def test(request):
    return render(request, 'user/test.html')


def Home(request):
    return render(request, 'user/Home.html')


def Introduction(request):
    return render(request, 'user/Introduction.html')


def Login_page(request):
    return render(request, 'user/login_page.html')


def About_us(request):
    return render(request, 'user/about_as.html')


def Access_data(request):
    return render(request, 'user/access_data.html')


def by_element(request):
    return render(request, 'user/by_element.html')


def by_interstatioal_water(request):
    return render(request, 'user/by_interstatioal_water.html')


def by_cnhs(request):
    return render(request, 'user/by_cnhs.html')


def by_sra(request):
    return render(request, 'user/by_sra.html')


def by_age(request):
    return render(request, 'user/by_age.html')


def by_location(request):
    return render(request, 'user/search_by_location.html')


def by_program(request):
    return render(request, 'user/search_by_program.html')


def search_result(request):
    return render(request, 'user/search_result.html')

def general_search(request):
    return render(request, 'user/general_search.html')


def search_download(request):
    return render(request, 'user/search_download.html')


def logingout(request):
    del request.session['userid']
    del request.session['username']
    return HttpResponseRedirect('/user/login')


def queryre(request):
    filterList_ = request.POST.getlist('filter')
    location = request.POST.getlist('location')
    age = request.POST['age']
    program = request.POST.getlist('program')
    element = request.POST.getlist('element')
    iw = request.POST.getlist('iw')
    cnhs = request.POST.getlist('cnhs')
    sra = request.POST.getlist('sra')
    src_check = request.POST['src_check']
    print(src_check)
    print(location)

    print(age)

    print(program)
    print(element)
    print(iw)
    print(cnhs)
    print(sra)
    print(filterList_)
    location_txt = ''

    if location != ['']:
        location_txt = 'new_latitude>="' + location[1] + '" and ' + 'new_latitude<="' + location[0] + '" and new_longitude>="' + \
                       location[3] + '" and new_longitude<="' + location[2] + '"'

    print('location_txt： ' + location_txt)
    program.sort(reverse=True)
    new_program = []
    for i in program:
        index = 0
        for j in new_program:
            if i not in j:
                index += 1
        if index == len(new_program):
            new_program.append(i)
    program = new_program

    # 此为循环or条件
    program_txt = []
    if program != ['']:
        count = 0
        for i in program:
            j = i.split('-')
            if j[1] != 'All':
                if len(j[1]) == 5:
                    count += 1
                    program_txt.append('(expdivleg="' + j[0] + '" and site="' + j[1] + '")')
                else:
                    program_txt.append(
                        '(expdivleg="' + j[0] + '" and site="' + j[1][0:5] + '" and hole="' + j[1][5] + '")')
            else:
                program_txt.append('(expdivleg="' + j[0] + '")')

    program_txt = " or ".join(program_txt)
    program_txt = '(' + program_txt + ')'
    print('program_txt: ' + program_txt)
    element_txt = []
    if element != ['']:
        for i in element:
            i = ' '.join(i.split())

            first = [m.strip() for m in re.split(':', i)]
            h = get_classfy(get_classfy_c(first[0]))
            second = re.split('_| ', first[1])
            t = []
            for it in get_its_headers(first[0]):
                t.append('(' + get_classfy(get_classfy_c(it)) + '>="' + second[0] + '" and ' + get_classfy(
                    get_classfy_c(it)) + '<="' + second[2] + '")')
            t = ' or '.join(t)
            t = "(" + t + ")"
            element_txt.append(t)
    element_txt = ' and '.join(element_txt)
    element_txt = '(' + element_txt + ')'
    print('element_txt：' + element_txt)

    iw_txt = []
    if iw != ['']:

        for i in iw:
            i = ' '.join(i.split())

            first = [m.strip() for m in re.split(':', i)]

            second = re.split('_| ', first[1])

            iw_txt.append('(' + get_classfy(get_classfy_c(first[0])) + '>="' + second[0] + '" and ' + get_classfy(
                get_classfy_c(first[0])) + '<="' + second[2] + '")')

    iw_txt = ' and '.join(iw_txt)
    iw_txt = '(' + iw_txt + ')'
    print('iw_txt: ' + iw_txt)

    cnhs_txt = []
    if cnhs != ['']:

        for i in cnhs:
            i = ' '.join(i.split())

            first = [m.strip() for m in re.split(':', i)]

            second = re.split('_| ', first[1])

            cnhs_txt.append('(' + get_classfy(get_classfy_c(first[0])) + '>="' + second[0] + '" and ' + get_classfy(
                get_classfy_c(first[0])) + '<="' + second[2] + '")')

    cnhs_txt = ' and '.join(cnhs_txt)
    cnhs_txt = '(' + cnhs_txt + ')'
    print('cnhs_txt ' + cnhs_txt)

    sra_txt = []
    if sra!= ['']:

        for i in sra:
            i = ' '.join(i.split())

            first = [m.strip() for m in re.split(':', i)]

            second = re.split('_| ', first[1])

            sra_txt.append('(' + get_classfy(get_classfy_c(first[0])) + '>="' + second[0] + '" and ' + get_classfy(
                get_classfy_c(first[0])) + '<="' + second[2] + '")')

    sra_txt = ' and '.join(sra_txt)
    sra_txt = '(' + sra_txt + ')'

    print('sra_txt: ' + sra_txt)

    print(request.POST.getlist('headers'))
    # text = ''
    # if filterList_ != []:
    #
    #     for i in filterList_:
    #         j = i.split(',')
    #         text += str(get_classfy(str(j[0]))) + str(j[1]) + '"' + str(j[2]) + '" and '
    # text += '1=1'
    filterList_ = []
    if location_txt != '':
        filterList_.append(location_txt)

    if program_txt != '()':
        filterList_.append(program_txt)
    if element_txt != '()':
        filterList_.append(element_txt)
    if iw_txt != '()':
        filterList_.append(iw_txt)
    if cnhs_txt != '()':
        filterList_.append(cnhs_txt)
    if sra_txt != '()':
        filterList_.append(sra_txt)
    print('查询数组')
    print(filterList_)

    filterList_ = ' and '.join(filterList_)
    print('filterList: ' + filterList_)
    headers = request.POST.getlist('headers')
    print(text)

    hs = []
    for i in headers:
        if i not in hs:
            hs += [i]
    headers = hs
    headers_0 = [get_classfy_c(header) for header in headers]

    headers_1 = [get_classfy(header) for header in headers_0]

    # filter_string=''
    # for line in filterList_:
    #     filter_string +=str(line[0])+'=='+str(line[1])

    # engine = create_engine('mysql+pymysql://root:root@localhost/totaldata', pool_size=100)
    #
    # # 定义模型类继承的父类及数据连接会话
    # metadata = MetaData(engine)
    # Session = scoped_session(sessionmaker())
    # Session.configure(bind=engine)
    # session = Session()
    # Base = declarative_base()
    # md = MetaData(bind=engine)
    # md = MetaData(bind=engine)
    keys = []
    values = []
    # with open('lables.txt', 'r', encoding='utf-8') as f:
    #     for line in f:
    #         keys.append(str(line.strip()))
    # keys = ['id'] + headers

    values, headers, counts = get_data_ture(filterList_, headers_1, src_check)
    print(headers)
    print(values)
    print(counts)
    all_headers = get_all_headers()

    new_headers = []
    for i in all_headers:

        if get_classfy(get_classfy_c(i)) in headers:
            new_headers += [get_classfy(get_classfy_c(i))]

    headers = ['id'] + new_headers
    print(headers)
    print('check')
    for i in range(0, len(values)):

        for k, v in values[i].items():
            if k not in headers:
                print(k)

    # prox = engine.execute('select * from sediment_tbl where %s' % filterList_)
    # for result in prox:
    #
    #     cur = dict()
    #     for k, v in result.items():
    #         cur[k] = v
    #     values.append(cur)
    # session.close()
    print('values')

    print(headers)
    print(values)

    result = {"keys": headers, "values": values, "counts": counts}

    return JsonResponse(result)
def queryre_1(request):
    filterList_ = request.POST.getlist('filter')
    src_check = request.POST['src_check']
    # print(filterList_)
    text = ''
    if filterList_ != []:

        for i in filterList_:
            j = i.split(',')
            text += str(get_classfy(str(j[0]))) + str(j[1]) + '"' + str(j[2]) + '" and '
    text += '1=1'
    filterList_ = text
    headers = request.POST.getlist('headers')
    print(headers)
    print(text)

    hs =[]
    for i in headers:
        if i not in hs:
            hs+=[i]
    headers=hs
    headers_0 = [get_classfy_c(header) for header in headers]

    headers_1 = [get_classfy(header) for header in headers_0]

    # filter_string=''
    # for line in filterList_:
    #     filter_string +=str(line[0])+'=='+str(line[1])

    # engine = create_engine('mysql+pymysql://root:root@localhost/totaldata', pool_size=100)
    #
    # # 定义模型类继承的父类及数据连接会话
    # metadata = MetaData(engine)
    # Session = scoped_session(sessionmaker())
    # Session.configure(bind=engine)
    # session = Session()
    # Base = declarative_base()
    # md = MetaData(bind=engine)
    # md = MetaData(bind=engine)
    keys = []
    values = []
    # with open('lables.txt', 'r', encoding='utf-8') as f:
    #     for line in f:
    #         keys.append(str(line.strip()))
    # keys = ['id'] + headers

    values, headers,_ = get_data_ture(filterList_, headers_1,src_check)
    # print(headers)
    print('values')
    print(values)
    all_headers = get_all_headers()

    new_headers = []
    for i in all_headers:

        if get_classfy(get_classfy_c(i)) in headers:


            new_headers += [get_classfy(get_classfy_c(i))]

    headers = ['id'] + new_headers
    print(headers)
    print('check')
    for i in range(0, len(values)):

        for k, v in values[i].items():
            if k not in headers:
                print(k)

    # prox = engine.execute('select * from sediment_tbl where %s' % filterList_)
    # for result in prox:
    #
    #     cur = dict()
    #     for k, v in result.items():
    #         cur[k] = v
    #     values.append(cur)
    # session.close()
    print('values')

    print(headers)
    print(values)

    result = {"keys": headers, "values": values, "num": [1, 2, 4]}

    return JsonResponse(result)

def get_allheaders(requset):
    datas, types, headers = get_headers()
    result = {'datas': datas, 'types': types, 'headers': headers}
    return JsonResponse(result)


def file_iterator(file_name, chunk_size=512):
    '''
	# 用于形成二进制数据
	:return:
	'''
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
    return c


def download(request):
    print('download------------')
    print(request.session['userid'])
    keys = request.POST.getlist('k')
    v = json.loads(request.POST['v'])

    values = []

    for i in v:

        tem = keys[:]

        for key, value in i.items():
            j = tem.index(key)
            tem[j] = value

            # tem[j]=None
        for ind in range(0, len(keys)):
            if keys[ind] == tem[ind]:
                tem[ind] = None

        values.append(tem)

    wbk = xlsxwriter.Workbook('./static/files/' + str(request.session['userid']) + '.xlsx')
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_worksheet('Sheet1')
    k = [get_classfy_1(i) for i in keys]
    for i in xrange(len(values)):
        # 对result的每个子元素作遍历，
        if i == 0:
            for x in xrange(len(k)):
                sheet.write(0, x, k[x])
        for j in xrange(len(values[i])):
            y = i + 1
            # 将每一行的每个元素按行号i,列号j,写入到excel中。
            print
            values[i][j]
            sheet.write(y, j, values[i][j])
    wbk.close()

    return JsonResponse({'id': request.session['userid']})
