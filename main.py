import requests, re, time
# 脚本测试(0)or 开始抢购(1)
STATUS = 1
mode = 2
if (STATUS==1):
    mode = 1
print(mode)
good_id = ""
good_url = ""
session = requests.Session()
headers = {
"Host": "shop44164290.youzan.com",
"User-Agent": "Mozilla/5.0 (Linux; Android 11; V1981A Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045811 Mobile Safari/537.36 MMWEBID/6799 MicroMessenger/8.0.14.2000(0x28000E37) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
}
# 搜索九价信息
search_url = 'https://shop44164290.youzan.com/wscshop/showcase/goods_search/goods.json?kdt_id=43972122&offline_id=0&keyword=九价&page=1&page_size=20'
session.headers.update(headers)
flag = True
# 如果找不到在售九价，每隔0.5s查询一次
TIME = 0.5
while(flag):
    try:
        search = session.get(search_url)
        js = search.json()
        if js["code"] == 0:
            goods_list = js["data"]
            for good in goods_list:
                title = good["title"]
                if "九价" in title and good["sold_status"] == mode:
                    msg = "查询到疫苗:\n"
                    good_id = str(good["id"])
                    good_url = good["url"]
                    msg += "title：{0}\nid:{1}\n{2}\n".format(good["title"], good["id"], good["url"])
                    flag = False
                    break
            if (good_id == ""):
                print("商品未开售")
        else:
            msg = "查询失败"

    except Exception as e:
        print("请求错误")
    time.sleep(TIME)
print(msg)
tail = good_url.split('/')[-1]
# 商品详情链接
true_url = "https://shop44164290.m.youzan.com/wscgoods/detail/"+tail
print(true_url)
try:
    headers["Host"] = "shop44164290.m.youzan.com"
    headers["Cookie"] = 'KDTSESSIONID=YZ913378021525524480YZ80vtE6Sq; nobody_sign=YZ913378021525524480YZ80vtE6Sq; _kdt_id_=43972122; Hm_lvt_679ede9eb28bacfc763976b10973577b=1637809466; yz_log_uuid=17841ecd-9d07-1e78-60a8-53b10aa8022b; yz_log_ftime=1637809465876; yz_log_seqb=1637809465944; loc_dfp=8483cb9a28662c9444f8177e8575298a; dfp=6511a23d484207c7145abd2cf3a3251d; captcha_sid=YZ913384999488376832YZb0uL1L0r; Hm_lpvt_679ede9eb28bacfc763976b10973577b=1637809631; yz_log_seqn=279'
    session.headers.update(headers)
    good_detail = session.get(true_url)
    txt = good_detail.text
    pattern1 = re.compile('kdtId=[0-9]*')
    pattern2= re.compile('"skuId":[0-9]*')
    kdtId = str(pattern1.findall(txt)[0][6:])
    skuId = str(pattern2.findall(txt)[0][8:])
    print("good_id:" + good_id)
    # print("kdtId:" + kdtId)
    print("skuId:" + skuId)
except Exception as e:
    print("wrong")
    exit(0)
# 下单
buy_url = "https://cashier.youzan.com/pay/wsctrade/order/buy/v2/bill-fast.json?kdt_id=43972122"
data = {
    "version": 2,
    "source": {
        "bookKey": "163aa402-974b-44ac-8e52-2afe10717241",
        "clientIp": "59.172.4.216",
        "fromThirdApp": False,
        "isWeapp": False,
        "itemSources": [{
            "activityId": 0,
            "activityType": 0,
            "bizTracePointExt": "{\"yai\":\"wsc_c\",\"st\":\"js\",\"sv\":\"1.1.31\",\"atr_uuid\":\"\",\"page_type\":\"\",\"yzk_ex\":\"\",\"tui_platform\":\"\",\"tui_click\":\"\",\"uuid\":\"17841ecd-9d07-1e78-60a8-53b10aa8022b\",\"userId\":13373954287,\"platform\":\"web\",\"from_source\":\"\",\"wecom_uuid\":\"\",\"wecom_chat_id\":\"\"}",
            "cartCreateTime": 0,
            "cartUpdateTime": 0,
            "gdtId": "",
            "goodsId": good_id,
            "pageSource": "",
            "skuId": skuId
        }],
        "kdtSessionId": "YZ913378021525524480YZ80vtE6Sq",
        "needAppRedirect": False,
        "orderType": 0,
        "platform": "unknown",
        "salesman": "",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "bizPlatform": ""
    },
    "config": {
        "bosWorkFlow": False,
        "containsUnavailableItems": False,
        "fissionActivity": {
            "fissionTicketNum": 0
        },
        "paymentExpiry": 0,
        "receiveMsg": True,
        "usePoints": False,
        "useWxpay": False,
        "buyerMsg": "姓名:吴李花;手机号:15807932371;身份证号:362331199801191026",  # 备注信息
        "disableStoredDiscount": True,
        "storedDiscountRechargeGuide": True,
        "yzGuaranteeInfo": {
            "displayTag": {
                "IS_YZ_SECURED": "0",
                "FREIGHT_INSURANCE_FREE": "0",
                "IS_FREIGHT_INSURANCE": "0"
            },
            "freightInsurance": False,
            "mainSupportContent": [],
            "securedItemSnapshotList": [],
            "hideYzGuarantee": False,
            "page": "order"
        }
    },
    "usePayAsset": {},
    "items": [{
        "activityId": 0,
        "activityType": 0,
        "deliverTime": 0,
        "extensions": {
            "OUTER_ITEM_ID": "10000"
        },
        "fCode": "",
        "goodsId": good_id,
        "isSevenDayUnconditionalReturn": False,
        "itemFissionTicketsNum": 0,
        "itemMessage": "[\"15807932371\"]",  # 手机号
        "kdtId": 43972122,
        "num": 1,
        "pointsPrice": 0,
        "price": 100,
        "skuId": skuId,
        "storeId": 0,
        "umpSkuId": 0
    }],
    "seller": {
        "kdtId": 43972122,
        "storeId": 0
    },
    "ump": {
        "activities": [{
            "activityId": 0,
            "activityType": 0,
            "externalPointId": 0,
            "goodsId": good_id,
            "kdtId": 43972122,
            "pointsPrice": 0,
            "skuId": skuId,
            "usePoints": False
        }],
        "coupon": {},
        "useCustomerCardInfo": {
            "specified": False
        },
        "costPoints": {
            "kdtId": 43972122,
            "usePointDeduction": True
        }
    },
    "newCouponProcess": True,
    "unavailableItems": [],
    "asyncOrder": False,
    "delivery": {
        "hasFreightInsurance": False,
        "expressTypeChoice": 0
    },
    "confirmTotalPrice": 100,
    "extensions": {
        "IS_OPTIMAL_SOLUTION": "True",
        "IS_SELECT_PRESENT": "0",
        "SELECTED_PRESENTS": "[]",
        "BIZ_ORDER_ATTRIBUTE": "{\"RISK_GOODS_TAX_INFOS\":\"0\"}"
    },
    "behaviorOrderInfo": {
        "bizType": 158,
        "token": ""
    }
}
headers["Host"] = "cashier.youzan.com"
# proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}  # 设置fiddler代理
session.headers.update(headers)
buy_result = session.post(url=buy_url, json=data, verify=False)
print(buy_result.text)


