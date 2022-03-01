import os
import pandas as pd

calls = 'call_options'
puts = 'put_options'

while True:
    date_input = str(input("Please enter a date in format mm/dd/yyyy or Q to quit: "))
    if date_input == 'Q':
        break
    date_input_array = date_input.split("/")
    if (len(date_input_array[0]) == 1):
        date_input_array[0] = "0" + date_input_array[0]
    if (len(date_input_array[1]) == 1):
        date_input_array[1] = "0" + date_input_array[1]
    file_date = date_input_array[2] + "-" + date_input_array[0] + "-" + date_input_array[1]
    dateExists = False
    try:
        for file_name in os.listdir(calls):
            if file_date in file_name:
                dateExists = True
                break
        for file_name in os.listdir(puts):
            if file_date in file_name:
                dateExists = True
                break
        if (dateExists == False): raise Exception("-----------------------\nERROR: Date does not exist in files, please try another date\n-----------------------")
    except Exception as E:
        print(E)
    else:
        while True:
            ticker_input = str(input("Please enter a ticker you want to parse or Q to quit: "))
            if ticker_input == 'Q':
                break
            option_type = str(input("Do you want to explore call options? (Y/y) or (N/n) for puts: "))
            file_name = file_date + "_" + ticker_input
            if option_type == 'Y' or option_type == 'y':
                try:
                    file_name = "call_options/" + file_name + "_C.csv"
                    calls_dataframe = pd.read_csv(file_name, sep=',')
                    print("///////////////////////////////////////////////////")
                    print("Total volume: " + str(calls_dataframe['volume'].sum()))
                    total_calls = calls_dataframe['contractSymbol'].count()
                    print("Total options: " + str(total_calls))
                    #Bought at or below bid
                    atOrBelowBid = ((calls_dataframe['lastPrice'] <= calls_dataframe['bid']).value_counts())
                    #Count of true values
                    print("Bought at or below bid: " + str((atOrBelowBid.get(key=True))))
                    print("Percentage of total: " + str(round((atOrBelowBid.get(key=True)) / total_calls * 100, 2)) + "%")
                    #Bought at ask or above
                    atOrAboveAsk = ((calls_dataframe['lastPrice'] >= calls_dataframe['ask']).value_counts())
                    #Count of True values
                    print("Bought at or above ask: " + str(atOrAboveAsk.get(key=True)))
                    print("Percentage of total: " + str(round((atOrAboveAsk.get(key=True)) / total_calls * 100, 2)) + "%")
                    #Between the market
                    betweenTheMarket = ((calls_dataframe['lastPrice'] > calls_dataframe['bid']) & (calls_dataframe['lastPrice'] < calls_dataframe['ask'])).value_counts()
                    print("Bought between market (at price between bid and ask): " + str(betweenTheMarket.get(key=True)))
                    print("Percentage of total: " + str(round((betweenTheMarket.get(key=True)) / total_calls * 100, 2)) + "%")
                    print("///////////////////////////////////////////////////")


                except:
                    print(f'-----------------------\nERROR: Ticker {ticker_input} does not exist, cannot open file\n-----------------------')
            else:
                try:
                    file_name = "put_options/" + file_name + "_P.csv"
                    puts_dataframe = pd.read_csv(file_name, sep=',')
                    print("Total volume: " + str(puts_dataframe['volume'].sum()))
                    #Bought at or below bid
                    print()

                except:
                    print(f'ERROR: Ticker {ticker_input} does not exist, cannot open file') 

#for f in os.listdir(calls):
#    file = 'call_options/' + f
#    if os.path.isfile(file):
#        file