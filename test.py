from unittest import TestCase
from script import AccountingProcess
import unittest
import pandas as pd

class TestProcessAccount(TestCase):

    def test_general_ledger_to_dataframe(self):
        accounts_filename = 'chart_of_accounts.xlsx'
        general_ledger_filename = 'general_ledger.xlsx'
        a = AccountingProcess(accounts_filename, general_ledger_filename)
        a.get_general_ledger_dataframe()
        self.assertEqual(a.df_general.shape, (171, 2))

    def test_account_charts_to_dataframe(self):
        accounts_filename = 'chart_of_accounts.xlsx'
        general_ledger_filename = 'general_ledger.xlsx'
        a = AccountingProcess(accounts_filename, general_ledger_filename)
        a.get_account_dataframe()
        self.assertEqual(a.df_accounts.shape, (255, 1))

    def test_main_process(self):
        accounts_filename = 'chart_of_accounts.xlsx'
        general_ledger_filename = 'general_ledger.xlsx'
        a = AccountingProcess(accounts_filename, general_ledger_filename)
        reference = list(a.final_result.values())
        self.assertTrue(all(reference))
        


if __name__ == '__main__':
    unittest.main()