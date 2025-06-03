import numpy as np
np.float = float  # Patch for deprecated np.float used in seaborn
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date', parse_dates = ['date'])


# Clean data
low_percentile = df['value'].quantile(0.025)  # 2.5th percentile
high_percentile = df['value'].quantile(0.975) # 97.5th percentile
df = df[(df['value'] >= low_percentile) & (df['value'] <= high_percentile)]


def draw_line_plot():
    # Draw line plot

    fig,ax = plt.subplots(figsize=(12,6))
    ax.plot(df, color = '#A52A2A')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Define the correct month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Convert month column to ordered categorical type
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Group and pivot
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot

    fig,ax = plt.subplots(figsize=(12,6))
    df_bar.plot(kind='bar', ax=ax)

    #set the legend
    ax.legend(title = 'Months')

    #set the label
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Monthly Average Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date] # %b abbreviate the month 'January' - 'Jan'

    #month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    # Initialize the figure and axes
    fig, ax = plt.subplots(ncols=2, figsize=(15, 5))
    sns.boxplot(
        data = df_box, x="year", y="value", whis =[0, 99], palette="Set2", ax=ax[0],
        flierprops=dict(marker='D', markerfacecolor='black', markersize=2)
    )


    sns.boxplot(
        data = df_box, x="month", y="value", whis =[0, 99], palette="Set2", ax=ax[1],
        flierprops=dict(marker='D', markerfacecolor='black', markersize=2), order=month_order
    )


    ax[0].set(xlabel="Year")
    ax[0].set(ylabel="Page Views")
    ax[1].set(xlabel="Month")
    ax[1].set(ylabel="Page Views")
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')

    # Adjust spacing between the two axes
    plt.subplots_adjust(wspace=0.3)  # wspace = width space between columns




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
