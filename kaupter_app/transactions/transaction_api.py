import os
from json import loads, dumps
from flask import request, current_app as app
from SolomoLib import Util as util


def example_field_map(fieldmap):
    return dumps(util.load_configuration(fieldmap))

#from adapters.utils import db_utils
        
"""def get_active_count():
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    cursor = cn.cursor()
    cursor.execute("SELECT COUNT(*) as rec_count FROM CIPNAME0 WHERE FLGDLI = 'N'")
    row = cursor.fetchone()
    row_count = row[0]

    cursor.close()
    cn.close()

    if row:
        data = '{"account_count": %s}' % row_count
        return data

def get_all_count():
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    cursor = cn.cursor()
    cursor.execute("SELECT COUNT(*) as rec_count FROM CIPNAME0 ")
    row = cursor.fetchone()
    row_count = row[0]

    cursor.close()
    cn.close()

    if row:
        data = '{"account_count": %s}' % row_count
        return data

def get_account_by_cust_no(customer_number):
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    
    file = open('adapters/accounts/queries/account.sql', 'r')
    query = file.read()
    sql = query + " AND acct.CUNO = ?"

    cursor = cn.cursor()

    rows = cursor.execute(sql, (customer_number))
    data = db_utils.create_dict_from_cursor(rows)
    cursor.close()
    cn.close()  

    return data

def get_all_accounts(limit=10, offset=0):
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    
    file = open('adapters/accounts/queries/account.sql', 'r')
    query = file.read()
    filter = " LIMIT %s OFFSET %s" % (limit,offset)
    query += filter

    cursor = cn.cursor()
    data = db_utils.create_dict_from_cursor(cursor.execute(query))
    cursor.close()
    cn.close()  

    return data

def get_all_active_accounts(limit=10, offset=0):
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    
    file = open('adapters/accounts/queries/account.sql', 'r')
    query = file.read()
    filter = " AND acct.FLGDLI = 'N' LIMIT %s OFFSET %s" % (limit,offset)
    query += filter

    cursor = cn.cursor()
    data = db_utils.create_dict_from_cursor(cursor.execute(query))
    cursor.close()
    cn.close()  

    return data

def get_team_members(limit=10, offset=0):
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    
    file = open('adapters/accounts/queries/member.sql', 'r')
    query = file.read()
    filter = " LIMIT %s OFFSET %s" % (limit,offset)
    query += filter

    cursor = cn.cursor()
    data = db_utils.create_dict_from_cursor(cursor.execute(query))
    cursor.close()
    cn.close()  

    return data

def get_inclusive_accounts(limit=10, offset=0):
    active_customer_list = "adapters/accounts/data/inclusive.csv" 
    accounts = get_all_active_accounts(limit, offset)
    results = compare_and_return_active(active_customer_list, accounts)
    return results

def get_active_accounts_since(year=2012, limit=10, offset=0):
    cn_str = db_utils.get_connection_string("DB2")
    cn = pyodbc.connect(cn_str)
    
    file = open('adapters/accounts/queries/inclusive_accounts.sql', 'r')
    query = file.read()
    filter = " LIMIT %s OFFSET %s" % (limit,offset)
    query += filter

    cursor = cn.cursor()
    results = cursor.execute(query, (str(year)))
    data = db_utils.create_dict_from_cursor(results)
    cursor.close()
    cn.close()  

    return data

def compare_and_return_active(input_file, recs):
    results = []

    with open(input_file, "r") as inclusive_data:
        reader = csv.DictReader(inclusive_data, delimiter='\t')
        accounts = list(reader)

        for i in range(0, len(recs)):
            acct = recs[i]['CUSTOMER_NUMBER__C'].strip()
            included_acct = next(((row['CUNO']) for row in accounts if row['CUNO'] == acct), '')

            if included_acct:
                results.append(recs[i])
    return results """
