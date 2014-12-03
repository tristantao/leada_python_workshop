import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
import dateutil
import pandas as pd
import datetime

from leada_util import *

class LeadaParser(object):

    max_people_per_convo = 4

    def __init__(self, threads, MY_NAME):
        self.threads = threads
        self.from_df = pd.DataFrame(columns=['date', 'name'])
        self.to_df = pd.DataFrame(columns=['date', 'name'])
        self.total_df = pd.DataFrame(columns=['date', 'name'])
        self.MY_NAME = MY_NAME

    def extract_top_friends_series(self, top_friends_from_key, top_friends_to_key):
        import time
        start_time = time.time()
        total_index = 0
        for thread in self.threads:
            friends_in_thread = [name.strip() for name in thread.contents[0].split(",")]
            if too_big_of_group(friends_in_thread, self.max_people_per_convo):
                # print "too big of a thread: %s" % len(friends_in_thread)
                continue
            for m in thread.find_all("div", {"class": "message"}):
                total_index += 1
                if total_index % 1000 == 0:
                    print "total_index: %s" % total_index
                user = m.find("span", {"class": "user"})
                meta = m.find("span", {"class": "meta"})
                friend_name = user.text
                date = dateutil.parser.parse(meta.text)
                if friend_name == self.MY_NAME:
                    for thread_friend in friends_in_thread:
                        if in_top_friends(top_friends_to_key, thread_friend):
                            self.to_df = append_to_df(self.to_df, [date, thread_friend])#, index=to_index)
                            #to_index = append_to_df(to_df, [date, thread_friend])#, index=to_index)
                            pass
                elif in_top_friends(top_friends_from_key, friend_name):
                    self.from_df = append_to_df(self.from_df, [date, friend_name])#, index=from_idex)
                    pass

        self.total_df = pd.concat([self.from_df, self.to_df])

        grouped_from_series = self.from_df.groupby([[ datetime.datetime(d.year, d.month, 1, 0, 0) for d in self.from_df.date], self.from_df.name]).size()
        grouped_to_series = self.to_df.groupby([[ datetime.datetime(d.year, d.month, 1, 0, 0) for d in self.to_df.date], self.to_df.name]).size()
        grouped_total_series = self.total_df.groupby([[ datetime.datetime(d.year, d.month, 1, 0, 0) for d in self.total_df.date], self.total_df.name]).size()

        unstacked_from = grouped_from_series.unstack().fillna(0)
        unstacked_to = grouped_to_series.unstack().fillna(0)
        unstacked_total = grouped_total_series.unstack().fillna(0)

        unstacked_from = unstacked_from.reset_index()
        unstacked_to = unstacked_to.reset_index()
        unstacked_total = unstacked_total.reset_index()

        unstacked_from.rename(columns={'index': 'date'}, inplace=True)
        unstacked_to.rename(columns={'index': 'date'}, inplace=True)
        unstacked_total.rename(columns={'index': 'date'}, inplace=True)
        print("--- %s seconds ---" % (time.time() - start_time))
        return unstacked_from, unstacked_to, unstacked_total


























