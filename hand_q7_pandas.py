import pandas as pd

def q7(supplier, lineitem, orders, customer, nation):
    var1 = 'FRANCE'
    var2 = 'GERMANY'

    na_filt = nation[(nation['n_name'] == var1) | (nation['n_name'] == var2)]

    na_su_join = nation.merge(right=supplier,
                              left_on='n_nationkey', right_on='s_nationkey',
                              how='inner')

    na_su_join.rename({'n_name': 'n1_name'}, axis=1, inplace=True)

    na_cu_join = na_filt.merge(right=customer,
                               left_on='n_nationkey', right_on='c_nationkey',
                               how='inner')

    cu_ord_join = na_cu_join.merge(right=orders,
                                   left_on='c_custkey', right_on='o_custkey',
                                   how='inner')

    cu_ord_join.rename({'n_name': 'n2_name'}, axis=1, inplace=True)

    li_filt = lineitem[(lineitem['l_shipdate'] >= '1995-01-01') & (lineitem['l_shipdate'] <= '1996-12-31')]

    ord_li_join = cu_ord_join.merge(right=li_filt,
                                    left_on='o_orderkey', right_on='l_orderkey',
                                    how='inner')

    all_join = na_su_join.merge(right=ord_li_join,
                                left_on='s_suppkey', right_on='l_suppkey',
                                how='inner')

    all_join = all_join[((all_join['n1_name'] == var1) & (all_join['n2_name'] == var2))
                        | ((all_join['n1_name'] == var2) & (all_join['n2_name'] == var1))]

    all_join['supp_nation'] = all_join['n1_name']
    all_join['cust_nation'] = all_join['n2_name']
    all_join['l_year'] = all_join['l_shipdate'].dt.year
    all_join['volume'] = all_join['l_extendedprice'] * (1.0 - all_join['l_discount'])

    shipping = all_join[['supp_nation', 'cust_nation', 'l_year', 'volume']]

    result = shipping.groupby(['supp_nation', 'cust_nation', 'l_year'], as_index=False) \
        .agg(revenue=('volume', 'sum'))

    return result