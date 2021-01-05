import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
month_list = ['january', 'february', 'march', 'april', 'may', 'june']
day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


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
    while True:
        city = input("Would you like to see data for Chicago, New York city, or Washington\n").lower()
        if city not in CITY_DATA:
            print("Wrong option, please choose one of this cities: {}".format(tuple(CITY_DATA)))
        else:
            break

    # get user input for month (january, february, ... , june)
    while True:
        user_input = input(
            'Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter\n')
        if user_input.lower() == 'month':
            while True:
                month = input("Which month - January, February, March, April, May, or June?\n").lower()
                day = 'all'
                if month not in month_list:
                    print("Wrong option, please choose one of this options: {}".format(tuple(month_list)))
                else:
                    break
            break
        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif user_input.lower() == 'day':
            while True:
                month = 'all'
                day = input(
                    "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday,Sunday or all?\n").lower()
                if day not in day_list:
                    print("Wrong option, please choose one of this options: {}".format(tuple(day_list)))
                else:
                    break
            break

        elif user_input.lower() == 'both':
            print("both")
            while True:
                month = input("Which month - January, February, March, April, May, or June?\n").lower()
                if month not in month_list:
                    print("Wrong option, please choose one of this options: {}".format(tuple(month_list)))
                else:
                    break
            while True:
                day = input(
                    "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n").lower()
                if day not in day_list:
                    print("Wrong option, please choose one of this options: {}".format(tuple(day_list)))
                else:
                    break
            break

        elif user_input.lower() == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            print("Wrong answer")

    printline_terminal(40)
    print("User options: ", city, month, day)
    printline_terminal(40)
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
    start_time = time.time()
    print("Loading Data ...")

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    time_calculation(start_time)
    return df

def printline_terminal(ntimes):
    print('-' * ntimes)

def time_calculation(start_time):
    """Calculate the time a process took"""

    print("\nThis took {:.3f} seconds to calculate.".format(time.time() - start_time))
    printline_terminal(40)


def user_stats(df):
    """Calculate and displays user statistics."""

    start_time = time.time()

    print("Calculating user statistics...\n")
    print("What is the breakdown of users?")
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())
    try:
        # Display counts of gender, only available for NYC and Chicago !!!
        gender = df['Gender'].value_counts()
        print(gender.to_string())
        # Display earliest, most recent, and most common year of birth , only available for NYC and Chicago !!!
        print("The earliest year of birth is", int(np.min(df['Birth Year'])))
        print("The most recent year of birth is", int(np.max(df['Birth Year'])))
        print("The most common year of birth is", int(df['Birth Year'].mode()[0]))

    except:
        print("Data for Gender and Birth Year no available for this city")

    time_calculation(start_time)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()
    print("Calculating The Most Frequent Times of Travel...\n")
    # display the most common month
    print("The most common month is", month_list[df['month'].mode()[0] - 1].title())
    # display the most common day of week
    print("The most common day of week is", df['day_of_week'].mode()[0])
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is", df['hour'].mode()[0])

    time_calculation(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()
    print("Calculating The Most Popular Stations and Trip...\n")
    # display most commonly used start station
    print("The most commonly used start station is", df['Start Station'].mode()[0])
    # display most commonly used end station
    print("The most commonly used end station is", df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    df['Station Start to End'] = "from: " + df['Start Station'] + " to: " + df['End Station']
    print("The most frequent used route is", df['Station Start to End'].mode()[0])

    time_calculation(start_time)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()
    print("Calculating Trip Duration...\n")
    # display total travel time, seconds converted in format Years , Days
    trip_total_sec = int(df['Trip Duration'].sum())
    td = datetime.timedelta(seconds=trip_total_sec)
    print("The total travel time is {} Year(s) and {} Day(s)".format(td.days // 365, (td.days % 365)))
    # display mean travel time
    trip_mean_sec = int(df['Trip Duration'].mean())
    tm = datetime.timedelta(seconds=trip_mean_sec)
    print("The mean travel time is {} Hour(s) and {} Minute(s)".format(tm.seconds // 3600, (tm.seconds % 3600) // 60))

    time_calculation(start_time)


def chunker(iterable, size):
    """Yield successive chunks from iterable of length size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def raw_view(df):
    """Print to console 5 Rows at a time of data"""
    raw_view_input = input("Would you like to see the first 5 Rows of data? Yes or No\n").lower()

    if raw_view_input == "yes":
        for chunk in chunker(df, 5):
            print(chunk)
            raw_view_input = input("Would you like to see the next 5 Rows of data? Yes or No\n").lower()
            if raw_view_input != "yes":
                break
            else:
                continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
