import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_input(prompt, valid_options):
    """
    Validation of user-input.
    If no valid option is put in, asks again and lists all valid options.

    Return:
        (str) user-input, only if it is valid
    """
    response = input(prompt).strip().lower()
    while response not in valid_options:
        print(f"Invalid input. Please choose one of: {', '.join(valid_options)}")
        response = input(prompt).strip().lower()
    return response

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_valid_input(
        "Enter a city (Chicago, New York City, Washington): ",
        valid_cities
    )
    
    # get user input for month (all, january, february, ... , june)
    month = get_valid_input(
        "Enter a month (January to June) or 'all': ",
        valid_months
    )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input(
        "Enter a day of week or 'all': ",
        ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    )

    # TEST
    #month, day = 'may', 'friday'
    print('-'*40)
    return city, month, day


#DONE
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month_num]
    # filter by day of week if applicable
    if day != 'all':       
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]                                       #.dt.day_name() erstellt namen grossgeschrieben!
    
    # TEST
    #print(df.head())
    return df

# DONE
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()
    print("Most common month: {}".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].value_counts().idxmax()
    print("Most common day of the week: {}".format(popular_day))
    
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].value_counts().idxmax()
    print("Most common start hour: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#DONE
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print("Most commonly used Start Station: {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print("Most commonly used End Station: {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_stations = df.groupby(['Start Station', 'End Station'], as_index =False).size().idxmax()
    print("Most frequent combination of start and end station: {} and {}".format(popular_stations[0], popular_stations[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#DONE
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#DONE
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types:")
    print(user_types)
    print("\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Gender counts:")
        print(gender_count)
        print("\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("Earliest year of birth: {}".format(earliest_year))
        print("Most recent year of birth: {}".format(most_recent_year))
        print("Most common year of birth: {}".format(most_common_year))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    """Display raw data of filtered dataframe
    input: filtered dataframe
    output: raw data; 5 rows in one step, user will be asked if he wants 5 more rows
    """
    row_index = 0
    while True:
        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if raw_data.lower() not in ['yes', 'y']:
            break
        
        while row_index < len(df):          
            print(df[row_index:row_index+5])                                                    #print 5 rows in a table
            row_index += 5                                                                      #track current row_index
                       
            if row_index < len(df):                                                             #check if there are no more rows left
                more_data = input('\nWould you like to see 5 more rows? Enter yes or no.\n')
            if more_data.lower() not in ['yes', 'y'] :                                          #check if user says "no"
                break
        
        print('-'*40)
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data available for those filters. Please try another combination.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
