import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chi': 'chicago.csv',
              'new': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'was': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Are you interested in Chicago, New York City or Washington?   \n>').lower()[:3]
    while city != 'chi' and city != 'new' and city != 'was' and city != 'nyc':
        city = input('I don\'t recognise that city. Please enter one of Chicago, New York City or Washington\n>')
                     

    # get user input for month (all, january, february, ... , june)
    month = input('Do you want to filter by month? Enter a month between January and June, or type "all".  \n>').lower()[:3]
    while month not in  ['jan','feb','mar','apr','may','jun','all']:
        month = input('Not a valid input! Please enter either "all" or a month between January and June.\n>')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Do you want to filter by day of the week? Enter the name of a day or type 'all'\n>").lower()
    day = day[:3]
    days = ['mon','tue','wed','thu','fri','sat','sun']
    while day not in days and day != 'all':
        day = input('Not a valid input! Please enter either "all" or the name of a day of the week.\n>')
    confirmation = "Calculating data for "+city.upper()+" for month <"+month.upper()+"> and day of week <"+day.upper()+">" 
    if day != 'all':
        day = days.index(day)
    
    print('-'*40)
    #print(day)
    
    return city, month, day, confirmation


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]
    #print(df)

    return df


def time_stats(df, confirmation):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('\n'+confirmation)
    # display the most common month
    #if len(df['month'].unique()) > 1:
    common_month = df['month'].mode()
    print("The month with the most trips was: "+str(months[common_month.iat[0]-1].title()))
    #print(df('month').value_counts())

    # display the most common day of week``
    if len(df['day_of_week'].unique()) > 1:
        print("\nThe day of the week with the most trips was: "+str(days[df['day_of_week'].mode().iat[0]]))

    #display the most common start hour
        df['start_hour'] = df['Start Time'].dt.hour

    print("\nThe most common hour to start a trip was: "+str(df['start_hour'].mode().iat[0])+":00")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most popular starting station was: "+str(df['Start Station'].mode().iat[0]))

    # display most commonly used end station
    print("\nThe most popular destination was: "+str(df['End Station'].mode().iat[0]))

    # display most frequent combination of start station and end station trip
    df['trip_route'] = df['Start Station']+" TO "+df['End Station']
    #trips = df.groupby(['Start Station','End Station'])['End Station'].value_counts()
    
    print("\nThe most popular route was: "+str(df['trip_route'].mode().iat[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total duration of all trips was: "+str(df['Trip Duration'].sum()//3600)+" hours.")

    # display mean travel time
    print("The average trip duration was: "+ str(df['Trip Duration'].mean()//60)[:-2]+" minutes and "+str((df['Trip Duration'].mean()/60-df['Trip Duration'].mean()//60)*60)[:2]+" seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    print("The number of riders who were subscribers: "+str(df['User Type'].value_counts()["Subscriber"]))
    print("The number of riders who were customers: "+str(df['User Type'].value_counts()["Customer"]))

    # Display counts of gender
    if city != 'washington':
       print("\nThe number of riders who were male: "+str(df['Gender'].value_counts()["Male"]))
       print("The number of riders who were female: "+str(df['Gender'].value_counts()["Female"])) 
    # Display earliest, most recent, and most common year of birth
       print('\nThe oldest rider was born in '+str(df['Birth Year'].min())[:4])
       print('The youngest rider was born in '+str(df['Birth Year'].max())[:4])
       print('The most common year of birth for riders was '+str(df['Birth Year'].mode()[0])[:4])
    else:
        print('\nRider gender and birth year data is not available for Washington')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Displays five lines of raw data, allowing input to either go back or view more data'''
    bookmark = 0
    print(df.iloc[bookmark:bookmark+5])
    continue_prompt = input('Press enter to display more rows.\n Or go back (b).\n'+'-'*40).lower()
    while continue_prompt not in ['b','back'] and bookmark+5 <= len(df):
        continue_prompt = input('Press enter to display more rows.\n Or go back (b).\n'+'-'*40).lower()
        bookmark += 5
        print(df.iloc[bookmark:bookmark+5])

    

def data_prompt(df,city,confirmation):
    '''handles inputs in order to direct user to the various data functions or to restart or end the program'''
    print('To continue, press enter')
    input('-'*40)
    print('\n')
    print('The following data packages can be viewed:\nTime Stats (ts)\nStation Stats (ss)\nTrip Duration Stats (tds)\nUser Stats (us)\n')
    print('You can view the raw data (rd)\n')
    print('You may also restart with another city (rs)\nOr quit the program (q)\n')
    prompt_choice = input('What do you wish to do now?\n>').lower()
    
    while prompt_choice not in ['q','quit','rs','restart','ts','ss','tds','us','rd','time stats','station stats','trip duration stats','user stats','raw data']:
        prompt_choice = input('Invalid selection. Please try again.\n>')
    
    if prompt_choice in ['ts','time stats']:
        time_stats(df,confirmation)
    elif prompt_choice in ['ss','station stats']:
        station_stats(df)
    elif prompt_choice in ['tds','trip duration stats']:
        trip_duration_stats(df)
    elif prompt_choice in ['us','user stats']:
        user_stats(df,city)
    elif prompt_choice in ['q','quit']:
        quit()
    elif prompt_choice in ['rd','raw data']:
        raw_data(df)
    elif prompt_choice in ['rs','restart']:
        main()
    data_prompt(df,city,confirmation)

def main():
    while True:
        city, month, day, confirmation = get_filters()
        df = load_data(city, month, day)
        data_prompt(df,city,confirmation)

        #restart = input('\nWould you like to restart? y/n\n')
        #if restart.lower()[:1] != 'y':
        #    break


if __name__ == "__main__":
	main()
