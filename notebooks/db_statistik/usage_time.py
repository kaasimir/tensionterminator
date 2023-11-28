from getpass import getpass
import matplotlib.pyplot as plt
import pandas as pd
import db_builder.db_handler as dbh
import seaborn as sns


class UsageTimePlotter:

    def __init__(self):
        self.second_column = None
        self.logging = None
        self.time_sum_per_data_df = None
        self.db_params = {
            'user': 'postgres',
            'password': getpass('Please enter DB pw'),  # enter your DB password
            'host': 'localhost',  # 'localhost' or IP address
            'port': '5432',  # '5432'
            'database': 'ttdatabase',  # tensionTerminator
        }
        self.toolcheck = dbh.DB_Conn(self.db_params)
        self.toolcheck.connect()
        self.engine = self.toolcheck.get_engine()

    def table_to_df(self, tabel_name: str):
        return pd.read_sql_table(tabel_name, con=self.engine)

    def datatransformer(self, table):
        data_df = self.table_to_df(table).dropna()
        self.second_column = data_df.columns[1]
        data_df['time_in_use'] = pd.to_datetime(data_df['time_in_use'], format='%H:%M:%S')
        data_df['time_in_use_seconds'] = data_df['time_in_use'].dt.hour * 3600 + data_df[
            'time_in_use'].dt.minute * 60 + data_df['time_in_use'].dt.second
        return data_df.groupby(self.second_column)['time_in_use_seconds'].sum().reset_index()

    def plot(self, table):
        self.time_sum_per_data_df = self.datatransformer(table)
        colors = sns.color_palette('husl', n_colors=len(self.time_sum_per_data_df))

        plt.figure(figsize=(12, 8))
        self.second_column = self.time_sum_per_data_df.columns[0]
        print(self.second_column)
        plt.bar(self.time_sum_per_data_df[self.second_column], self.time_sum_per_data_df['time_in_use_seconds'] / 60,
                color=colors)

        plt.xlabel(table)
        plt.ylabel('Minuten')
        plt.title(
            f"Count of each {table}, summarized time: {self.time_sum_per_data_df['time_in_use_seconds'].sum() / 60} min")

        plt.savefig(f"diagrams/{table}_usage_per_unlabeled_Data.png")



