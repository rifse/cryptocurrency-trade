import math

DATA = {'hitbtc': {'usdt':
    {'price_step': 0.01,
        'lot_size_XVG': 10,
        'lot_size_OCC': 0.1}},
    'binance': {'usdt':
        {'price_step': 0.01,
            'lot_size_ADA': 1,
            'lot_size_ETH': 0.00001}},
            # 'lot_size_ETH': 0.00001}},
    'exmarkets': {'usdt':
        {'price_step': 0.01,
            'lot_size_ADAX': 10}}}
            # 'lot_size_ADAX': 1}}}
     # 'lot_size_OCC': 1}}}
     # 'lot_size_OCC': 0.001}}}

def sell(low, high, min_order, actual_min_order, min_step, amount, max_orders=None):
    quant_n = max_orders*(max_orders+1)/2 if max_orders else None
    quant_size = amount/quant_n if quant_n else None
    # digits = abs(math.floor(math.log(min_order, 10))) if min_order < 1 else 0  # !
    # digits = abs(math.floor(math.log(actual_min_order, 10))) if min_order < 1 else 0  # !
    log10 = math.floor(math.log(min_order, 10))
    digits = abs(log10) if log10 < 0 else 0
    if not max_orders or quant_size < actual_min_order:
        step_n, quant_n = _calculate_steps(int(amount/actual_min_order))
    else:
        actual_min_order = quant_size
        step_n = max_orders
    residue = (amount-(quant_n*actual_min_order))/int(amount/actual_min_order)
    dspread = max((high-low)/(step_n-1), min_step)
    _orders = [[
        i+1, 
        truncate(i*dspread+low),  # price
        round((i+1)*(actual_min_order+residue), digits) if digits > 0 else int((i+1)*(actual_min_order+residue))] for i in range(step_n)]  # amount [base]
        # truncate((i+1)*(actual_min_order))] for i in range(step_n)]
    return _orders

def buy(high, low, min_order, actual_min_order, min_step, amount, max_orders=None):
    quant_n = max_orders*(max_orders+1)/2 if max_orders else None
    quant_size = amount/quant_n if quant_n else None
    # base_min_order = quant_size if quant_size else high*min_order
    base_min_order = max(quant_size, high*actual_min_order) if quant_size else high*actual_min_order
    log10 = math.floor(math.log(min_order, 10))
    digits = abs(log10) if log10 < 0 else 0
    if not max_orders or quant_size < min_order:
        step_n, quant_n = _calculate_steps(int(amount/base_min_order))
        residue = (amount-(quant_n*base_min_order))/int(amount/base_min_order)
    else:
        step_n = max_orders
        residue = 0
    dspread = max((high-low)/(step_n-1), min_step)
    _orders = [[
        i+1, 
        truncate(high-i*dspread),  # price
        round((i+1)*(base_min_order+residue)/(high-i*dspread), digits) if digits > 0 else int((i+1)*(base_min_order+residue)/(high-i*dspread)),  # cost [quote]
        # round((i+1)*(base_min_order+residue), digits) if digits > 0 else int((i+1)*(base_min_order+residue))] for i in range(step_n)]  # amount of coin to buy [base]
        truncate((i+1)*(base_min_order+residue))] for i in range(step_n)]  # cost
    return _orders

# def buy(high, low, min_order, min_step, amount, max_orders=None):
#     quant_n = max_orders*(max_orders+1)/2 if max_orders else None
#     quant_size = amount/quant_n if quant_n else None
#     base_min_order = quant_size if quant_size else high*min_order
#     if not max_orders or quant_size < min_order:
#         step_n, quant_n = _calculate_steps(int(amount/base_min_order))
#         residue = (amount-(quant_n*base_min_order))/int(amount/base_min_order)
#     else:
#         step_n = max_orders
#         residue = 0
#     dspread = max((high-low)/(step_n-1), min_step)
#     _orders = [[
#         i+1, 
#         truncate(high-i*dspread),  # price
#         truncate((i+1)*(base_min_order+residue)),  # cost
#         truncate((i+1)*(base_min_order+residue)/(high-i*dspread))] for i in range(step_n)]  # amount of coin to buy
#     return _orders

def _calculate_steps(max_sum):
    s, i = 0, 0
    while s <= max_sum:
        i += 1
        s += i
        # print(i, s)
    return i-1, s-i

def truncate(number, relevant_digits=4):
    '''sloppy, use decimal type for precision at less than zero? 
    https://stackoverflow.com/questions/13479163/round-float-to-x-decimals.'''
    log10 = math.floor(math.log(number, 10))
    if log10 < 0:
        # number = '{0:.{precision}f}'.format(number, precision=-log10-1+relevant_digits)
        # probably there's a better way but:
        number = float('{0:.{precision}f}'.format(number, precision=-log10-1+relevant_digits))
    else:
        add_digits = (-log10-1) % relevant_digits
        number = round(number, add_digits) if add_digits and log10 < relevant_digits else int(number)
    return number

if __name__ == '__main__':
    # orders = sell(low=0.0287, 
    #              high=0.078, 
    #              min_order=DATA['hitbtc']['usdt']['lot_size_XVG'],
    #              min_step=DATA['hitbtc']['usdt']['price_step'],
    #              amount=500)
    # orders = sell(low=3, 
    #              high=17, 
    #              min_order=DATA['binance']['usdt']['lot_size_ADA'],
    #              min_step=DATA['binance']['usdt']['price_step'],
    #              amount=200)
    # orders = sell(low=3, 
    #              high=64, 
    #              min_order=DATA['exmarkets']['usdt']['lot_size_ADAX'],
    #              min_step=DATA['exmarkets']['usdt']['price_step'],
    #              amount=333)
    orders_s = sell(low=4300, 
                 high=12000, 
                 min_order=DATA['binance']['usdt']['lot_size_ETH'],
                 min_step=DATA['binance']['usdt']['price_step'],
                 max_orders=10,
                 amount=0.11572191)
    orders_b = buy(low=4.5, 
                high=9.1, 
                min_order=DATA['hitbtc']['usdt']['lot_size_OCC'],
                min_step=DATA['hitbtc']['usdt']['price_step'],
                max_orders=18,
                amount=158)
    for i in range(len(orders_s)):
        print(orders_s[i])
    for i in range(len(orders_b)):
        print(orders_b[i])
    pass
# def sell(low, high, min_order, min_step, amount, max_orders=None):
#     n = int(amount/min_order)
#     steps_n, _sum = _calculate_steps(n)
#     # print(steps_n, _sum)    
#     residue = (amount-(_sum*min_order))/n
#     # print(residue)
#     dspread = max((high-low)/(steps_n-1), min_step)
#     _orders = [[
#         i+1, 
#         truncate(i*dspread+low), 
#         truncate((i+1)*(min_order+residue))] for i in range(steps_n)]
#     for i in range(steps_n): # asf 0, 
#         print(f'{i+1}, price={i*dspread+low}, amount={(i+1)*(min_order+residue)}')
#     return _orders

# def buy(high, low, min_order, min_step, amount, max_orders=None):
#     base_min_order = high*min_order
#     n = int(amount/base_min_order)
#     steps_n, _sum = _calculate_steps(n)
#     # print(steps_n, _sum)
#     residue = (amount-(_sum*base_min_order))/n
#     # print(residue)
#     dspread = max((high-low)/(steps_n-1), min_step)
#     _orders = [[
#         i+1, 
#         truncate(high-i*dspread), 
#         truncate((i+1)*(base_min_order+residue)), 
#         truncate((i+1)*(base_min_order+residue)/(high-i*dspread))] for i in range(steps_n)]
#     return _orders
