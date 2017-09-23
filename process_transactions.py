import sqlite3
import numpy as np
import pandas as pd
import datetime as dt
import glob

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

# wf_trans_types = {
#   'Purchase': 'PURCHASE AUTHORIZED',
#   'Return': 'PURCHASE RETURN',
#   'ATM Withdrawal': 'ATM WITHDRAWAL',
#   'Direct Deposit': 'DIRECT DEP',
#   'Deposit': 'eDeposit',
#   'Transfer': 'TRANSFER',
# }

wf_trans_types = {
    'PURCHASE AUTHORIZED' : ('Purchase',lambda df: split_wf_purchase(df)),
    'PURCHASE RETURN': ('Return', lambda df: split_wf_return(df)),
    # 'ATM WITHDRAWAL',
    'DIRECT DEP': ('Direct Deposit', lambda df: split_wf_dd(df)),
    # 'eDeposit',
    'TRANSFER': ('Transfer', lambda df: split_wf_trnf(df)),
}

def import_files(date):

    glob_string = '{}*.csv'.format(date)
    import_files = glob.glob(glob_string)

    for file in import_files:

        date, bank, account_type = file[:-4].split('_')

        df = pd.read_csv(file, header=None)

        df['transaction_type'] = ''
        df['transaction_date'] = ''
        df['formatted_description'] = ''
        df['transaction_city'] = ''
        df['transaction_state'] = ''
        df['source_id_num'] = ''
        df['card_num'] = ''
        df['recipient_name'] = ''

        clean_df = clean_transactions(df, bank)
        return clean_df

def clean_transactions(df, bank):

    if bank == 'wf':

        df.rename(columns={0: 'record_date', 1: 'amount', 2: 'star', 3: 'blank', 4: 'full_description'}, inplace=True)
        
        df['record_date'] = pd.to_datetime(df['record_date'])
        
        df_list = []

        for tran_type, tran_tup in wf_trans_types.items():

        	df.loc[df['full_description'].str.contains(tran_type), 'transaction_type'] = tran_tup[0]

        	sub_df = tran_tup[1](df.loc[df['full_description'].str.contains(tran_type)])

        	df_list.append(sub_df)

        full_df = pd.concat(df_list)

        return full_df

def split_wf_purchase(sub_df):
    # sub_df['transaction_type'] = 'Purchase'
	sub_df[['transaction_date','formatted_description','transaction_city','transaction_state','source_id_num','card_num']] = sub_df['full_description'].str.extract(r'^PURCHASE AUTHORIZED ON (\d{2}/\d{2}) ([\w#\'\.\-\*\\\&\/]+[\s\w#\'\.\-\*\/\\\&]*) ([\w#\'\.\-\*\\\&\/]+[[\s\w\.\/#]{3,4}]*) ([A-Za-z]{2}) ([A-Za-z]{1}\d{10,}) CARD (\d{4})$')
	sub_df['transaction_date'] = sub_df.apply(format_date, axis=1)
	return sub_df

def split_wf_return(sub_df):
    # sub_df['transaction_type'] = 'Return'
    sub_df[['transaction_date','formatted_description','transaction_city','transaction_state','source_id_num','card_num']] = sub_df['full_description'].str.extract(r'^PURCHASE RETURN AUTHORIZED ON (\d{2}/\d{2}) ([\w#\'\.\-\*\\\&\/]+[\s\w#\'\.\-\*\\\/\&]*) ([\w#\'\.\-\*\\\&\/]+[[\s\w\.\/#]{3,4}]*) ([A-Za-z]{2}) ([A-Za-z]{1}\d{10,}) CARD (\d{4})$')
    sub_df['transaction_date'] = sub_df.apply(format_date, axis=1)
    return sub_df

def split_wf_dd(sub_df):
	# sub_df['transaction_type'] = 'Direct Deposit'
	sub_df[['formatted_description', 'transaction_date', 'source_id_num', 'recipient_name']] = sub_df['full_description'].str.extract(r'^([\w+\s*]+)DIRECT DEP (\d{6}) ([\w\d]+) ([\w\s,\.]+)$')

	sub_df['transaction_date'] = sub_df['transaction_date'].apply(lambda x: dt.datetime.strptime(str(x), '%y%m%d'))
	sub_df['formatted_description'] = sub_df['formatted_description'] + ' ' + sub_df['recipient_name']
	sub_df = sub_df.drop('recipient_name',axis=1)
	return sub_df

# def split_wf_atm(sub_df):

# def split_wf_edep(sub_df):

def split_wf_trnf(sub_df):

    sub_df[['source_id_num', 'card_num', 'transaction_date']] = sub_df['full_description'].str.extract(r'^ONLINE TRANSFER REF ([\w#]+) TO [\w\s]+ [X]+(\d{4}) ON ([\d\/]+)$')
    sub_df['transaction_date'] = pd.to_datetime(sub_df['transaction_date'])
    return sub_df

def format_date(row):

	record_year = row['record_date'].year
	record_mo = row['record_date'].month

	tran_mo, tran_day = map(int, row['transaction_date'].split('/'))

	if record_mo == tran_mo:
		tran_year = record_year
	elif record_mo < tran_mo:
		tran_year = record_year - 1
	elif record_mo > tran_mo:
		tran_year = record_year

	row['transaction_date'] = dt.datetime(tran_year, tran_mo, tran_day)

	return row