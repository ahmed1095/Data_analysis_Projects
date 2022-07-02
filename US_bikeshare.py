import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("select the city (chicago, new york city, washington) :\n ").lower()
    while city not in CITY_DATA.keys():
        print ("your choice is an invalid city. You have to choose chicago, new york city or washington")

    # TO DO: get user input for month (all, january, february, ... , june)
    months= ['all','January','February','March','April','May','June']
    while True:
           month= input("select the month you want :[ January - Februaru - March - April - May - June ] to selsct all months Please write (all).\n")
           if month in months :
               break
           else: 
               print ("invalid Month - Please select the valid month from the above ones")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days= ['all','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday','Sunday']
    while True:
           day= input(" Select the day you want : [Saturday - Sunday - Monday - Tuesday - Wednesday - Thrusday - Friday] to selsct all days Please write (all).\n ")
           if day in days :
               break
           else:
               print("invalid Day - Please select the vaild day from the above ones")

    print('-'*40)
    return city, month, day


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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print( "the most Common month : {}" .format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print ( "the most common day of week : {}" .format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print ( "the most common Satrt hour : {}" .format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('most commonly used start station : {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('most commonly used end station : {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Total Trip'] = df['Start Station']+","+df['End Station']
    print('most frequent cobination : {}'.format(df['Total Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('total travel time : ',(df['Trip Duration'].sum()).round())

    # TO DO: display mean travel time
    print('mean travel time (AVG.travel time) : ',(df['Trip Duration'].mean()).round())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    # TO DO: Display counts of gender
    if city != 'washington':
        print(df['Gender'].value_counts().to_frame())

    # TO DO: Display earliest, most recent, and most common year of birth
        print('most common year of birth : ',int(df['Birth Year'].mode()[0]))
        print('most recent year of birth : ',int(df['Birth Year'].max()))
        print('earlisedt year of birth : ',int(df['Birth Year'].min()))
    else:
        print('no data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    print('\nRaw data is available to check.. \n')
    
    i=0
    user_input=input('would you like to show 5 rows for the row data? . Please type  yes or no.\n').lower()
    if user_input not in ['yes','no']:
        print('Invalid choice Please type yes or no')
        user_input=input('would you like to show 5 rows for the row data?. Please type  yes or no.\n').lower()
    elif user_input != 'yes':
        print('Thank You') 
    else:
        while i+5 < df.shape[0]:
            print(df.iloc[i:i+5])
            i += 5
            user_input = input ('would you like to show more than 5 rows of data ?. Please type yes or no.\n').lower()
            if user_input != 'yes':
                print ('Thank You')
                break
            
                
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if  restart.lower()!= 'yes':
            break
        else: 
               print ("your choice is invaild - Please select the valid choice yes or no")


if __name__ == "__main__":
	main()
