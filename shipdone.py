from AESCipher import *
import json


def encrypt(data):
    # print("encrypt")
    cert_encp_cd = 't3hzDZ4YFnD7x9cG'
    aes = AESCipher(cert_encp_cd)

    return aes.encrypt(data)


def orderparsing():
    # print("orderParsing")
    orderJsonFile = r'E:/nas/주문조회결과_0323_강변점.json'

    with open(orderJsonFile, 'r', encoding="utf-8") as f:
        order = json.load(f)

    orderList = order["data"]["orderDetl"]

    orderRst = []
    orderDetlId = "orderDetlId"
    itemId = "itemId"
    orderItem = "orderItem"
    shipDoneItemList = "shipDoneItemList"
    key = ["orderDetlItemId", "itemNm", "itemCnt"]
    for dic in orderList:
        orderDic = {
            shipDoneItemList: []
        }
        orderDic.update({orderDetlId: dic.get(orderDetlId)})

        for item in dic[orderItem]:
            itemDic = {}
            for x in key:
                if x == "orderDetlItemId":
                    itemDic.update({itemId: item.get(x)})
                else:
                    itemDic.update({x: item.get(x)})
            orderDic[shipDoneItemList].append(itemDic)
        orderRst.append(orderDic)

    return orderRst


def optmparsing():
    # print("optmParsing")
    optmJsonFile = r'E:/nas/response_롯데TB lglmart_강변점.json'

    with open(optmJsonFile, 'r', encoding="utf-8") as f:
        optmRes = json.load(f)

    # optmRes
    orderList = optmRes['data']['optmResult']
    carList = []
    for orderDic in orderList:
        carFile = orderDic['carId'] + '.json'
        carList.append(carFile)
        orderInfo = orderDic['orderInfo']
        orderInfoRes = orderInfo[1:len(orderInfo) - 1]

        with open(carFile, 'w', encoding="utf-8") as f:
            json.dump(orderInfoRes, f, ensure_ascii=False, indent="\t")

    # print(carList)
    return carList


def shipdone(orderRst, carList, default):
    # print("createShipDone")
    # data = '37.551256166892486'
    # print(encrypt(data))
    print(orderRst)
    print(carList)
    key = ["shipVisitNo", "orderDetlId", "orderDestNm", "posLat", "posLon"]
    shipDoneItemList = "shipDoneItemList"

    for car in carList:
        shipDone = []
        with open(car, 'r', encoding='utf-8') as f:
            orderInfoRes = json.load(f)

        for dic in orderInfoRes:
            shipDic = default.copy()  # 얇은 복사 필수
            for x in key:
                if x == "orderDestNm":
                    shipDic.update({"shipDoneUserNm": encrypt(dic.get(x))})
                elif x == "posLat":
                    shipDic.update({x: encrypt(dic.get(x))})
                elif x == "posLon":
                    shipDic.update({x: encrypt(dic.get(x))})
                else:
                    shipDic.update({x: dic.get(x)})

            for item in orderRst:
                if shipDic["orderDetlId"] == item["orderDetlId"]:
                    shipDic.update({shipDoneItemList: item[shipDoneItemList]})

            shipDone.append(shipDic)

        carShipFile = str(shipDoneItemList) + "_" + car
        with open(carShipFile, 'w', encoding="utf-8") as f:
            json.dump(shipDone, f, ensure_ascii=False, indent="\t")


if __name__ == '__main__':
    default = {
        "event": "comp",
        "memo": "",
        "recpRelationCd": "03",
        "ndlvReasonCd": "",
        "orientation": "6",
        "orderDate": "20230210",
        "orderId": "000000002334"
    }
    # 주문정보조회 가져와서 Parsing
    orderRst = orderparsing()
    # 최적화결과 가져와서 Parsing
    carList = optmparsing()
    # 배송보고 요청문 생성
    shipdone(orderRst, carList, default)
