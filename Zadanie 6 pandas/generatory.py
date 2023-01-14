import pandas as pd
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

dir = os.path.dirname(os.path.abspath(__file__))

df1 = pd.read_csv(dir + "\\Plant_1_Generation_Data.csv", parse_dates=['DATE_TIME'])
df2 = pd.read_csv(dir + "\\Plant_2_Generation_Data.csv", parse_dates=['DATE_TIME'])

df = pd.concat([df1, df2])

df = df.dropna()

df['YEAR'] = df['DATE_TIME'].dt.year
df['WEEK'] = df['DATE_TIME'].dt.isocalendar().week
df['YEAR_WEEK'] = df['YEAR'].astype(str)+df['WEEK'].astype(str)

generators = df['SOURCE_KEY'].unique()
year_week = df['YEAR_WEEK'].unique()

chosen_generator = generators[0]
chosen_year_week = year_week[1]


df_filtered = df[(df['YEAR_WEEK']==chosen_year_week) & (df['SOURCE_KEY']==chosen_generator)]
df_chosen_week = df[df['YEAR_WEEK']==chosen_year_week]

df_mean = df_chosen_week[['AC_POWER', 'DATE_TIME']].groupby(by='DATE_TIME', as_index=False).mean()

ax = df_filtered.plot(x ='DATE_TIME', y = 'AC_POWER', color='red', label=chosen_generator)

df_mean.plot(ax = ax, x = 'DATE_TIME', y = 'AC_POWER', color='green', label = "Mean")

plt.title("YearWeek: " + chosen_year_week + " Generator: " + chosen_generator)
plt.show()

df['mean'] = df[['DATE_TIME', 'AC_POWER']].groupby(by='DATE_TIME').transform('mean') # nie wygodniej by było od razu tego użyć?
df_underperforming = df[df['AC_POWER']<0.8*df['mean']]
df_u = df_underperforming.groupby(by='SOURCE_KEY').size()

print("Count of instances of generator underperforming: ")
print(df_u.sort_values(ascending=False))
