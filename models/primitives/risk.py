from pprint import pprint
import numpy as np
import pandas as pd

parameters = {'btc': [-4.26138127, 5.14290383, 3.65932922, 0.09989763],
              'eth': [-3.98104476, 4.74731142, 2.14279409, 0.07926272],
              'neo': [-4.56053475, 5.28758755, 0.76027031, 0.09514826],
              'silver': [-5.44776679, 6.50969391, 1.01492414, 0.06758493],
              'gold': [-4.39166439, 5.40363846, 2.51219638, 0.07074411],
              # 'hbar1': [-4.63017041, 5.26617661, -2.10760802, 0.12334456],
              'hbar': [-2.86516426, 3.69439744, -1.79452064, 0.12776717],
              'ada': [-3.31348853, 4.06018421, -1.82649535, 0.09174109],
              'xrp': [-4.68090744, 5.2995862, -1.14670791, 0.08105529],
              'link_log1': [-4.59545104, 5.42525238, 0.48593899, 0.11342292],
              'link_log2': [-4.94747835, 4.90449262, -0.52376317, 0.20489514],
              'link_para1': [-4.58818713, 5.41476566, 0.53046864, 0.16859701]}

def priceCalc(x, a, b, c, d):
    return 10**(((x - a)/b)**(1/d) + c)

risks = pd.DataFrame({'risk': np.divide(np.arange(0, 401), 4)})  # np.arange(i) = list(range(i))
for coin in parameters:
    risks[coin] = [priceCalc(x/100.0, *parameters[coin]) for x in risks.risk]

risks.set_index('risk', inplace=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 163):  # more options can be specified also
    print(risks)
