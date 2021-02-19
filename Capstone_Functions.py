import time
import pickle
from sklearn import linear_model

reg = linear_model.LinearRegression()

# Function to predict splits via linear regression from user input converted to seconds
def calc_splits(input_in_seconds):

    df = pickle.load(open("model.pkl", "rb"))

    reg_five = linear_model.LinearRegression()
    reg_five.fit(df[['official_time']], df.five_k)
    
    reg_ten = linear_model.LinearRegression()
    reg_ten.fit(df[['official_time']], df.ten_k)
    
    reg_fifteen = linear_model.LinearRegression()
    reg_fifteen.fit(df[['official_time']], df.fifteen_k)
    
    reg_twenty = linear_model.LinearRegression()
    reg_twenty.fit(df[['official_time']], df.twenty_k)
    
    reg_half = linear_model.LinearRegression()
    reg_half.fit(df[['official_time']], df.half)
    
    reg_twentyfive = linear_model.LinearRegression()
    reg_twentyfive.fit(df[['official_time']], df.twentyfive_k)
    
    reg_thirty = linear_model.LinearRegression()
    reg_thirty.fit(df[['official_time']], df.thirty_k)
    
    reg_thirtyfive = linear_model.LinearRegression()
    reg_thirtyfive.fit(df[['official_time']], df.thirtyfive_k)
    
    reg_forty = linear_model.LinearRegression()
    reg_forty.fit(df[['official_time']], df.forty_k)

    # Predicts the split
    # Must be treated as an array
    # output type of reg.xyz is an array, so must access first value of array
        # only one value per array
    # round(fivek_arr[0]) rounds value to closest integer
    fivek_arr = reg_five.predict([[input_in_seconds]]).astype(float)
    
    tenk_arr = reg_ten.predict([[input_in_seconds]]).astype(float)
    
    fifteenk_arr = reg_fifteen.predict([[input_in_seconds]]).astype(float)
    
    twentyk_arr = reg_twenty.predict([[input_in_seconds]]).astype(float)
    
    half_arr = reg_half.predict([[input_in_seconds]]).astype(float)
    
    twentyfivek_arr = reg_twentyfive.predict([[input_in_seconds]]).astype(float)
    
    thirtyk_arr = reg_thirty.predict([[input_in_seconds]]).astype(float)
    
    thirtyfivek_arr = reg_thirtyfive.predict([[input_in_seconds]]).astype(float)
    
    fortyk_arr = reg_forty.predict([[input_in_seconds]]).astype(float)
    
    # convert int seconds to HH:MM:SS format
    splits_arr = [time.strftime('%H:%M:%S', time.gmtime(round(fivek_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(tenk_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(fifteenk_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(twentyk_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(half_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(twentyfivek_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(thirtyk_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(thirtyfivek_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(round(fortyk_arr[0]))),
    time.strftime('%H:%M:%S', time.gmtime(input_in_seconds))]

    return splits_arr

# Returns an array of values in seconds to be plotted on line graph
def splits_in_seconds(input_in_seconds):
    df = pickle.load(open("model.pkl", "rb"))

    # linear regression for finish time against all splits
    reg_five = linear_model.LinearRegression()
    reg_five.fit(df[['official_time']], df.five_k)

    reg_ten = linear_model.LinearRegression()
    reg_ten.fit(df[['official_time']], df.ten_k)

    reg_fifteen = linear_model.LinearRegression()
    reg_fifteen.fit(df[['official_time']], df.fifteen_k)

    reg_twenty = linear_model.LinearRegression()
    reg_twenty.fit(df[['official_time']], df.twenty_k)

    reg_half = linear_model.LinearRegression()
    reg_half.fit(df[['official_time']], df.half)

    reg_twentyfive = linear_model.LinearRegression()
    reg_twentyfive.fit(df[['official_time']], df.twentyfive_k)

    reg_thirty = linear_model.LinearRegression()
    reg_thirty.fit(df[['official_time']], df.thirty_k)

    reg_thirtyfive = linear_model.LinearRegression()
    reg_thirtyfive.fit(df[['official_time']], df.thirtyfive_k)

    reg_forty = linear_model.LinearRegression()
    reg_forty.fit(df[['official_time']], df.forty_k)

    # Predicts the split
    # Must be treated as an array
    # output type of reg.xyz is an array, so must access first value of array
    # only one value per array
    # round(fivek_arr[0]) rounds value to closest integer
    fivek_arr = reg_five.predict([[input_in_seconds]]).astype(float)

    tenk_arr = reg_ten.predict([[input_in_seconds]]).astype(float)

    fifteenk_arr = reg_fifteen.predict([[input_in_seconds]]).astype(float)

    twentyk_arr = reg_twenty.predict([[input_in_seconds]]).astype(float)

    half_arr = reg_half.predict([[input_in_seconds]]).astype(float)

    twentyfivek_arr = reg_twentyfive.predict([[input_in_seconds]]).astype(float)

    thirtyk_arr = reg_thirty.predict([[input_in_seconds]]).astype(float)

    thirtyfivek_arr = reg_thirtyfive.predict([[input_in_seconds]]).astype(float)

    fortyk_arr = reg_forty.predict([[input_in_seconds]]).astype(float)

    splits_in_seconds_arr = [round(fivek_arr[0]), round(tenk_arr[0]), round(fifteenk_arr[0]), round(twentyk_arr[0]),
                             round(half_arr[0]), round(twentyfivek_arr[0]), round(thirtyk_arr[0]),
                             round(thirtyfivek_arr[0]),round(fortyk_arr[0]), round(input_in_seconds)]

    return splits_in_seconds_arr

# Returns a list to be used for plotting the scatter plot
def get_scatter(input_in_seconds):

    df = pickle.load(open("model.pkl", "rb"))

    df = df.drop(columns=['pace'])

    partial_set = df[df['official_time'] < input_in_seconds].tail(10)
    partial_indexes = []
    # Gets up to next 10 runners splits and stores the pandas index into a list
    # For example, if user enters 3:00:00 as projected finish time, will pull next 10 runners that ran just under 3 hrs
    for row in partial_set.iterrows():
        partial_indexes.append(row[0])

    # x = ['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Final']
    y = [[], [], [], [], [], [], [], [], [], []]

    # Loop to get and store splits of the up to previous 10 racers times
    j = -1
    while j < len(partial_indexes) - 1:
        j += 1

        i = -1
        while i < 9:
            i += 1
            y[i].append(partial_set.at[partial_indexes[j], partial_set.columns[i]])

    return y