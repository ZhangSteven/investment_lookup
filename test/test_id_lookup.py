"""
Test the open_jpm.py
"""

import unittest2
from investment_lookup.utility import get_current_path
from investment_lookup.id_lookup import get_investment_Ids, \
                                        InvalidPortfolioId, \
                                        InvestmentIdNotFound, \
                                        initialize_investment_lookup, \
                                        lookup_investment_currency, \
                                        InvestmentCurrencyNotFound, \
                                        InvalidAccountingTreatment, \
                                        get_stock_investment_id, \
                                        InvalidStockId



class TestLookup(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLookup, self).__init__(*args, **kwargs)

    def setUp(self):
        """
            Run before a test function
        """
        pass



    def tearDown(self):
        """
            Run after a test finishes
        """
        pass



    def test_get_investment_Ids(self):
        """
        Read the date
        """
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('11490', 'ISIN', 'xyz')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, 'xyz')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('11490', 'CMU', 'HSBCFN13014')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, 'HK0000163607')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('11490', 'JPM', '4C0198S')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '<to be determined>')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('12548', 'ISIN', 'xyz')

        self.assertEqual(geneva_investment_id_for_HTM, 'xyz HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('12548', 'CMU', 'HSBCFN13014')

        self.assertEqual(geneva_investment_id_for_HTM, 'HK0000163607 HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('12548', 'CMU', 'WLHKFN09007')

        self.assertEqual(geneva_investment_id_for_HTM, 'CMU_WLHKFN09007 HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')



    def test_get_investment_Ids_2(self):
        """
        Read the date
        """
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'ISIN', 'xyz')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, 'xyz')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'ISIN', 'xyz', 'Trading')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, 'xyz')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'ISIN', 'xyz', 'HTM')

        self.assertEqual(geneva_investment_id_for_HTM, 'xyz HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'CMU', 'HSBCFN13014', 'HTM')

        self.assertEqual(geneva_investment_id_for_HTM, 'HK0000163607 HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'CMU', 'WLHKFN09007')

        self.assertEqual(geneva_investment_id_for_HTM, '')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, 'BBG00000WLY9')

        geneva_investment_id_for_HTM, isin, bloomberg_figi = \
            get_investment_Ids('19437', 'CMU', 'WLHKFN09007', 'HTM')

        self.assertEqual(geneva_investment_id_for_HTM, 'CMU_WLHKFN09007 HTM')
        self.assertEqual(isin, '')
        self.assertEqual(bloomberg_figi, '')



    def test_lookup_investment_currency(self):
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        security_id_type = 'JPM'
        security_id = 'B1L3XL6'
        self.assertEqual(lookup_investment_currency(security_id_type, security_id),
                            'HKD')



    def test_get_stock_investment_id(self):
        self.assertEqual(get_stock_investment_id('HK 00004'), '4 HK')

        with self.assertRaises(InvalidStockId):
            get_stock_investment_id('HK 00 04')

        with self.assertRaises(InvalidStockId):
            get_stock_investment_id('HK0004')

        with self.assertRaises(InvalidStockId):
            get_stock_investment_id('HK 0000')



    def test_error1(self):
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        with self.assertRaises(InvalidPortfolioId):
            get_investment_Ids('88888', 'ISIN', 'xyz')



    def test_error2(self):
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        with self.assertRaises(InvestmentIdNotFound):
            get_investment_Ids('11490', 'CMU', '12345678')



    def test_error3(self):
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        with self.assertRaises(InvestmentCurrencyNotFound):
            lookup_investment_currency('JPM', '8888888')



    def test_error4(self):
        lookup_file = get_current_path() + '\\samples\\sample_lookup.xls'
        initialize_investment_lookup(lookup_file)

        with self.assertRaises(InvalidAccountingTreatment):
            get_investment_Ids('19437', 'isin', 'xyz', 'some_weird_accounting')