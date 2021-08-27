import pandas as pd
import os

class AccountingProcess():
    
    def __init__(self, accounts_filename, general_ledger_filename):

        '''
        Call methods in the constructor,
        Assign variables
        '''
        self.accounts_filename = accounts_filename
        self.general_ledger_filename = general_ledger_filename
        self.df_accounts = self.get_account_dataframe()
        self.df_general = self.get_general_ledger_dataframe()
        self.accounts = self.aggregate_account_and_general_ledger()
        self.number_of_levels = self.get_levels()
        self.levels = self.separate_data_by_the_levels()
        self.results = self.main_process()
        self.final_result = self.reorder_data()
        self.save_data()
    
    def get_account_dataframe(self):
        
        '''
        Manipulate chart_of_accounts excel and transform into a dataframe
        '''
        df_accounts = pd.read_excel(self.accounts_filename, engine="openpyxl")
        df_accounts.dropna(axis=1, how='all', inplace=True)
        df_accounts.dropna(inplace=True)
        df_accounts['value'] = 0
        
        return df_accounts
    
    def get_general_ledger_dataframe(self):

        '''
        Manipulate general_ledger excel and transform into a dataframe
        Sum all the values for one account.  
        '''
        
        general_ledger = pd.read_excel(self.general_ledger_filename, engine="openpyxl")
        df_general = pd.DataFrame(general_ledger.groupby('account')['value'].apply(lambda x: sum(list(x))))
        df_general.reset_index(inplace=True)
        
        return df_general
    
    def aggregate_account_and_general_ledger(self):

        '''
        Assign the values in the general ledger to accounts,
        Transform accounts into a dictionary
        '''
        
        for index_account, data_account in enumerate(zip(self.df_accounts['account'], self.df_accounts['value'])):
            for account_general, value_general in (zip(self.df_general['account'], self.df_general['value'])):
                if data_account[0] == account_general:
                    self.df_accounts.loc[index_account, 'value'] = value_general
                    
        self.df_accounts.set_index('account', inplace=True)
        accounts = self.df_accounts.to_dict()['value']
                    
        return accounts
        
    def get_levels(self):

        '''
        Return list with the range being the number of higher subdivision in the accounts
        '''
    
        number_of_levels = list()
        for key, value in self.accounts.items():
            number_of_levels.append(key.count('.'))
        number_of_levels= list(set(number_of_levels))
        max_value = max(number_of_levels)

        return number_of_levels
        
    def separate_data_by_the_levels(self):

        '''
        Separate the accounts based on the subdivisions
        '''

        levels = []
        for i in reversed(range(len(self.number_of_levels))):
            levels.append({key:val for key,val in self.accounts.items() if key.count('.')==i})
        
        return levels
        
    def main_process(self):

        '''
        Takes the child account, sum them and atribute to the parent account
        '''

        for i in range(len(self.number_of_levels)-1):
            for account_parent, value_parent in self.levels[i+1].items():
                new_value = 0
                for account_child, value_child in self.levels[i].items():
                    if account_child.startswith(account_parent):
                        new_value += value_child
                final_value = value_parent + new_value
                self.levels[i+1][account_parent] = final_value 
                
        return self.levels
        
    def reorder_data(self):

        '''
        Reorder the accounts based on the chart_of_accounts
        '''

        final_result = {k1:{k:v for item in self.results for k,v in item.items()}[k1] for k1 in self.accounts.keys()}
        
        return final_result

    def save_data(self):
        s = pd.Series(self.final_result, name='value')
        s.index.name = 'account'
        df = pd.DataFrame(s)
        df.to_excel('final_result.xlsx')