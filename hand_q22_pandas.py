import pandas as pd

def q22(customer, orders):
    var1 = ('13', '31', '23', '29', '30', '18', '17')

    cu1 = customer.copy()

    cu1_filt = cu1[(cu1['c_acctbal'] > 0.00)
                   & (cu1['c_phone'].str.startswith(var1[0])
                      | cu1['c_phone'].str.startswith(var1[1])
                      | cu1['c_phone'].str.startswith(var1[2])
                      | cu1['c_phone'].str.startswith(var1[3])
                      | cu1['c_phone'].str.startswith(var1[4])
                      | cu1['c_phone'].str.startswith(var1[5])
                      | cu1['c_phone'].str.startswith(var1[6]))]

    cu1_agg = cu1_filt.agg(sum_acctbal=('c_acctbal', 'sum'),
                           count_acctbal=('c_acctbal', 'count')).squeeze()

    cu1_avg = cu1_agg['sum_acctbal'] / cu1_agg['count_acctbal']

    cu_filt = customer[(customer['c_acctbal'] > cu1_avg)
                       & (customer['c_phone'].str.startswith(var1[0])
                          | customer['c_phone'].str.startswith(var1[1])
                          | customer['c_phone'].str.startswith(var1[2])
                          | customer['c_phone'].str.startswith(var1[3])
                          | customer['c_phone'].str.startswith(var1[4])
                          | customer['c_phone'].str.startswith(var1[5])
                          | customer['c_phone'].str.startswith(var1[6]))]

    custsale = cu_filt[~cu_filt['c_custkey'].isin(orders['o_custkey'])]
    custsale['cntrycode'] = customer['c_phone'].str.slice(0, 2)

    result = custsale.groupby(['cntrycode'], as_index=False).agg(numcust=('c_acctbal', 'count'),
                                                                 totacctbal=('c_acctbal', 'sum'))

    return result