from Model.Payment import *
from Library.dataformat import *
from Config.config import *
from phpserialize import *
import requests, pickle
import collections 
import json
from datetime import datetime,timedelta,timezone


class SinoReportController():

	# 取得交易紀錄
	def getpayment():
		session_payment = SMaster()
		refund_list = session_payment.query(PackagePayment).filter(PackagePayment.pending_refund == 1,PackagePayment.status == 'refund').all()

		for refund in refund_list:
			data=collections.OrderedDict()
			data['ProcessDate'] = ProcessDate
			data['Merchant_ID'] = Merchant_ID
			data['tick_sernum'] = tick_sernum
			data['product_name'] = product_name
			data['pay_style'] = pay_style
			data['card_type'] = card_type
			data['str_CarditCard'] = str_CarditCard
			data['Authentication'] = Authentication
			data['tick_barcode'] = tick_barcode
			data['used_Style'] = used_Style
			data['prices'] = prices
			data['card_par'] = card_par
			data['trust_par'] = trust_par
			data['net_prices'] = net_prices
			data['order_date'] = order_date
			data['used_date'] = used_date
			data['cancel_date'] = cancel_date
			data['bank_check_date'] = bank_check_date
			data['Credit_prices'] = Credit_prices
			data['Trust_End_Date'] = Trust_End_Date
			data['sale_type'] = sale_type
			data['tick_type'] = tick_type
			data['payment_date'] = payment_date
			data['Terminal_ID'] = Terminal_ID
			data['Order_ID'] = Order_ID

