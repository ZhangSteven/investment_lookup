# coding=utf-8
# 
from xlrd import open_workbook
from investment_lookup.utility import get_current_path
import logging
logger = logging.getLogger(__name__)



class InvalidAccountingTreatment(Exception):
	pass

class InvalidPortfolioId(Exception):
	pass

class InvestmentIdNotFound(Exception):
	pass

class InvestmentCurrencyNotFound(Exception):
	pass

class InvalidStockId(Exception):
	pass



def get_investment_Ids(portfolio_id, security_id_type, security_id, accounting_treatment=None):
	"""
	Determine the appropriate investment id for a security, based on:

	1. The position's security id type: ISIN for isin code
	2. The position's security id value
	3. The position's accounting treatmentposition: HTM or Trading

	Returns a tuple (geneva_investment_id, isin, bloomberg_figi), at least one
	of the items in the tuple should be non-empty.
	"""
	logger.debug('get_investment_Ids(): portfolio_id={0},security_id_type={1}, security_id={2}, accounting_treatment={3}'.
					format(portfolio_id, security_id_type, security_id, accounting_treatment))

	if accounting_treatment is None:
		accounting_treatment = get_portfolio_accounting_treatment(portfolio_id)

	if not accounting_treatment in ['HTM', 'Trading']:
		logger.error('get_investment_Ids(): invalid accounting treatment:{0}'.format(accounting_treatment))
		raise InvalidAccountingTreatment()

	if security_id_type == 'ISIN':
		return get_investment_id_from_isin(accounting_treatment, security_id)

	# BOC HK use 'Market' as the security id type if the bank does not know its
	# ISIN code, then it uses the security id from its local market. For example,
	# 4 HK Equity, it uses a market id 'HK 00004'. Another example, China
	# interbank bond 'AGRICULTURAL BK CHINA/HK 0 22/02/17', it uses a market 
	# id 'CN COAL7980769'.

	# So here we try to detect whether the security is a stock based on the market
	# id, if yes then return the Geneva id directly. 
	# elif security_id_type == 'Market' and security_id.startswith('HK') and len(security_id) == 8:
	elif security_id_type == 'Market' and security_id.startswith('HK'):
		return (get_stock_investment_id(security_id), '', '')

	else:
		isin, bbg_id, geneva_investment_id_for_HTM = lookup_investment_id(security_id_type, security_id)
		if isin != '':
			return get_investment_id_from_isin(accounting_treatment, isin)
		else:
			if accounting_treatment == 'HTM':
				return (geneva_investment_id_for_HTM, '', '')
			else:
				return ('', '', bbg_id)



def get_stock_investment_id(security_id):
	"""
	When the security id looks like a stock, e.g., 'HK 00004', return its
	Geneva investment id.
	"""
	tokens = security_id.split()
	if len(tokens) != 2:
		logger.error('get_stock_investment_id(): invalid id: {0}'.format(security_id))
		raise InvalidStockId()

	i = 0
	for c in tokens[1]:
		if c == '0':
			i = i + 1
		else:
			break

	if tokens[1][i:] == '':
		logger.error('get_stock_investment_id(): invalid stock code: {0}'.format(tokens[1]))
		raise InvalidStockId()

	return tokens[1][i:] + ' ' + tokens[0]



def get_investment_id_from_isin(accounting_treatment, isin):
	if accounting_treatment == 'HTM':
		# return (isin + ' HTM', '', '')

		# The change has been made because the HTM portfolios can contain
		# AFS positions, then we use ISIN code to match those positions.
		return (isin + ' HTM', isin, '')

	else:
		return ('', isin, '')



investment_lookup = {}
currency_lookup = {}
def initialize_investment_lookup(lookup_file=get_current_path()+'\\investmentLookup.xls'):
	"""
	Initialize the lookup table from a file, for those securities that
	do have an isin code.

	To lookup,

	isin, bbg_id = investment_lookup(security_id_type, security_id)
	"""
	logger.debug('initialize_investment_lookup(): on file {0}'.format(lookup_file))

	wb = open_workbook(filename=lookup_file)
	ws = wb.sheet_by_name('Sheet1')
	row = 1
	global investment_lookup
	while (row < ws.nrows):
		security_id_type = ws.cell_value(row, 0)
		if security_id_type.strip() == '':
			break

		security_id = value_to_string(ws.cell_value(row, 1))
		# print('security_id {0}, type {1}'.format(security_id, type(security_id)))
		isin = ws.cell_value(row, 3)
		bbg_id = ws.cell_value(row, 4)
		investment_id = ws.cell_value(row, 5)
		if isinstance(security_id, float):
			security_id = str(int(security_id))

		investment_lookup[(security_id_type.strip(), security_id.strip())] = \
			(isin.strip(), bbg_id.strip(), investment_id.strip())

		row = row + 1
	# end of while loop 

	ws = wb.sheet_by_name('Sheet2')
	row = 1
	global currency_lookup
	while (row < ws.nrows):
		security_id_type = ws.cell_value(row, 0)
		if security_id_type.strip() == '':
			break

		security_id = ws.cell_value(row, 1)
		currency = ws.cell_value(row, 3)
		if isinstance(security_id, float):
			security_id = str(int(security_id))

		currency_lookup[(security_id_type.strip(), security_id.strip())] = currency.strip()

		row = row + 1
	# end of while loop 



def lookup_investment_id(security_id_type, security_id):
	logger.debug('lookup_investment_id(): security_id_type={0}, security_id={1}'.
					format(security_id_type, security_id))

	global investment_lookup
	if len(investment_lookup) == 0:
		initialize_investment_lookup()

	try:
		return investment_lookup[(security_id_type, security_id)]
	except KeyError:
		logger.error('lookup_investment_id(): No record found for security_id_type={0}, security_id={1}'.
						format(security_id_type, security_id))
		raise InvestmentIdNotFound()



def lookup_investment_currency(security_id_type, security_id):
	logger.debug('lookup_investment_currency(): security_id_type={0}, security_id={1}'.
					format(security_id_type, security_id))

	global currency_lookup
	if len(currency_lookup) == 0:
		initialize_investment_lookup()

	try:
		return currency_lookup[(security_id_type, security_id)]
	except KeyError:
		logger.error('lookup_investment_currency(): No record found for security_id_type={0}, security_id={1}'.
						format(security_id_type, security_id))
		raise InvestmentCurrencyNotFound()



def get_portfolio_accounting_treatment(portfolio_id):
	"""
	Map a portfolio id to its accounting treatment.
	"""
	a_map = {
		# China Life overseas equity, discretionary / non-discretionary
		'11490':'Trading',
		'12341':'Trading',
		'12298':'Trading',
		'12857':'Trading',
		'12856':'Trading',
		'12726':'Trading',

		# China Life ListCo equity, discretionary / non-discretionary
		'12404':'Trading',
		'12307':'Trading',
		'12086':'Trading',
		'12094':'HTM',

		# China Life overseas bond (HTM)
		'12528':'HTM',
		'12229':'HTM',
		'12630':'HTM',
		'12366':'HTM',

		'12548':'HTM',	# portfolio closed, but kept here so that
						# past testing code does not break
		
		'12549':'HTM',
		'12732':'HTM',
		'12733':'HTM',
		'12734':'HTM',

		# DIF
		'19437':'Trading',

		# Concord 
		'21815':'Trading',

		# Greenblue
		'11602':'Trading',

		# Special Event Fund
		'16454':'Trading',

		# China Life Franklin Clients Account
		'13456':'Trading',

		# FFX
		'30001':'Trading',

		# in house fund
		'20051':'HTM',

		# the new China Life Macau fund
		'99999':'HTM',

		# ListCo Equity SCYF
		'12087':'Trading',

		# JIC International
		'40002': 'Trading'
	}
	try:
		return a_map[portfolio_id]
	except KeyError:
		logger.error('get_portfolio_accounting_treatment(): {0} is not a valid portfolio id'.
						format(portfolio_id))
		raise InvalidPortfolioId()



def value_to_string(value):
	"""
	A security id may be in a integer form, but we need to store it as string.
	"""
	if isinstance(value, str):
		return value
	else:
		try:
			return str(int(value))
		except:
			logger.exception('value_to_string(): ')
			raise