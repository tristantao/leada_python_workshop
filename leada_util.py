# import pandas as pd

def update_message_to_friends(count_dict, friends_in_thread, MY_NAME):
        # I'm speaking to everyone in the thread, so update everyone.
    for friend in friends_in_thread:
        if friend == MY_NAME:
            continue
        count_dict[friend][0] += 1

def update_message_from_friend(count_dict, friend, MY_NAME):
    # I'm getting a message from a friend, so update it.
    # Don't include myself.
    if friend == MY_NAME:
        return
    try:
        count_dict[friend][1] += 1
    except KeyError as kE:
        count_dict[friend] = [0, 1]

def too_big_of_group(friends_in_thread, max_people_per_convo):
    return len(friends_in_thread) > max_people_per_convo

def append_to_df(df, entry, index=None):
    # Append data to our df via concat.
    # Direct assignment is too slow (by a large margin).
    # returns the newly appended df.
    if index == None:
        temp_df = pd.DataFrame([entry], columns=['date', 'name'])
        df = pd.concat([df,temp_df])
        last_index = len(df)
        return df
    else:
        if index % 1000 == 0:
            print index
        df.loc[index] = entry
        return index + 1

def in_top_friends(friends_message_count, name):
    return name in friends_message_count

