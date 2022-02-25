from calendar import month
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["chicago" , "new york" , "washington"]
    city = input("Would you like to see data for (chicago, new york, or washington) :\n").lower()
    while city not in city_list :
        print("invalid input")
        city = input("Please specify a city from (chicago, new york, or washington) :\n")


    # get user input for month (all, january, february, ... , june)
    month_list = ["all" , "january" , "february" , "march" , "april" , "may" , "june"]
    month = input("Would you like to filter the data by month (all, january, february, ... , june) :\n").lower()
    while month not in month_list:
        print("invalid input")
        month = input("Please specify a month from (all, january, february, ... , june) :\n")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ["all" , "monday" , "tuesday" , "wednesday" , "thursday" , "friday" , "saturday" , "sunday"]
    day = input("Would you like to filter the data by day (all, monday, tuesday, ... sunday) :\n").lower()
    while day not in day_list :
        print("invalid input")
        day = input("Please specify a day from (all, monday, tuesday, ... sunday) :\n")


    print('-'*40)
    return(city, month, day)
    


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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('the most common month:',most_common_month)


    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('the most common day:',most_common_day)


    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('the most common start hour:',most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_used_start_station = df['Start Station'].mode()[0]
    print('the most common used start station:',most_common_used_start_station)


    # display most commonly used end station
    most_common_used_end_station = df['End Station'].mode()[0]
    print('the most common used end station:',most_common_used_end_station)


    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] +"  >>>  "+ df['End Station']
    most_freq_trip = df['trip'].mode()[0]
    print('the most frequent combination of start station and end station trip:',most_freq_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time:',total_travel_time)



    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the mean travel time:',mean_travel_time)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].count()
    print('the counts of user types:',user_type_count)


    # Display counts of gender
    if 'Gender' in df:

        gender_count = df['Gender'].count()
        print('the counts of gender:',gender_count)
    else:
        print("There is No Gender")



    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('the earliest year of birth:',earliest_birth_year)
        print('the recent year of birth:',recent_birth_year)
        print('the common year of birth:',common_birth_year)
    else:
        print('There is no Birth Year')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        start_loc = 0
        while view_data != "no":
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
