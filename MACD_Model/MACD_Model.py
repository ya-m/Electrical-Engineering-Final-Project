##############################
# My Model is based on MACD #
##############################

import pandas_datareader as web
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys


##### functions #####

def personal_info_page():
    def get_entry_fields():
        global user_first_name
        global user_last_name
        user_first_name = t1.get()
        user_last_name = t2.get()

        msg_box = tk.messagebox.askquestion(title='Investment Simulator',
                                            message='Welcome {} {}!\nDo you wish to proceed?'.format(user_first_name,
                                                                                                     user_last_name))

        if msg_box == 'yes':
            master.destroy()
        else:
            exit_program()

    def exit_program():
        master.destroy()
        sys.exit()

    master = tk.Tk()

    master.title('Welcome to the Investment Simulator')
    master.geometry("500x300+10+10")
    master.config(bg='#9FE2BF')

    lbl_fill_form = tk.Label(master, text='Please Fill Your Personal Information', bg='#9FE2BF', font='bold')
    lbl_fill_form.place(x=100, y=50)

    lbl1 = tk.Label(master, text='First name:', bg='#9FE2BF')
    lbl2 = tk.Label(master, text='Last name:', bg='#9FE2BF')
    t1 = tk.Entry(master, bg='white')
    t1.insert(END, 'Yariv')
    t1.pack()
    t2 = tk.Entry(master, bg='white')
    t2.insert(END, 'Mizrahi')
    t2.pack()

    lbl1.place(x=100, y=100)
    t1.place(x=200, y=100)
    lbl2.place(x=100, y=150)
    t2.place(x=200, y=150)
    b1 = tk.Button(master, text='Submit', command=get_entry_fields, bg='light green')
    b1.place(x=100, y=200)
    b2 = tk.Button(master, text='Exit', command=exit_program, bg='Salmon')
    b2.place(x=200, y=200)

    tk.mainloop()


def get_stock_requierments_from_user():
    def get_entry_fields():
        global stock_name
        global stock_starting_date
        global stock_end_date
        global stock_investment_value
        global stock_feature_to_predict
        stock_name = t1.get()
        stock_starting_date = t2.get()
        stock_end_date = t3.get()
        stock_investment_value = t4.get()
        stock_feature_to_predict = cb1.get()
        master.destroy()

    def exit_program():
        master.destroy()
        sys.exit()

    master = tk.Tk()

    master.title('Investment Simulator - Add stock to portfolio')
    master.geometry("500x400+10+10")
    master.config(bg='#9FE2BF')

    lbl_fill_form = tk.Label(master, text='Please Fill Your Preferences For Prediction', bg='#9FE2BF', font='bold')
    lbl_fill_form.place(x=100, y=50)

    lbl1 = tk.Label(master, text='Stock Symbol:', bg='#9FE2BF')
    lbl2 = tk.Label(master, text='Starting Date:', bg='#9FE2BF')
    lbl3 = tk.Label(master, text='End Date:', bg='#9FE2BF')
    lbl4 = tk.Label(master, text='Investment amount:', bg='#9FE2BF')
    lbl5 = tk.Label(master, text='Parameter to predict:', bg='#9FE2BF')
    t1 = tk.Entry(master, bg='white')
    t1.insert(END, 'AAPL')
    t2 = tk.Entry(master, bg='white')
    t2.insert(END, '2020-01-01')
    t3 = tk.Entry(master, bg='white')
    t3.insert(END, '2021-01-01')
    t4 = tk.Entry(master, bg='white')
    t4.insert(END, '100000')
    cb1 = ttk.Combobox(master, width=27)
    cb1['values'] = ('Open',
                     'Close',
                     'Volume',
                     'Adj Close',
                     'High',
                     'Low')
    cb1.grid(column=1, row=6)
    cb1.current(1)
    lbl1.place(x=100, y=100)
    t1.place(x=250, y=100)
    lbl2.place(x=100, y=150)
    t2.place(x=250, y=150)
    lbl3.place(x=100, y=200)
    t3.place(x=250, y=200)
    lbl4.place(x=100, y=250)
    t4.place(x=250, y=250)
    lbl5.place(x=100, y=300)
    cb1.place(x=250, y=300)
    b1 = tk.Button(master, text='Submit', command=get_entry_fields, bg='light green')
    b1.place(x=100, y=350)
    b2 = tk.Button(master, text='Exit', command=exit_program, bg='Salmon')
    b2.place(x=250, y=350)

    tk.mainloop()


def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span=fast, adjust=False).mean()
    exp2 = price.ewm(span=slow, adjust=False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns={stock_feature_to_predict: 'macd'})
    signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(columns={'macd': 'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns={0: 'hist'})
    frames = [macd, signal, hist]
    df = pd.concat(frames, join='inner', axis=1)
    return df


def plot_macd(prices, macd, signal, hist):
    ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

    ax1.plot(prices)
    ax2.plot(macd, color='grey', linewidth=1.5, label='My Model')
    ax2.plot(signal, color='skyblue', linewidth=1.5, label='SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color='#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color='#26a69a')

    plt.legend(loc='lower right')


def implement_macd_strategy(prices, data):
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)

    return buy_price, sell_price, macd_signal


def get_benchmark(start_date, investment_value):
    spy = web.DataReader('SPY', data_source='yahoo')[stock_feature_to_predict]
    benchmark = pd.DataFrame(np.diff(spy)).rename(columns={0: 'benchmark_returns'})

    investment_value = investment_value
    number_of_stocks = floor(investment_value / spy[-1])
    benchmark_investment_ret = []

    for i in range(len(benchmark['benchmark_returns'])):
        returns = number_of_stocks * benchmark['benchmark_returns'][i]
        benchmark_investment_ret.append(returns)

    benchmark_investment_ret_df = pd.DataFrame(benchmark_investment_ret).rename(columns={0: 'investment_returns'})
    return benchmark_investment_ret_df


##### Start of main code #####

user_first_name = ''
user_last_name = ''
stock_name = ''
stock_starting_date = ''
stock_end_date = ''
stock_feature_to_predict = ''
stock_investment_value = ''

personal_info_page()
get_stock_requierments_from_user()

# Set defaults in case user didn't put data
if (user_first_name == ''):
    user_first_name = 'Yariv'
if (user_last_name == ''):
    user_last_name = 'Mizrahi'
if (stock_name == ''):
    stock_name = 'AAPL'
if (stock_starting_date == ''):
    stock_starting_date = '2020-01-01'
if (stock_end_date == ''):
    stock_end_date = '2021-01-01'
if (stock_feature_to_predict == ''):
    stock_feature_to_predict = 'Close'
if (stock_investment_value == ''):
    stock_investment_value = 100000
else:
    stock_investment_value = float(stock_investment_value)

#####
plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

#####
googl = web.DataReader(stock_name, data_source='yahoo', start=stock_starting_date, end=stock_end_date)
googl
googl.shape

#####
googl_macd = get_macd(googl[stock_feature_to_predict], 26, 12, 9)
googl_macd

#####
plot_macd(googl[stock_feature_to_predict], googl_macd['macd'], googl_macd['signal'], googl_macd['hist'])

#####
buy_price, sell_price, macd_signal = implement_macd_strategy(googl[stock_feature_to_predict], googl_macd)

ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=4, colspan=1)
ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

ax1.plot(googl[stock_feature_to_predict], color='skyblue', linewidth=2, label=stock_name)
ax1.plot(googl.index, buy_price, marker='^', color='green', markersize=10, label='BUY SIGNAL', linewidth=0)
ax1.plot(googl.index, sell_price, marker='v', color='r', markersize=10, label='SELL SIGNAL', linewidth=0)
ax1.legend()
ax1.set_title('Order by My Model for {} stock'.format(stock_name))
ax2.plot(googl_macd['macd'], color='grey', linewidth=1.5, label='My Model')
ax2.plot(googl_macd['signal'], color='skyblue', linewidth=1.5, label='SIGNAL')

for i in range(len(googl_macd)):
    if str(googl_macd['hist'][i])[0] == '-':
        ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color='#ef5350')
    else:
        ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color='#26a69a')

plt.legend(loc='lower right')
plt.show()

position = []
for i in range(len(macd_signal)):
    if macd_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len(googl[stock_feature_to_predict])):
    if macd_signal[i] == 1:
        position[i] = 1
    elif macd_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i - 1]

macd = googl_macd['macd']
signal = googl_macd['signal']
close_price = googl[stock_feature_to_predict]
macd_signal = pd.DataFrame(macd_signal).rename(columns={0: 'macd_signal'}).set_index(googl.index)
position = pd.DataFrame(position).rename(columns={0: 'macd_position'}).set_index(googl.index)

frames = [close_price, macd, signal, macd_signal, position]
strategy = pd.concat(frames, join='inner', axis=1)

strategy

googl_ret = pd.DataFrame(np.diff(googl[stock_feature_to_predict])).rename(columns={0: 'returns'})
macd_strategy_ret = []

for i in range(len(googl_ret)):
    try:
        returns = googl_ret['returns'][i] * strategy['macd_position'][i]
        macd_strategy_ret.append(returns)
    except:
        pass

macd_strategy_ret_df = pd.DataFrame(macd_strategy_ret).rename(columns={0: 'macd_returns'})

number_of_stocks = floor(stock_investment_value / googl[stock_feature_to_predict][-1])
macd_investment_ret = []

for i in range(len(macd_strategy_ret_df['macd_returns'])):
    returns = number_of_stocks * macd_strategy_ret_df['macd_returns'][i]
    macd_investment_ret.append(returns)

macd_investment_ret_df = pd.DataFrame(macd_investment_ret).rename(columns={0: 'investment_returns'})
total_investment_ret = round(sum(macd_investment_ret_df['investment_returns']), 2)
profit_percentage = floor((total_investment_ret / stock_investment_value) * 100)

benchmark = get_benchmark(stock_starting_date, stock_investment_value)

total_benchmark_investment_ret = round(sum(benchmark['investment_returns']), 2)
benchmark_profit_percentage = floor((total_benchmark_investment_ret / stock_investment_value) * 100)



def print_results(stock_investment_value, stock_name, total_investment_ret, profit_percentage, total_benchmark_investment_ret, benchmark_profit_percentage):
    master = tk.Tk()

    master.title('Investment Simulator')
    master.geometry("600x400+10+10")
    master.config(bg='#9FE2BF')

    lbl_fill_form = tk.Label(master, text='Investment Report', bg='#9FE2BF', font='60px')
    lbl_fill_form.place(x=50, y=30)

    lbl1 = tk.Label(master, text='Profit gained from My Model by investing ${}k in {} : {}'.format(stock_investment_value / 1000, stock_name,
                                                                                                   total_investment_ret), bg='#9FE2BF', font='16px')
    lbl2 = tk.Label(master, text='Profit percentage of My Model : {}%'.format(profit_percentage), bg='#9FE2BF', font='16px')
    lbl3 = tk.Label(master, text='Benchmark profit by investing ${}k : {}'.format(stock_investment_value / 1000, total_benchmark_investment_ret), bg='#9FE2BF', font='16px')
    lbl4 = tk.Label(master, text='Benchmark Profit percentage : {}%'.format(benchmark_profit_percentage), bg='#9FE2BF', font='16px')
    lbl5 = tk.Label(master, text='My Model profit is {}% higher than the Benchmark Profit'.format(
            profit_percentage - benchmark_profit_percentage), bg='#9FE2BF', font='16px')

    lbl1.place(x=50, y=100)
    lbl1.place(x=50, y=100)
    lbl2.place(x=50, y=150)
    lbl3.place(x=50, y=200)
    lbl4.place(x=50, y=250)
    lbl5.place(x=50, y=300)

    tk.mainloop()



print_results(stock_investment_value, stock_name, total_investment_ret, profit_percentage, total_benchmark_investment_ret, benchmark_profit_percentage)
