# -*- coding: UTF-8 -*-

import datetime
import os

import requests
import logging

from main.data_types.item import Item, SpecialItem
from main.resources.searchers.base_searcher import BaseSearcher


class DigikalaSpecialOfferSearch(BaseSearcher):

    def start_search(self):
        results = []

        search_url = self.base_url

        logging.debug('Digikala special searching for special items: {}'.format(search_url))
        result = requests.get(search_url)
        if 200 <= result.status_code < 300:
            item_docs = result.json().get('responses')[0].get('hits').get('hits')
            for item_doc in item_docs:
                results.append(self.create_item(item_doc.get('_source'), 'digikala_special_items', search_url))
        else:
            logging.debug('DK searching for {}: ({})\n{}'.format('digikala_special_items', result.status_code, result.raw))

        return results

    def create_item(self, item_doc, search_phrase=None, search_url=None):
        g = SpecialItem()
        try:
            g.shop = 'digikala_special'
            g.search_phrase = search_phrase
            g.search_url = search_url

            g.price = item_doc.get('Price') - item_doc.get('Discount', 0)
            g.discount = item_doc.get('Discount')
            g.old_price = item_doc.get('Price')
            g.discount_percent = int(float(float(g.discount) / float(g.old_price)) * 100)
            g.view_price = item_doc.get('MaxPrice')

            try:
                g.start_date = datetime.datetime.strptime(item_doc.get('StartDateTime'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                g.start_date = datetime.datetime.strptime(item_doc.get('StartDateTime'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

            try:
                g.end_date = datetime.datetime.strptime(item_doc.get('EndDateTime'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                g.end_date = datetime.datetime.strptime(item_doc.get('EndDateTime'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

            g.title = item_doc.get('ShowTitle')
            g.name = item_doc.get('EnTitle')
            g.is_second_hand = False

            g.image_link = os.path.join('http://file.digikala.com/Digikala', item_doc.get('ProductImagePath'))
            g.link = 'http://www.digikala.com/Product/DKP-{}'.format(item_doc.get('Id'))

            return g
        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))

if __name__ == '__main__':

    res = DigikalaSpecialOfferSearch("http://search.digikala.com/api2/Data/Get?categoryId=0&ip=0", [], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s


'''
{
	"responses": [{
		"took": 3,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 10,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11348",
				"_score": null,
				"_source": {
					"Discount": 300000,
					"ShowTitle": "Asus Zenfone 4 Dual SIM Mobile Phone",
					"KeyFeatures": "تعداد سیم کارت: دو  سیم کارت\r\nحافظه داخلی: 8 گیگابایت\r\nشبکه های ارتباطی: 2G، 3G\r\nرزولوشن عکس: 5.0 مگاپیکسل\r\n",
					"ExistStatus": 2,
					"Title": "Asus Zenfone 4 Dual SIM",
					"BackgroundPath": "",
					"ProductId": 34406,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_4/Original/ASUS.png",
					"StartDateTime": "2016-11-02T00:00:00.407",
					"ProductImagePath": "Image/Webstore/Product/P_34406/Original/Mobile-Asus-Zenfone-4-Dual-SIMa49911.jpg",
					"EndDateTime": "2016-11-03T12:00:00.407",
					"Price": 2990000,
					"FaTitle": "گوشي موبايل دو سيم کارت ايسوس مدل Zenfone 4",
					"HasGift": false,
					"Id": 11348,
					"EnTitle": "Asus Zenfone 4 Dual SIM Mobile Phone"
				},
				"sort": ["F", 1]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11336",
				"_score": null,
				"_source": {
					"Discount": 460000,
					"ShowTitle": "Lenovo IdeaPad 110 - D - 15 inch",
					"KeyFeatures": "پردازنده: AMD Carrizo E1-7010\r\nرم: 2GB  - هارد: 500GB\r\nگرافیک: AMD Radeon R2\r\nسری جدید، جایگزین G5045\r\n",
					"ExistStatus": 2,
					"Title": "Lenovo IdeaPad 110",
					"BackgroundPath": "",
					"ProductId": 183971,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_94/Original/LENOVO.png",
					"StartDateTime": "2016-11-02T00:00:00.053",
					"ProductImagePath": "Image/Webstore/Product/P_183971/Original/Lenovo-IdeaPad-110---D---15-inch-Laptop-4c1c41.jpg",
					"EndDateTime": "2016-11-03T00:00:00.053",
					"Price": 9850000,
					"FaTitle": "لپ تاپ 15 اينچي لنوو مدل IdeaPad 110 - D",
					"HasGift": false,
					"Id": 11336,
					"EnTitle": "Lenovo IdeaPad 110 - D - 15 inch Laptop"
				},
				"sort": ["F", 2]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11337",
				"_score": null,
				"_source": {
					"Discount": 2500000,
					"ShowTitle": "Sony Playstation 4",
					"KeyFeatures": "ظرفیت هارد : 500 گیگابایت\r\nریجن : 3 \r\nسری : CUH-1206A",
					"ExistStatus": 2,
					"Title": "Sony Playstation 4",
					"BackgroundPath": "",
					"ProductId": 125866,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_1/Original/SONY-BRAND_49B1DB75C1374D4F9448AA351A2D4E2E.png",
					"StartDateTime": "2016-11-02T00:00:00.937",
					"ProductImagePath": "Image/Webstore/Product/P_125866/Original/Sony-Playstation-4-Region-3-CUH-1206A-500GB-Game-Console-dec792.jpg",
					"EndDateTime": "2016-11-03T00:00:00.937",
					"Price": 12990000,
					"FaTitle": "کنسول بازي سوني مدل Playstation 4 کد CUH-1206A ريجن 3 - ظرفيت 500 گيگابايت",
					"HasGift": false,
					"Id": 11337,
					"EnTitle": "Sony Playstation 4 Region 3 CUH-1206A 500GB Game Console"
				},
				"sort": ["F", 3]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11338",
				"_score": null,
				"_source": {
					"Discount": 960000,
					"ShowTitle": "مودم بی‌سیم 4G دی-لینک",
					"KeyFeatures": "وزن 180 گرم\r\nاتصال بی‌سیم ( Wi-Fi )\r\nپورت RJ-45 LAN\r\nپورت RJ-45 WAN/ LAN\r\nشیار سیم کارت",
					"ExistStatus": 2,
					"Title": "مودم بی‌سیم 4G دی-لینک",
					"BackgroundPath": "",
					"ProductId": 166901,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_43/Original/D-LINK.png",
					"StartDateTime": "2016-11-02T00:00:00.663",
					"ProductImagePath": "Image/Webstore/Product/P_166901/Original/D-Link-DWR-921E-Wireless-N300-4G-LTE-Router-39ed64.jpg",
					"EndDateTime": "2016-11-03T00:00:00.663",
					"Price": 3950000,
					"FaTitle": "مودم بي‌سيم 4G دي-لينک مدل DWR-921E",
					"HasGift": false,
					"Id": 11338,
					"EnTitle": "D-Link DWR-921E Wireless 4G Router"
				},
				"sort": ["F", 4]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11339",
				"_score": null,
				"_source": {
					"Discount": 551000,
					"ShowTitle": " ترازوی دیجیتال ترایلون",
					"KeyFeatures": "دارای صفحه‌ی شیشه‌ای\r\n ابعاد: 2.5 × 32 × 32 سانتی متر\r\nواحد های اندازه گیری: گرم، کیلوگرم",
					"ExistStatus": 2,
					"Title": " ترازوی دیجیتال ترایلون",
					"BackgroundPath": "",
					"ProductId": 91549,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "",
					"StartDateTime": "2016-11-02T00:00:00.093",
					"ProductImagePath": "Image/Webstore/Product/P_91549/Original/Digital-Scale-Terraillon-TX6000347b27.jpg",
					"EndDateTime": "2016-11-03T00:00:00.093",
					"Price": 1250000,
					"FaTitle": "ترازوي حمام ترايلون مدل TX6000",
					"HasGift": false,
					"Id": 11339,
					"EnTitle": "Terraillon TX6000 Bath Scale"
				},
				"sort": ["F", 7]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11342",
				"_score": null,
				"_source": {
					"Discount": 460000,
					"ShowTitle": "قفل فرمان خودرو شوان",
					"KeyFeatures": "بدنه مستحکم تمام فولادی و بسیار مقاوم\r\nدارای دو میله با ضخامت 16 میلی‌متر \r\nنوع کلید: کامپیوتری\r\nجنس روکش PVC",
					"ExistStatus": 2,
					"Title": "قفل فرمان خودرو ",
					"BackgroundPath": "",
					"ProductId": 151704,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "",
					"StartDateTime": "2016-11-02T00:00:00.833",
					"ProductImagePath": "Image/Webstore/Product/P_151704/Original/Schwan-904-Steering-Wheel-Lock.JPG",
					"EndDateTime": "2016-11-03T00:00:00.833",
					"Price": 790000,
					"FaTitle": "قفل فرمان خودرو شوان مدل 904",
					"HasGift": false,
					"Id": 11342,
					"EnTitle": "Schwan 904 Steering Wheel Lock"
				},
				"sort": ["F", 8]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11345",
				"_score": null,
				"_source": {
					"Discount": 840000,
					"ShowTitle": "Givenchy Dahlia Noir For Women",
					"KeyFeatures": "حجم: 75 میلی‌لیتر\r\n فرد سازنده: Francois Demachy\r\n ساختار رایحه: مرکبات، گل، میوه",
					"ExistStatus": 2,
					"Title": "Givenchy Dahlia Noir 75ml",
					"BackgroundPath": "",
					"ProductId": 162498,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "",
					"StartDateTime": "2016-11-02T00:00:00.357",
					"ProductImagePath": "Image/Webstore/Product/P_162498/Original/Perfume-Givenchy-Dahlia-Noir-Eau-De-Toilette-For-Women-75ml.jpg",
					"EndDateTime": "2016-11-03T00:00:00.357",
					"Price": 1980000,
					"FaTitle": "ادو تويلت زنانه ژيوانشي مدل Dahlia Noir حجم 75 ميلي ليتر",
					"HasGift": false,
					"Id": 11345,
					"EnTitle": "Givenchy Dahlia Noir Eau De Toilette For Women 75ml"
				},
				"sort": ["F", 9]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11346",
				"_score": null,
				"_source": {
					"Discount": 120000,
					"ShowTitle": " جامدادی گابل",
					"KeyFeatures": "جنس پلی استر \r\nابعاد70 × 105 × 230 میلی متر\r\nبا سه جیب زیپی \r\n",
					"ExistStatus": 2,
					"Title": "جامدادی",
					"BackgroundPath": "",
					"ProductId": 174805,
					"OnlyForMembers": false,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_3142/Original/GABOL.png",
					"StartDateTime": "2016-11-02T00:00:00.14",
					"ProductImagePath": "Image/Webstore/Product/P_174805/Original/Gabol-Cisne-Design-2-Pencil-Case.JPG",
					"EndDateTime": "2016-11-03T00:00:00.14",
					"Price": 310000,
					"FaTitle": "جامدادي گابل مدل Cisne طرح 2",
					"HasGift": false,
					"Id": 11346,
					"EnTitle": "Gabol Cisne Design 2 Pencil Case"
				},
				"sort": ["F", 10]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11341",
				"_score": null,
				"_source": {
					"Discount": 5460000,
					"ShowTitle": "دوچرخه کوهستان جاینت مدل ATX 1 سایز 27.5",
					"KeyFeatures": "مجهز به تکنولوژی AluXX افزایش استحکام و ایجاد وزنی سبک در دوچرخه \r\nدارای ترمز دیسکی\r\nکمک جلو قفل شونده\r\nکیفیت ساخت بالا\r\n\r\n",
					"ExistStatus": 3,
					"Title": "دوچرخه کوهستان Giant",
					"BackgroundPath": "",
					"ProductId": 185105,
					"OnlyForMembers": true,
					"OnlyForApplication": false,
					"BrandLogoPath": "",
					"StartDateTime": "2016-11-02T00:00:00.937",
					"ProductImagePath": "Image/Webstore/Product/P_185105/Original/Giant-ATX-1-Mountain-Bicycle-Size-27.5-9b6777.jpg",
					"EndDateTime": "2016-11-03T00:00:00.937",
					"Price": 0,
					"FaTitle": "دوچرخه کوهستان جاينت مدل ATX 1 سايز 27.5",
					"HasGift": false,
					"Id": 11341,
					"EnTitle": "Giant ATX 1 Mountain Bicycle Size 27.5"
				},
				"sort": ["T", 5]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "incredibleoffers",
				"_id": "11340",
				"_score": null,
				"_source": {
					"Discount": 4270000,
					"ShowTitle": " سرخ کن فیلیپس",
					"KeyFeatures": "توان مصرفی: 1425 وات\r\nسرخ کردن تنها با یک قاشق مربا خوری روغن\r\nمناسب برای سرخ کردن،بریان کردن، پختن و گریل کردن",
					"ExistStatus": 2,
					"Title": " سرخ کن فیلیپس",
					"BackgroundPath": "",
					"ProductId": 145101,
					"OnlyForMembers": true,
					"OnlyForApplication": false,
					"BrandLogoPath": "Image/Webstore/Brand/B_68/Original/PHILIPS_40A13123B5A840CA929A02FEFFCE9B26.jpg",
					"StartDateTime": "2016-11-02T00:00:00.723",
					"ProductImagePath": "Image/Webstore/Product/P_145101/Original/Philips-Viva-Collcetion-HD9623-Airfryer.jpg",
					"EndDateTime": "2016-11-03T00:00:00.723",
					"Price": 13760000,
					"FaTitle": "سرخ کن فيليپس سري Viva Collcetion مدل HD9623",
					"HasGift": false,
					"Id": 11340,
					"EnTitle": "Philips Viva Collcetion HD9623 Airfryer"
				},
				"sort": ["T", 6]
			}]
		}
	}, {
		"took": 2,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 690,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "video",
				"_id": "833",
				"_score": null,
				"_source": {
					"URLCode": "Apple_iPhone_7_Plus_Introduction",
					"VisitCounter": 2035,
					"CategoryUrlCode": "Mobile",
					"ContentCategoryUrlCode": "Introduction",
					"FaTitle": "معرفي اپل آيفون ۷ پلاس",
					"Duration": 83,
					"PreviewImagePath": "Movie/Introduction/Apple_iPhone_7_Plus_Introduction/49AB3555/Small/Apple_iPhone_7_Plus_Introduction.jpg",
					"Id": 833
				},
				"sort": [833, "F"]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "video",
				"_id": "831",
				"_score": null,
				"_source": {
					"URLCode": "Vibram_Trek_Ascent_Insulated_Introduction",
					"VisitCounter": 3172,
					"CategoryUrlCode": "Misc",
					"ContentCategoryUrlCode": "Introduction",
					"FaTitle": "معرفي کفش کوهنوردي مردانه ويبرام Trek Ascent Insulated",
					"Duration": 67,
					"PreviewImagePath": "Movie/Introduction/Vibram_Trek_Ascent_Insulated_Introduction/572D4307/Small/Vibram_Trek_Ascent_Insulated_Introduction.jpg",
					"Id": 831
				},
				"sort": [831, "F"]
			}]
		}
	}, {
		"took": 2,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 115,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "digimag",
				"_id": "172917",
				"_score": null,
				"_source": {
					"Id": 172917,
					"Title": "تمام بدنه‌ی گلکسی S8 از صفحه نمایش تشکیل شده",
					"Link": "http://mag.digikala.com/?p=172917",
					"ImagePath": "http://mag.digikala.com/wp-content/uploads/2016/11/Samsung-Galaxy-S8-edge-60x60.jpg",
					"PublishDateTime": "2016-11-02T11:22:00"
				},
				"sort": [1478085720000]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "digimag",
				"_id": "172919",
				"_score": null,
				"_source": {
					"Id": 172919,
					"Title": "سرویس بازی فیس‌بوک راه‌اندازی شد",
					"Link": "http://mag.digikala.com/?p=172919",
					"ImagePath": "http://mag.digikala.com/wp-content/uploads/2016/11/Facebook-Gameroom-60x60.jpg",
					"PublishDateTime": "2016-11-02T11:20:34"
				},
				"sort": [1478085634000]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "digimag",
				"_id": "172891",
				"_score": null,
				"_source": {
					"Id": 172891,
					"Title": "آیا مرگ تاپ‌گیر نزدیک است؟",
					"Link": "http://mag.digikala.com/?p=172891",
					"ImagePath": "http://mag.digikala.com/wp-content/uploads/2016/11/topgear-60x60.jpg",
					"PublishDateTime": "2016-11-02T11:12:37"
				},
				"sort": [1478085157000]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "digimag",
				"_id": "172867",
				"_score": null,
				"_source": {
					"Id": 172867,
					"Title": "سامسونگ یک میلیارد دلار در آستین تگزاس سرمایه‌گذاری می‌کند",
					"Link": "http://mag.digikala.com/?p=172867",
					"ImagePath": "http://mag.digikala.com/wp-content/uploads/2016/11/Samsung-Austin-plant-e1353099940474-60x60.jpg",
					"PublishDateTime": "2016-11-02T10:56:35"
				},
				"sort": [1478084195000]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "digimag",
				"_id": "165359",
				"_score": null,
				"_source": {
					"Id": 165359,
					"Title": "دنیای رزیدنت اویل 7؛ تریلرهای جدید را ببینید",
					"Link": "https://mag.digikala.com/?p=165359",
					"ImagePath": "http://mag.digikala.com/wp-content/uploads/2016/10/RE7-Trailer-60x60.jpg",
					"PublishDateTime": "2016-11-02T10:50:40"
				},
				"sort": [1478083840000]
			}]
		}
	}, {
		"took": 12,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 52542,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "5289",
				"_score": null,
				"_source": {
					"LikeCounter": 1013,
					"CategoryId": 5721,
					"ProductTypes": "T4594 ",
					"ProductAttributes": "A12062V12004 A12062V12003 A12062V13076 A12062V12005 A12063V13082 A12065V12010 A12074V12012 A13257V13319 A18359V21725 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 43,
					"MinPrice": 960000,
					"UserRating": 693,
					"UrlCode": "Computer-Net-D-Link-DSL-2750U-New",
					"LastPeriodViewCounter": 1638,
					"IsSpecialOffer": false,
					"ProductCategories": " C5721 C7192 C6987 C21 C4 C5966",
					"RegDateTime": "2001-01-01T00:00:00",
					"ImagePath": "Image/Webstore/Product/P_5289/Original/Computer-Net-D-Link-DSL-2750U-New9cddce.jpg",
					"ViewCounter": 3543,
					"HasVideo": false,
					"EnTitle": "D-Link DSL-2750U New N300 ADSL2+ Wireless Router",
					"OtherTitle": "Mahmehrabani29,Mahmehrabani26,Mahmehrabani23,Mahmehrabani20,Mahmehrabani17,d-linkfestival,dlinkjtir",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 5289,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 5289,
						"ColorCode": "White",
						"ColorId": 2
					}],
					"ShowType": 1,
					"Rate": 86,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 127991,
					"ProductColors": "C1 C2 ",
					"MinPriceList": 0,
					"FavoriteCounter": 0,
					"FaTitle": "مودم روتر بي‌سيم دي-لينک سري +ADSL2 مدل DSL-2750U New",
					"LastPeriodFavoriteCounter": 0,
					"Id": 5289,
					"MaxPrice": 960000,
					"LastPeriodSaleCounter": 66
				},
				"sort": [127991, 1638]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "35221",
				"_score": null,
				"_source": {
					"LikeCounter": 765,
					"CategoryId": 11,
					"ProductTypes": "T201 ",
					"ProductAttributes": "A136V197 A172V247 A183V261 A18186V21338 A18186V21339 A20172V24932 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 82,
					"MinPrice": 5790000,
					"UserRating": 754,
					"UrlCode": "Mobile-Huawei-Ascend-G750-U10-Dual-SIM",
					"LastPeriodViewCounter": 3479,
					"IsSpecialOffer": false,
					"ProductCategories": " C7322 C11 C1 C5966 C6988",
					"RegDateTime": "2014-07-01T14:12:00",
					"ImagePath": "Image/Webstore/Product/P_35221/Original/Mobile-Huawei-Ascend-G750-U10-Dual-SIM0c9910.jpg",
					"ViewCounter": 7087,
					"HasVideo": false,
					"EnTitle": "Huawei Ascend G750 U10 Dual SIM Mobile Phone",
					"OtherTitle": "huaweiBEST,اعشصثه انر 3ط ل يعشم سهئ، 750، Honor 3X",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 35221,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 35221,
						"ColorCode": "White",
						"ColorId": 2
					}],
					"ShowType": 2,
					"Rate": 87,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 126563,
					"ProductColors": "C1 C2 ",
					"MinPriceList": 6100000,
					"FavoriteCounter": 0,
					"FaTitle": "گوشي موبايل دو سيم کارت هوآوي مدل Ascend G750 U10 ",
					"LastPeriodFavoriteCounter": 0,
					"Id": 35221,
					"MaxPrice": 5790000,
					"LastPeriodSaleCounter": 5
				},
				"sort": [126563, 3479]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "14934",
				"_score": null,
				"_source": {
					"LikeCounter": 466,
					"CategoryId": 48,
					"ProductTypes": "T6 ",
					"ProductAttributes": "A6V8 A7V12 A16V21 A23V33 A51V78 A70V114 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 12,
					"MinPrice": 18990000,
					"UserRating": 319,
					"UrlCode": "Digital-Camera-Canon-EOS-700D-Kit-18-55mm-IS-STM",
					"LastPeriodViewCounter": 1344,
					"IsSpecialOffer": true,
					"ProductCategories": " C7619 C48 C6 C5966 C6981",
					"RegDateTime": "2013-06-24T22:00:00",
					"ImagePath": "Image/Webstore/Product/P_14934/Original/Digital-Camera-Canon-EOS-700D-Kit-18-55mm-IS-STM9072fb.jpg",
					"ViewCounter": 3624,
					"HasVideo": false,
					"EnTitle": "Canon EOS 700D Kit 18-55mm IS STM Digital Camera",
					"OtherTitle": "Mehrlottery8,mehrlottery5,photographybts,modern family,TripEquipment,Rebel T5i , LastingMemoriesFestival93, canondslr",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 14934,
						"ColorCode": "Black",
						"ColorId": 1
					}],
					"ShowType": 2,
					"Rate": 83,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 122504,
					"ProductColors": "C1 ",
					"MinPriceList": 0,
					"FavoriteCounter": 2124,
					"FaTitle": "دوربين ديجيتال کانن مدل EOS 700D Kit 18-55mm IS STM",
					"LastPeriodFavoriteCounter": 2124,
					"Id": 14934,
					"MaxPrice": 18990000,
					"LastPeriodSaleCounter": 5
				},
				"sort": [122504, 1344]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "4360",
				"_score": null,
				"_source": {
					"LikeCounter": 697,
					"ProductTypes": "T242 ",
					"ProductAttributes": "A604V1067 A604V4378 A606V1071 A6515V4370 A6516V4372 A8670V7477 A14112V13998 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 61,
					"MinPrice": 2490000,
					"UserRating": 776,
					"UrlCode": "Computer-HDD-Adata-HD710-1TB",
					"LastPeriodViewCounter": 3144,
					"IsSpecialOffer": true,
					"ProductCategories": " C68 C68 C7531 C6987 C22 C4 C5966 C19 C19 C6060 C5966 C3 C5966",
					"RegDateTime": "2001-01-01T00:00:00",
					"ImagePath": "Image/Webstore/Product/P_4360/Original/Computer-HDD-Adata-HD710-1TB42eaae.jpg",
					"ViewCounter": 6349,
					"HasVideo": false,
					"EnTitle": "Adata HD710 External Hard Drive - 1TB",
					"OtherTitle": "externalhdd,ITReturn,HARDpromotion,HDDvaMODEM,Coin_adata,ladiesfestdigital,btslottery, mtpcsteacher, datastoragebts, datastorage1, , Adata HD710, Adata HD-710, Adata HD_710, Adata HD 710, raningday",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 4360,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "آبي",
						"ColorHex": "#0000FF",
						"ProductId": 4360,
						"ColorCode": "Blue",
						"ColorId": 4
					}, {
						"ColorTitle": "زرد",
						"ColorHex": "#FFFF00",
						"ProductId": 4360,
						"ColorCode": "Yellow",
						"ColorId": 5
					}],
					"ShowType": 2,
					"Rate": 82,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 122277,
					"ProductColors": "C1 C4 C5 ",
					"MinPriceList": 2590000,
					"FavoriteCounter": 0,
					"FaTitle": "هاردديسک اکسترنال اي ديتا مدل HD710 ظرفيت 1 ترابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 4360,
					"MaxPrice": 2490000,
					"LastPeriodSaleCounter": 139
				},
				"sort": [122277, 3144]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "21067",
				"_score": null,
				"_source": {
					"LikeCounter": 719,
					"CategoryId": 5721,
					"ProductTypes": "T4594 ",
					"ProductAttributes": "A12062V12003 A12062V12004 A12063V12008 A12074V12011 A13257V13319 A18359V21725 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 43,
					"MinPrice": 570000,
					"UserRating": 475,
					"UrlCode": "Computer-Net-D-Link-Wireless-Router-DSL-2730U-U1",
					"LastPeriodViewCounter": 1594,
					"IsSpecialOffer": false,
					"ProductCategories": " C5721 C7192 C6987 C21 C4 C5966",
					"RegDateTime": "2013-09-13T17:49:00",
					"ImagePath": "Image/Webstore/Product/P_21067/Original/Computer-Net-D-Link-Wireless-Router-DSL-2730U-U10190a5.jpg",
					"ViewCounter": 3251,
					"HasVideo": false,
					"EnTitle": "D-Link DSL-2730U/U1 Wireless N150 ADSL2+ Modem Router",
					"OtherTitle": "d-linkfestival,D-Link DSL-2730U, DSL2730U/U1, DSL-2730UU1, DSL2730UU1",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 21067,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 21067,
						"ColorCode": "White",
						"ColorId": 2
					}],
					"ShowType": 1,
					"Rate": 89,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 115678,
					"ProductColors": "C1 C2 ",
					"MinPriceList": 610000,
					"FavoriteCounter": 232,
					"FaTitle": "مودم روتر  بي‌سيم N150 دي-لينک سري +ADSL2 مدل DSL-2730U/U1",
					"LastPeriodFavoriteCounter": 232,
					"Id": 21067,
					"MaxPrice": 570000,
					"LastPeriodSaleCounter": 89
				},
				"sort": [115678, 1594]
			}]
		}
	}, {
		"took": 11,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 20996,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "117313",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 11,
					"ProductTypes": "T201 ",
					"ProductAttributes": "A136V197 A172V247 A183V261 A13366V13402 A13366V21003 A13366V13404 A18186V21338 A18186V21339 A18186V21340 A20172V24933 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 22,
					"MinPrice": 5790000,
					"UserRating": 1610,
					"UrlCode": "Mobile-Phone-LG-K10",
					"LastPeriodViewCounter": 21613,
					"IsSpecialOffer": false,
					"ProductCategories": " C7322 C11 C1 C5966 C6988",
					"RegDateTime": "2016-01-06T09:49:48.513",
					"ImagePath": "Image/Webstore/Product/P_117313/Original/Mobile-Phone-LG-K10d67ec6.jpg",
					"ViewCounter": 42091,
					"HasVideo": false,
					"EnTitle": "LG K10 Dual SIM 16GB Mobile Phone",
					"OtherTitle": "gooshihaye4g,LG BESTIES,smarphone4g,MOBILEdualsim,VARIA MOBILE,4G-TOP,4Gmobile,collectionMOBILE,popularmobile,LG FESTIVAL,addult,K10,ن10,;d10,کي10,lg k10,ال‌جي K10,الجي K10",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 117313,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 117313,
						"ColorCode": "White",
						"ColorId": 2
					}, {
						"ColorTitle": "سورمه اي",
						"ColorHex": "#191970",
						"ProductId": 117313,
						"ColorCode": "MidnightBlue",
						"ColorId": 9
					}, {
						"ColorTitle": "طلايي",
						"ColorHex": "#FFD700",
						"ProductId": 117313,
						"ColorCode": "Gold",
						"ColorId": 15
					}],
					"ShowType": 2,
					"Rate": 75,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C1 C2 C9 C15 ",
					"MinPriceList": 0,
					"FavoriteCounter": 0,
					"FaTitle": "گوشي موبايل دو سيم کارت ال جي مدل K10 ظرفيت 16 گيگابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 117313,
					"MaxPrice": 5790000,
					"LastPeriodSaleCounter": 572
				},
				"sort": [572, 21613, 2]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "154624",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 1272,
					"ProductTypes": "",
					"ProductAttributes": "A23576V32506 A23581V32512 A23581V32516 A23583V32541 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 1339,
					"MinPrice": 990000,
					"UserRating": 315,
					"UrlCode": "Accessories-Mobile-Power-Bank-Romoss-Polymos-20-20000mAh",
					"LastPeriodViewCounter": 5012,
					"IsSpecialOffer": false,
					"ProductCategories": " C1272 C7784 C6984 C12 C12 C6060 C5966 C1 C5966",
					"RegDateTime": "2016-06-30T12:24:04.27",
					"ImagePath": "Image/Webstore/Product/P_154624/Original/Romoss-Polymos-20-20000mAh-Power-Bank.JPG",
					"ViewCounter": 10687,
					"HasVideo": false,
					"EnTitle": "Romoss Polymos 20 20000mAh Power Bank",
					"OtherTitle": "affiliateac,acbest,acbtscolledge,Powerbankoffer,Polymos 20 , romoss , power bank , شارژر همراه , روموس , راموس",
					"ProductColorList": [{
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 154624,
						"ColorCode": "White",
						"ColorId": 2
					}],
					"ShowType": 1,
					"Rate": 77,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C2 ",
					"MinPriceList": 1490000,
					"FavoriteCounter": 0,
					"FaTitle": "شارژر همراه روموس مدل Polymos 20 با ظرفيت 20000 ميلي آمپر ساعت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 154624,
					"MaxPrice": 990000,
					"LastPeriodSaleCounter": 505
				},
				"sort": [505, 5012, 2]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "88765",
				"_score": null,
				"_source": {
					"LikeCounter": 64,
					"CategoryId": 68,
					"ProductTypes": "T242 ",
					"ProductAttributes": "A604V1067 A604V4378 A606V1071 A6515V4370 A6516V4373 A8670V7478 A14112V13998 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 48,
					"MinPrice": 2110000,
					"UserRating": 622,
					"UrlCode": "Computer-External-HDD-Western-Digital-My-Passport-Ultra-Premium-1TB",
					"LastPeriodViewCounter": 6503,
					"IsSpecialOffer": false,
					"ProductCategories": " C68 C68 C7531 C6987 C22 C4 C5966 C19 C19 C6060 C5966 C3 C5966",
					"RegDateTime": "2015-07-07T19:45:18.01",
					"ImagePath": "Image/Webstore/Product/P_88765/Original/Computer-External-HDD-Western-Digital-My-Passport-Ultra-Premium-1TB7045c3.jpg",
					"ViewCounter": 15182,
					"HasVideo": false,
					"EnTitle": "Western Digital My Passport Ultra Premium External Hard Drive - 1TB",
					"OtherTitle": "Mahmehrabani29,Mahmehrabani23,Mahmehrabani20,HARDpromotion,External Hard Drive - 1TB, my passport,passport ultra, wdpremium, وسترن ديجيتال, ماي پاسپورت,ماي پاسپورت آلترا, 1 ترابايت, My Passport Ultra Premium, Western Digital My Passport Ultra Premium",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 88765,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "آبي",
						"ColorHex": "#0000FF",
						"ProductId": 88765,
						"ColorCode": "Blue",
						"ColorId": 4
					}, {
						"ColorTitle": "زرشکي",
						"ColorHex": "#8B0000",
						"ProductId": 88765,
						"ColorCode": "DarkRed",
						"ColorId": 16
					}, {
						"ColorTitle": "سفيد صدفي",
						"ColorHex": "#FFF5EE",
						"ProductId": 88765,
						"ColorCode": "SeaShell",
						"ColorId": 29
					}],
					"ShowType": 2,
					"Rate": 71,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 8266,
					"ProductColors": "C1 C4 C16 C29 ",
					"MinPriceList": 2150000,
					"FavoriteCounter": 0,
					"FaTitle": "هاردديسک اکسترنال وسترن ديجيتال مدل My Passport Ultra Premium ظرفيت 1 ترابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 88765,
					"MaxPrice": 2160000,
					"LastPeriodSaleCounter": 324
				},
				"sort": [324, 6503, 2]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "88766",
				"_score": null,
				"_source": {
					"LikeCounter": 45,
					"CategoryId": 68,
					"ProductTypes": "T242 ",
					"ProductAttributes": "A604V1067 A604V4378 A606V1073 A6515V4370 A6516V4373 A8670V7478 A14112V13998 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 48,
					"MinPrice": 3105000,
					"UserRating": 494,
					"UrlCode": "Computer-External-HDD-Western-Digital-My-Passport-Ultra-Premium-2TB",
					"LastPeriodViewCounter": 7999,
					"IsSpecialOffer": false,
					"ProductCategories": " C68 C68 C7531 C6987 C22 C4 C5966 C19 C19 C6060 C5966 C3 C5966",
					"RegDateTime": "2015-07-07T19:45:50.49",
					"ImagePath": "Image/Webstore/Product/P_88766/Original/Computer-External-HDD-Western-Digital-My-Passport-Ultra-Premium-2TB09b9ce.jpg",
					"ViewCounter": 17670,
					"HasVideo": false,
					"EnTitle": "Western Digital My Passport Ultra Premium External Hard Drive - 2TB",
					"OtherTitle": "HARDpromotion ,My Passport Ultra Premium, WesternDigital My Passport Ultra Premium External Hard Drive - 2TB, my passport, passport ultra, wd, premium, وسترن ديجيتال, ماي پاسپورت, ماي پسپورت, ماي پاسپورت آلترا, 2 ترابايت",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 88766,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "آبي",
						"ColorHex": "#0000FF",
						"ProductId": 88766,
						"ColorCode": "Blue",
						"ColorId": 4
					}, {
						"ColorTitle": "زرشکي",
						"ColorHex": "#8B0000",
						"ProductId": 88766,
						"ColorCode": "DarkRed",
						"ColorId": 16
					}, {
						"ColorTitle": "سفيد صدفي",
						"ColorHex": "#FFF5EE",
						"ProductId": 88766,
						"ColorCode": "SeaShell",
						"ColorId": 29
					}],
					"ShowType": 2,
					"Rate": 74,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 5409,
					"ProductColors": "C1 C4 C16 C29 ",
					"MinPriceList": 3150000,
					"FavoriteCounter": 0,
					"FaTitle": "هاردديسک اکسترنال وسترن ديجيتال مدل My Passport Ultra Premium ظرفيت 2 ترابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 88766,
					"MaxPrice": 3160000,
					"LastPeriodSaleCounter": 300
				},
				"sort": [300, 7999, 2]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "128256",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 11,
					"ProductTypes": "T201 ",
					"ProductAttributes": "A136V197 A172V247 A183V261 A13366V21003 A13366V25763 A18186V21338 A18186V21339 A18186V21340 A20172V24933 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 22,
					"MinPrice": 7050000,
					"UserRating": 361,
					"UrlCode": "Mobile-Phone-LG-Stylus-2-K520DY",
					"LastPeriodViewCounter": 9345,
					"IsSpecialOffer": true,
					"ProductCategories": " C7322 C11 C1 C5966 C6988",
					"RegDateTime": "2016-02-17T11:05:20.04",
					"ImagePath": "Image/Webstore/Product/P_128256/Original/Mobile-Phone-LG-Stylus-2e417dc.jpg",
					"ViewCounter": 18716,
					"HasVideo": false,
					"EnTitle": "LG Stylus 2 Dual SIM K520DY 16GB Mobile Phone",
					"OtherTitle": "gooshihaye4g,LG BESTIES,4G-TOP,collectionMOBILE,bestLG,popularmobile,LG Stylus 2,Stylus 2,stylus,hsjhdg,s,استايلوس 2,سفغمعس 2, , K520DY",
					"ProductColorList": [{
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 128256,
						"ColorCode": "White",
						"ColorId": 2
					}, {
						"ColorTitle": "نوک مدادي",
						"ColorHex": "#696969",
						"ProductId": 128256,
						"ColorCode": "DimGray",
						"ColorId": 13
					}, {
						"ColorTitle": "قهوه اي",
						"ColorHex": "#8B4513",
						"ProductId": 128256,
						"ColorCode": "SaddleBrown",
						"ColorId": 14
					}],
					"ShowType": 2,
					"Rate": 75,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C2 C13 C14 ",
					"MinPriceList": 7400000,
					"FavoriteCounter": 0,
					"FaTitle": "گوشي موبايل دو سيم کارت ال جي مدل Stylus 2 K520DY ظرفيت 16 گيگابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 128256,
					"MaxPrice": 7050000,
					"LastPeriodSaleCounter": 157
				},
				"sort": [157, 9345, 2]
			}]
		}
	}, {
		"took": 17,
		"timed_out": false,
		"_shards": {
			"total": 1,
			"successful": 1,
			"failed": 0
		},
		"hits": {
			"total": 52542,
			"max_score": null,
			"hits": [{
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "185141",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 68,
					"ProductTypes": "T241 ",
					"ProductAttributes": "A604V4378 A606V1075 A6515V4371 A14112V13998 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 28,
					"MinPrice": 5550000,
					"UserRating": 1,
					"UrlCode": "computer-stroage-hdd-external-stel4000200-backup-pluse-desktop-4t",
					"LastPeriodViewCounter": 0,
					"IsSpecialOffer": false,
					"ProductCategories": " C68 C68 C7531 C6987 C22 C4 C5966 C19 C19 C6060 C5966 C3 C5966",
					"RegDateTime": "2016-10-31T15:16:37.63",
					"ImagePath": "Image/Webstore/Product/P_185141/Original/Seagate-Backup-Plus-Desktop-External-Hard-Disk-bc8ad7.jpg",
					"ViewCounter": 0,
					"HasVideo": false,
					"EnTitle": "Seagate Backup Plus Hub Desktop External Hard Disk - 4TB",
					"OtherTitle": "هارد اکسترنال , هارد 4 ترابايت , هارد سيگيت , stel4000200",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 185141,
						"ColorCode": "Black",
						"ColorId": 1
					}],
					"ShowType": 1,
					"Rate": 60,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C1 ",
					"MinPriceList": 0,
					"FavoriteCounter": 0,
					"FaTitle": "هارد ديسک اکسترنال سيگيت مدل Backup Plus Hub Desktop ظرفيت 4 ترابايت",
					"LastPeriodFavoriteCounter": 0,
					"Id": 185141,
					"MaxPrice": 5550000,
					"LastPeriodSaleCounter": 0
				},
				"sort": [185141, 0]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "184955",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 74,
					"ProductTypes": "T3537 ",
					"ProductAttributes": "A14889V15048 A14892V15049 A14893V15051 A14894V15054 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 123,
					"MinPrice": 1190000,
					"UserRating": 2,
					"UrlCode": "Accessories-Mobile-Handsfree-Jabra-Mini-Bluetooth-Headset-With-Car-Charger",
					"LastPeriodViewCounter": 0,
					"IsSpecialOffer": false,
					"ProductCategories": " C74 C74 C7563 C6984 C17 C17 C6060 C5966 C2 C5966 C12 C12 C6060 C5966 C1 C5966",
					"RegDateTime": "2016-10-31T09:12:26.487",
					"ImagePath": "Image/Webstore/Product/P_184955/Original/Jabra-Mini-Bluetooth-Headset-With-Car-Charger-3dbad3.jpg",
					"ViewCounter": 0,
					"HasVideo": false,
					"EnTitle": "Jabra Mini Bluetooth Headset With Car Charger",
					"OtherTitle": "jarbramini , تشذقش , [fvh",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 184955,
						"ColorCode": "Black",
						"ColorId": 1
					}],
					"ShowType": 1,
					"Rate": 76,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C1 ",
					"MinPriceList": 0,
					"FavoriteCounter": 0,
					"FaTitle": "هدست بلوتوث جبرا مدل Mini به همراه شارژ فندکي",
					"LastPeriodFavoriteCounter": 0,
					"Id": 184955,
					"MaxPrice": 1190000,
					"LastPeriodSaleCounter": 2
				},
				"sort": [184955, 0]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "184918",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 18,
					"ProductTypes": "T4 ",
					"ProductAttributes": "A303V432 A308V472 A310V490 A316V515 A351V600 A14251V14733 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 94,
					"MinPrice": 29990000,
					"UserRating": 3,
					"UrlCode": "Notebook-Lenovo-IdeaPad-Z5070-K",
					"LastPeriodViewCounter": 6,
					"IsSpecialOffer": true,
					"ProductCategories": " C18 C7063 C7967 C3 C5966",
					"RegDateTime": "2016-10-30T16:25:00.06",
					"ImagePath": "Image/Webstore/Product/P_184918/Original/Lenovo-IdeaPad-Z5070---K---15-inch-Laptop-0df682.jpg",
					"ViewCounter": 6,
					"HasVideo": false,
					"EnTitle": "Lenovo IdeaPad Z5070 - K - 15 inch Laptop",
					"OtherTitle": "لنو، مثدخرخ، زد 5070، 5070، سري 50، لب تاب، نوت بوک",
					"ProductColorList": [{
						"ColorTitle": "مشکي",
						"ColorHex": "#000000",
						"ProductId": 184918,
						"ColorCode": "Black",
						"ColorId": 1
					}, {
						"ColorTitle": "سفيد",
						"ColorHex": "#FFFFFF",
						"ProductId": 184918,
						"ColorCode": "White",
						"ColorId": 2
					}],
					"ShowType": 2,
					"Rate": 56,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C1 C2 ",
					"MinPriceList": 30500000,
					"FavoriteCounter": 0,
					"FaTitle": "لپ تاپ 15 اينچي لنوو مدل IdeaPad Z5070 - K",
					"LastPeriodFavoriteCounter": 0,
					"Id": 184918,
					"MaxPrice": 29990000,
					"LastPeriodSaleCounter": 1
				},
				"sort": [184918, 6]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "184898",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 5796,
					"ProductTypes": "",
					"ProductAttributes": "",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 1090,
					"MinPrice": 1985000,
					"UserRating": 0,
					"UrlCode": "Heater-Pars-Khazar-SH2000P",
					"LastPeriodViewCounter": 0,
					"IsSpecialOffer": false,
					"ProductCategories": " C5796 C7930 C7929 C5855 C5753 C5967",
					"RegDateTime": "2016-10-30T15:03:28.96",
					"ImagePath": "Image/Webstore/Product/P_184898/Original/Pars-Khazar-SH2000P-Heater-edbdca.jpg",
					"ViewCounter": 0,
					"HasVideo": false,
					"EnTitle": "Pars Khazar SH2000P Heater",
					"OtherTitle": "haheaterproducts,mehrlottery6,پارسخزر، Parskhazar، حشقسناشظشق، حشقس ناشظشق، پارث خزر، پارص خزر، پارثخزر، پارصخزر، heaterbigsale93",
					"ProductColorList": [],
					"ShowType": 2,
					"Rate": 0,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "",
					"MinPriceList": 0,
					"FavoriteCounter": 0,
					"FaTitle": "فن هيتر پارس خزر مدل SH2000P",
					"LastPeriodFavoriteCounter": 0,
					"Id": 184898,
					"MaxPrice": 1985000,
					"LastPeriodSaleCounter": 0
				},
				"sort": [184898, 0]
			}, {
				"_index": "ecs_20161029_184125",
				"_type": "product",
				"_id": "184816",
				"_score": null,
				"_source": {
					"LikeCounter": 0,
					"CategoryId": 6497,
					"ProductTypes": "T5993 ",
					"ProductAttributes": "A19068V22911 A19074V22914 ",
					"IsActive": true,
					"AnnounceDate": "2079-01-01T00:00:00",
					"ReducedPrice": 0,
					"BrandId": 1772,
					"MinPrice": 550000,
					"UserRating": 1,
					"UrlCode": "Enamels-Shirazi-Plate-20CM-Diagonal-Type-4",
					"LastPeriodViewCounter": 0,
					"IsSpecialOffer": false,
					"ProductCategories": " C6497 C6497 C7227 C6986 C8017 C6451 C8 C6451 C8",
					"RegDateTime": "2016-10-30T11:48:48.427",
					"ImagePath": "Image/Webstore/Product/P_184816/Original/Enamels-Shirazi-Plate-20CM-Diagonal-Type-4-ce3b76.jpg",
					"ViewCounter": 0,
					"HasVideo": false,
					"EnTitle": " ",
					"OtherTitle": "صنايع دستي , مينا کاري , ldkh;hvd , ldkh ;hvd Enamelled Copper Plate By Shirazi 20cm Diagonal Type 3 , minakari , mina kari",
					"ProductColorList": [{
						"ColorTitle": "آبي",
						"ColorHex": "#0000FF",
						"ProductId": 184816,
						"ColorCode": "Blue",
						"ColorId": 4
					}],
					"ShowType": 2,
					"Rate": 74,
					"ExistStatus": 2,
					"LastPeriodLikeCounter": 0,
					"ProductColors": "C4 ",
					"MinPriceList": 800000,
					"FavoriteCounter": 0,
					"FaTitle": "بشقاب مسي ميناکاري شده اثر شيرازي طرح 4 قطر 20 سانتي متر",
					"LastPeriodFavoriteCounter": 0,
					"Id": 184816,
					"MaxPrice": 550000,
					"LastPeriodSaleCounter": 6
				},
				"sort": [184816, 0]
			}]
		}
	}]
}
'''