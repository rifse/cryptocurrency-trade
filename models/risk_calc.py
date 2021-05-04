# import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

class Calculator:

    @staticmethod
    def predictor_log(x, a, b, c, d):
        # represents a generic logarithm: y = b*((log_d)(x - c)) + a  
        return a+b*np.log2(x-c)/np.log2(d)

    @staticmethod
    def predictor_lin(x, k, n):
        return k*x+n

    @staticmethod
    def predictor_exp(x, a, b, c):
        return np.exp(a*x+b)+c
        # return np.exp(Calculator.predictor_lin(x, a, b)) + c

    @staticmethod
    def normalize_vector(vector):
        norm = np.abs(vector.min()) if np.abs(vector.min()) > vector.max() else vector.max()
        return np.divide(vector, norm)

class Data:
    # (price-log)/log
    # log(price/20wMA)
    def __init__(self, history_file='../data/btc-usd.csv'):
        self.history = self.convertHistory(history_file)
        # self.calculate_log_Closes()
        # self.logReg_curveFit(logReg_accuracy)
        ##self.movingAverages_get(movingAverages)
        ##self.calculate_quotients([[movingAverages[0], movingAverages[1]]], plus_log=True) # self.calculate_logarithmQuotients([self.MA_1, self.MA_2])
        # self.calculate_log_priceDivByMA(movingAverages[2])

    # @staticmethod
    def convertHistory(self, file_csv_dir):
        history = pd.read_csv(file_csv_dir, comment='#')

        # df['index'] = df.index
        # df.set_index('Date', inplace=True)
        history['day'] = history.Timestamp

        # history['day_sinceD1'] = (pd.Timestamp(history.day)-pd.Timestamp(history.day.iloc[0,:])).days
        history['close'] = history.Close
        history['close_log'] = np.log10(history.close)
        return history[['day', 'close', 'close_log']]
        # self.history = history[['day', 'close', 'close_log']]

    def plotLoga(self, data_columns=['close_log'], right_yAxis=False, right_columns=None):  # right_columns=['risk00']
        months = pd.to_datetime(self.history.day, format='%Y-%m-%d %H:%M:%S.%f')
        history_toPlot = self.history.set_index(months, inplace=False)
        for column in data_columns:
            history_toPlot[column].plot()
        if right_yAxis:
            for column in right_columns:
                history_toPlot[column].plot(secondary_y=True, x_compat=True)
        plt.legend(loc='best')
        plt.show()

class Simple(Data):

    def __init__(self, history_file, moving_averages=[50, 350]):
        super().__init__(history_file)
        self.getMovingAverages(moving_averages)
        self.getQuotients([[moving_averages[0], moving_averages[1]]], plus_loga=True)

    def getMovingAverages(self, moving_averages):
        self.moving_averages = moving_averages
        for days in moving_averages:
            self.history['MA-{}'.format(days)] = self.history.close.astype(float).rolling(window=days).mean()

    def getQuotients(self, quotient_pairs, plus_loga=True):
        for pair in quotient_pairs:
            MA_0 = pair[0]
            MA_1 = pair[1]
            quotient = np.divide(self.history['MA-{}'.format(MA_0)], self.history['MA-{}'.format(MA_1)])
            self.history['quotient-{}_{}'.format(MA_0, MA_1)] = quotient
            if plus_loga:
                self.history['log-quotient-{}_{}'.format(MA_0, MA_1)] = np.log10(quotient)

    def getRisk(self, plot=False):
        risk = self.history['log-quotient-{}_{}'.format(self.moving_averages[0], self.moving_averages[1])]
        min_el = risk.min(skipna=True)

        risk = risk + np.abs(min_el)
        self.history['maybeBetter'] = Calculator.normalize_vector(risk)
        if plot:
            self.history['simpleRisk'] = Calculator.normalize_vector(self.history['quotient-{}_{}'.format(self.moving_averages[0], self.moving_averages[1])])
            self.plotLoga(right_yAxis=True, right_columns=['simpleRisk', 'maybeBetter'])

class RevEng(Data):

    def __init__(self, history_file, moving_averages=[50, 350]):
        super().__init__(history_file)

    def cowen_relInd_1(self, plot=False):
        # indicator = (self.history.close_log-self.history.LR_bottom)/abs(self.history.LR_bottom)
        # indicator = (self.history.close-np.power(10, self.history.LR_bottom))/np.power(10, self.history.LR_bottom)
        indicator = (self.history.close-np.power(10, self.history.LR_cowen))/np.power(10, self.history.LR_cowen)
        self.history['indicator_1'] = np.log10(abs(indicator))
        # self.history['indicator_1'] = indicator
        if plot:
            self.plot_log(['indicator_1'])

    def getRisk_00(self, plot=False):
        # risk = self.history['log-quotient-{}_{}'.format(self.movingAverages[0], self.movingAverages[1])]
        risk = self.history['quotient-{}_{}'.format(self.movingAverages[0], self.movingAverages[1])]
        # # risk = np.multiply(risk, self.history.indicator_1)
        # print(risk.min(skipna=True))
        min_el = risk.min(skipna=True)

        # risk = risk + np.abs(min_el)
        self.history['risk00'] = Calculator.normalize_vector(risk)
        # self.history['risk00'] = risk
        if plot:
            self.plot_log(right_yAxis=True, right_columns=['risk00'])
        # risk_proto = self.normalize_vector(self.history['quotient_{}_{}'.format(MA_1, MA_2)])
        # risk_proto = np.multiply(risk_proto, self.history['logarithm_priceByMA_{}'.format(MA_3)])
        # # self.history['risk_6'] = (risk_proto + 1)/2
        # self.history['risk_00'] = risk_proto

    def LR_basic(self, accuracy=0.001, approx4cowen=False, plot=False):
        theFit, something = curve_fit(Calculator.predictor_log, self.history.index, self.history.close_log, bounds=([-np.inf, -np.inf, -np.inf, 10**(-15)],
                                                                                                                    [np.inf, np.inf, 0, np.inf]))
        a, b, c, d = theFit
        a_bu, b_bu, c_bu, d_bu = a, b, c, d
        LR_first = np.multiply(np.divide(np.log10(self.history.index-c), np.log10(d)), b) + a
        norm = 1
        LR_last = LR_first
        while norm > accuracy:
            history_new = self.history.loc[self.history['close_log'] < LR_last]
            theFit, something = curve_fit(Calculator.predictor_log, history_new.index, history_new.close_log, p0=[a, b, c, d], bounds=([-np.inf, -np.inf, -np.inf, 0],
                                                                                                                                       [np.inf, np.inf, 0, np.inf]))
            a, b, c, d = theFit
            LR_new = np.multiply(np.divide(np.log10(self.history.index-c), np.log10(d)), b) + a
            norm = abs((LR_new - LR_last)).max()
            # print('NORM (bottom): {}'.format(norm))
            LR_last = LR_new
        print(f'LR_bottom params: a={a}, b={b}, c={c}, d={d}')
        self.history['LR_bottom'] = LR_last
        norm = 1
        LR_last = LR_first
        a, b, c, d = a_bu, b_bu, c_bu, d_bu
        while norm > accuracy:
            history_new = self.history.loc[self.history['close_log'] > LR_last]
            theFit, something = curve_fit(Calculator.predictor_log, 
                                          history_new.index, 
                                          history_new.close_log, 
                                          p0=[a, b, c, d], 
                                          bounds=([-np.inf, -np.inf, -np.inf, 0],
                                          [np.inf, np.inf, 0, np.inf]))                                                                                                                                
            a, b, c, d = theFit
            LR_new = np.multiply(np.divide(np.log10(self.history.index-c), np.log10(d)), b) + a
            norm = abs((LR_new - LR_last)).max()
            # print('NORM (top): {}'.format(norm))
            LR_last = LR_new
        print(f'LR_top params: a={a}, b={b}, c={c}, d={d}')
        self.history['LR_top'] = LR_last
        if approx4cowen:
            x = 1./5.1
            y = 1-x
            self.history['LR_cowen'] = x*self.history['LR_top']+y*self.history['LR_bottom']
        if plot:
            self.plot_log(['close_log', 'LR_bottom', 'LR_top'])

    def LR_lowHigh(self, accuracy=0.001, plot=False):
        theFit, something = curve_fit(Calculator.predictor_log, self.history.index, self.history.close_log, bounds=(-np.inf, [np.inf, np.inf, 0]))
        a, b, c = theFit
        a_bu, b_bu, c_bu = a, b, c
        LR_first = np.multiply(np.log10(self.history.index-c), b) + a
        norm = 1
        LR_last = LR_first
        # y_toFit = np.log10(self.history.low)
        while norm > accuracy:
            # y_toFit = y_toFit.loc[y_toFit['low'] < LR_last]
            history_new = self.history.loc[self.history['close_log'] < LR_last]
            theFit, something = curve_fit(self.predictor_log, history_new.index, history_new.close_log, p0=[a, b, c], bounds=(-np.inf, [np.inf, np.inf, 0]))
            a, b, c = theFit
            LR_new = np.multiply(np.log10(self.history.index-c), b) + a
            norm = abs((LR_new - LR_last)).max()
            # print('NORM (bottom): {}'.format(norm))
            LR_last = LR_new
        self.history['LR_bottom'] = LR_last
        norm = 1
        LR_last = LR_first
        a, b, c = a_bu, b_bu, c_bu
        while norm > accuracy:
            history_new = self.history.loc[self.history['close_log'] > LR_last]
            theFit, something = curve_fit(Calculator.predictor_log, history_new.index, history_new.close_log, p0=[a, b, c], bounds=(-np.inf, [np.inf, np.inf, 0]))
            a, b, c = theFit
            LR_new = np.multiply(np.log10(self.history.index-c), b) + a
            norm = abs((LR_new - LR_last)).max()
            # print('NORM (top): {}'.format(norm))
            LR_last = LR_new
        self.history['LR_top'] = LR_last
        if plot:
            self.plot_log(['close_log', 'LR_bottom', 'LR_top'])

    def LR_cowen(self, nonBubble_fit=True, plot=False):
        if nonBubble_fit:
            history = self.history
            history['index_bu'] = history.index
            history.day = pd.to_datetime(history.day)
            history = history.set_index(['day'], inplace=False)
            history = history.sort_index()
            h1 = history.loc['2010-07-25':'2010-10-07']  # aug-sep start is 2010-07-18
            h2 = history.loc['2010-12-05':'2011-04-22']  # nov
            # h3 = history.loc['2011-03-01':'2011-04-01']  # mar
            # h4 = history.loc['2011-08-01':'2011-12-01']  # aug-nov
            h4 = history.loc['2011-11-18':'2011-12-19']  # aug-nov
            # h5 = history.loc['2012-02-01':'2013-04-01']  # feb_12-mar_13
            h5 = history.loc['2012-02-19':'2013-02-13']  # feb_12-mar_13
            # h6 = history.loc['2015-01-14':'2017-06-01']  # jan_15-may_17
            h6 = history.loc['2015-01-14':'2017-06-01']  # jan_15-may_17
            # h7 = history.loc['2018-07-01':'2019-05-01']  # jul_18-apr_19
            h7 = history.loc['2018-12-15':'2019-05-01']  # jul_18-apr_19
            # h8 = history.loc['2019-08-01':'2020-10-01']  # aug_19-sep_20
            # h8 = history.loc['2019-12-17':'2019-02-13']  # korona
            h8 = history.loc['2020-03-12':'2020-11-05']
            history = pd.concat([h1, h2, h4, h5, h6, h7, h8])
            # history = pd.concat([h5, h6, h7, h8])
            theFit, something = curve_fit(Calculator.predictor_log, history.index_bu, history.close_log, 
                                          bounds=([-np.inf, -np.inf, -np.inf, 10**(-15)],
                                          [np.inf, np.inf, 0, np.inf]))                                                                    
            a, b, c, d = theFit
            LR_last = np.multiply(np.divide(np.log10(self.history.index-c), np.log10(d)), b) + a
            del self.history['index_bu']
        else:
            LR_last = self.history['close_log']+1
            for i in range(2):
                history_new = self.history.loc[self.history['close_log'] < LR_last]
                theFit, something = curve_fit(Calculator.predictor_log, 
                                              history_new.index, 
                                              history_new.close_log, 
                                              bounds=([-np.inf, -np.inf, -np.inf, 10**(-15)],
                                              [np.inf, np.inf, 0, np.inf]))                                                  
                a, b, c, d = theFit
                LR_last = np.multiply(np.divide(np.log10(self.history.index-c), np.log10(d)), b) + a
        print(f'LR_cowen params: a={a}, b={b}, c={c}, d={d}')
        self.history['LR_cowen'] = LR_last
        if plot:
            self.plot_log(['close_log', 'LR_cowen'])

    def normalizeByDescendingFit(self, column):
        pass



if __name__ == '__main__':
    dataHandler = Simple('../data/btc-usd.csv', [50, 350])
    # dataHandler.LR_basic()  # approx4cowen=True)
    ## dataHandler.LR_cowen()  # nonBubble_fit=True)  # , plot=True)
    # toPrintWhole = dataHandler.history.loc[(dataHandler.history['quotient_50_350_log'] < 0) & (dataHandler.history['LR_cowen'] < 0)]
    ## toPrintWhole = dataHandler.history.loc[(dataHandler.history['LR_cowen'] < 0)]
    # dataHandler.cowen_relInd_1()  #plot=True)
    dataHandler.getRisk(plot=True)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(dataHandler.history)
    #     # print(toPrintWhole)
