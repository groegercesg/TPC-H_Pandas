import pandas as pd

def q6(lineitem):
    var1 = '1994-01-01'
    var2 = '1995-01-01'
    var3 = 0.05
    var4 = 0.07
    var5 = 24

    li_filt = lineitem[
        (lineitem.l_shipdate >= var1) &
        (lineitem.l_shipdate < var2) &
        (lineitem.l_discount >= var3) &
        (lineitem.l_discount <= var4) &
        (lineitem.l_quantity < var5)
        ]

    li_filt['revenue'] = li_filt.l_extendedprice * li_filt.l_discount

    result = li_filt.agg({'revenue': 'sum'})

    return result