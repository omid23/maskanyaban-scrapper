import sys
import traceback

from functions import get_session_maskanyaban
import requests
import json
from bs4 import BeautifulSoup


def get_maskanyaban(username, password, scrapping_page=10):
    try:
        url = "http://www.maskanyaban.ir/pages/homes.aspx/GetAllMelkForUser"
        post_index = 1
        page_num = 0
        authentication = get_session_maskanyaban(username=username, password=password)
        while page_num < scrapping_page:
            payload = "{NoeMelk:'',NoeVagozari:'',MinRahn:'',MaxRahn:'',MinEjareh:'',MaxEjareh:'',MinForosh:''," \
                      "MaxForosh:'',MinMetrazh:'',MaxMetrazh:'',startPageIndex:" + str(
                post_index) + ",MinRoom:'',MaxRoom:'',Mantaghe:'',Mantaghe1:'',Mantaghe2:'',Mantaghe3:''," \
                              "Mantaghe4:'',Mantaghe5:'',Mantaghe6:'',Mantaghe7:'',Mantaghe8:'',MinFloor:''," \
                              "MaxFloor:'',MinFloors:'',MaxFloors:'',MinUnit:'',MaxUnit:'',MinAge:'',MaxAge:''," \
                              "JahateMelk:'',North:'',South:'',TwoCorners:'',TowWay:'',Oriental:'',Western:''," \
                              "Document:'',Total:'',Half:'',Proxy:'',Promise:'',Asansor:'',Parking:'',HozoreMalek:''," \
                              "DarBarghi:'',Teras:'',Anbari:'',malek:'',tel:'',addressWord:'',date:'',RegisterType:''} "
            headers = {
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': '*/*',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36',
                'Content-Type': 'application/json',
                'Origin': 'http://www.maskanyaban.ir',
                'Referer': 'http://www.maskanyaban.ir/estate/all/all/?page=4',
                'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
                'Cookie': 'ASP.NET_SessionId=h2lef3fzs3fjom23jive2ha0',
            }

            response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False, )
            res = json.loads(response.text.encode('utf-8').decode())
            posts = res['d']
            if len(posts.split('[&]')) > 0:
                for post in posts.split('[&]'):
                    trading_type = ''
                    property_type = ''
                    additional_data = dict()
                    post_detail = post.split('[#]')
                    if len(post_detail) > 1:
                        post_index += 1
                        if int(post_detail[1]) == 1:
                            trading_type = 'rent'  # rent
                        elif int(post_detail[1]) == 0:
                            trading_type = 'sell'  # sell
                        elif int(post_detail[1]) == 2:
                            trading_type = 'mortgage'  # mortgage
                        if int(post_detail[2]) == 0:
                            property_type = 'apartment'  # apartment
                        elif int(post_detail[2]) == 2:
                            property_type = 'villa'  # villa
                        elif int(post_detail[2]) == 1 or int(post_detail[2]) == 3:
                            property_type = 'office'  # office or store
                        token = post_detail[0]
                        trading_type = trading_type
                        property_type = property_type
                        meter = post_detail[4]
                        title = post_detail[5]
                        address = post_detail[5]
                        price = post_detail[6]
                        mortgage = post_detail[7]
                        rent = post_detail[8]
                        floor = post_detail[9]
                        rooms = post_detail[10]
                        property_age = post_detail[11]
                        elevator = post_detail[12]
                        additional_data['floor'] = floor
                        post_detail_url = "http://www.maskanyaban.ir/home-" + token
                        url = post_detail_url + "/SCORPION"

                        post_detail_headers = {
                            'Cookie': 'ASP.NET_SessionId=siq3vxwugdqagezvsxeujb4n; .ASPXAUTH=' + str(
                                authentication),
                        }
                        response = requests.request("GET", post_detail_url, headers=post_detail_headers)
                        if response.status_code != 200:
                            return 0
                        response = response.text.encode('utf8').decode()
                        soup_main_page = BeautifulSoup(response, 'lxml')

                        phones = soup_main_page.find('div', {'id': 'ContentPlaceHolder1_Malek'}).find_all('h6')
                        phone = None
                        if phones is not None:
                            phone = phones[1].text.split(':')[1].strip()

                        details = soup_main_page.find('div', {'class': 'ConfigMelk'}).find('ul').find_all('li')
                        hidden_fields = ['طبقه', 'تعداد خواب', 'سن بنا', 'آسانسور']
                        for detail in details:
                            key = detail.text.split(':')[0].strip()
                            if key in hidden_fields:
                                continue
                            value = detail.text.split(':')[1].strip()
                            additional_data[key] = value
                        description = soup_main_page.find('div', {'class': 'DescMelk'}).text.replace(
                            "توضیحات ملک :",
                            "").strip()
                        description = description
                        parking = 0

                        facilities = soup_main_page.find('div', {'class': 'Facilities'})
                        facility_details = facilities.find('ul').find_all('li')
                        if len(facility_details) > 0:
                            for facility_detail in facility_details:
                                key = facility_detail.text
                                if key == "پارکینگ":
                                    parking = 1
                                    continue
                                value = "دارد"
                                additional_data[key] = value

                        yield {
                            'address': address,
                            'title': title,
                            'description': description,
                            'token': token,
                            'elevator': elevator,
                            'parking': parking,
                            'meter': meter,
                            'mortgage': mortgage,
                            'rent': rent,
                            'price': price,
                            'property_age': property_age,
                            'phone': phone,
                            'property_type': property_type,
                            'rooms': rooms,
                            'trading_type': trading_type,
                            'url': url,
                            'additional_data': additional_data, }

                page_num += 1

    except BaseException as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        print("\n Exception type : %s " % ex_type.__name__)
        print("\n Exception message : %s" % ex_value)
        print("\n Stack trace : %s" % stack_trace)
        print("\n Error : %s" % ex)
