import numpy as np
import pandas as pd
import datetime as dt
import glob
import unittest

class ParseTest(unittest.TestCase):

	def setUp(self):
		bank_dict = {
            'wf': 'Wells Fargo',
            'usb': 'US Bank',
            'uva': 'UVA Community Credit Union',
        }

        account_dict = {
            'cc': 'Credit Card',
            'ch': 'Checking',
            'sa': 'Savings',
        }

        wf_trans_types = {
            'PURCHASE AUTHORIZED' : ('Purchase',lambda df: split_wf_purchase(df)),
            'PURCHASE RETURN': ('Return', lambda df: split_wf_return(df)),
            # 'ATM WITHDRAWAL',
            'DIRECT DEP': ('Direct Deposit', lambda df: split_wf_dd(df)),
            # 'eDeposit',
            'TRANSFER': ('Transfer', lambda df: split_wf_trnf(df)),
        }

    def tearDown(self):
        pass

    def test_import_files(self):
        pass



if __name__ == "__main__":
    unittest.main()