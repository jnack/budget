import numpy as np
import matplotlib.pyplot as plt



def account_levels(abstraction='by_account', chart_type='timeseries'):

    # code to grab data from DB
    df = ###

   abstr_dict = {
       'by_account': 'account_number',
       'by_bank': 'bank_id'
    }

   abstr_field = abstr_dict[abstraction] 

    if chart_type = 'timeseries':
        df = df.groupby(['transaction_date',abstr_field],as_index=False).agg({
            'transaction_amount': sum
        })

        accounts = list(df[abstr_field].unique())
        
        f, ax = plt.subplots()
        
        for account in accounts:
            sub_df = df.loc[df[abstr_field]==account].sort_values('transaction_date')
            plt.plot(x=sub_df['transaction_date'], y=sub_df['amount'], label=account)
