import numpy as np
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    return x
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country
def data_over_time(df, col):
    value_counts_df = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    print("DataFrame after value_counts and reset_index:")
    print(value_counts_df)

    # Rename columns appropriately
    value_counts_df.columns = ['Edition', col]
    
    # Print the DataFrame after renaming columns
    print("DataFrame after renaming columns:")
    print(value_counts_df)

    # Sort values by 'Edition'
    nations_over_time = value_counts_df.sort_values('Edition')
    
    return nations_over_time




def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete and get the top 15
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge with the original DataFrame to get additional details
    x = top_athletes.merge(df, on='Name', how='left')

    # Select and rename relevant columns
    x = x[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')
    
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by country if specified
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    # Count occurrences of each athlete and reset index to create a DataFrame
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medals']  # Rename columns to 'Name' and 'Medals'

    # Merge with the original DataFrame to get additional details
    merged_df = top_athletes.merge(df, on='Name', how='left')

    # Select relevant columns and remove duplicates
    result_df = merged_df[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return result_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
