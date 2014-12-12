# Use this as your code-editing file

import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
#import dateutil
from leada_util import *

MY_NAME = "Tristan Tao"
max_people_per_convo = 4

with open('html/messages.htm', 'r') as message_file:
    messages_htm = message_file.read()

bs_struct = BeautifulSoup(messages_htm, "html.parser")

threads = bs_struct.find_all("div", {"class": "thread"})

friends_message_count = {} #basically {friend: [to, from]}

for thread in threads:
    friends_in_thread = [name.strip() for name in thread.contents[0].split(",")]
    for friend in friends_in_thread: # initialize
        friends_message_count[friend] = friends_message_count.get(friend, [0, 0])
    if too_big_of_group(friends_in_thread, max_people_per_convo):
        continue
    for m in thread.find_all("div", {"class": "message"}):
        user = m.find("span", {"class": "user"})
        friend_name = user.text
        if friend_name == MY_NAME:
            update_message_to_friends(friends_message_count, friends_in_thread, MY_NAME)
        else:
            if "facebook" not in friend_name:
                update_message_from_friend(friends_message_count, friend_name, MY_NAME)

sorted_top_friends_to = sorted(friends_message_count.items(), key= lambda x: x[1][0], reverse=True)[0:4]
sorted_top_friends_from = sorted(friends_message_count.items(), key=lambda x: x[1][1], reverse=True)[0:4]

print sorted_top_friends_to
print sorted_top_friends_from

