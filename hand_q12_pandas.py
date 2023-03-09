import pandas as pd

def q12(orders, lineitem):
    var1 = ('MAIL', 'SHIP')
    var2 = '1994-01-01'
    var3 = '1995-01-01'

    li_filt = lineitem[lineitem['l_shipmode'].isin(var1) &
                       (lineitem['l_commitdate'] < lineitem['l_receiptdate'])
                       & (lineitem['l_shipdate'] < lineitem['l_commitdate'])
                       & (lineitem['l_receiptdate'] >= var2) & (lineitem['l_receiptdate'] < var3)]

    li_ord_join = orders.merge(li_filt, left_on='o_orderkey', right_on='l_orderkey')

    li_ord_join['high_line_priority'] = li_ord_join.apply(
        lambda x: 1 if ((x['o_orderpriority'] == '1-URGENT') | (x['o_orderpriority'] == '2-HIGH')) else 0,
        axis=1)

    li_ord_join['low_line_priority'] = li_ord_join.apply(
        lambda x: 1 if ((x['o_orderpriority'] != '1-URGENT') & (x['o_orderpriority'] != '2-HIGH')) else 0,
        axis=1)

    result = li_ord_join.groupby(['l_shipmode'], as_index=False) \
        .agg(high_line_count=('high_line_priority', 'sum'),
             low_line_count=('low_line_priority', 'sum'))

    return result