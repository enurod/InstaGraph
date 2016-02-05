__author__ = 'herzberge'
"""
This file accepts a command line Instagram user name input and returns a simple
network graph of the first 10 users the given user follows on Instagram
"""

#importing necessary libs
from instagram.client import InstagramAPI
import requests
import networkx as nx
import matplotlib.pyplot as plt
import sys

#Uses the Requests library to access the Instagram api for error handling purposes
def api_call_follows(id, access_token):
    url = 'https://api.instagram.com/v1/users/%s/follows?access_token=%s&count=10000' % (id, access_token)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return "Private account"

"""
 -The below function retrieves the first 100 followers for any given user_id
 -Pagination hasn't been built in for users with more than 100 followers
 -The response is an Instagram object that contains user-centric methods for data retrieval
"""
def get_follow_list(user_id):
    follow_list = []
    follow_list = [user for user in (api.user_follows(user_id=user_id, count=1000)[0])]
    return follow_list

#the below function retrieves the first 100 users a given user is followed by
#def get_followed_by_list(user_id):
# followed_by=[]
# followed_by = [ user for user in (api.user_followed_by(user_id=user_id, count=100000)[0]) ]
# return followed_by

"""
 -The below function takes a list of users and returns a dictionary where each key is
  a user and its value is a list of the first 100 people they follow
 -Using the api_call_follows function which does not use the python instagram library
  for error handling (private accounts) purposes
 -Pagination hasn't been built in for users with more than 100 followers
"""
def get_friends_follow(follow_list):
    friends_follow = {}
    friends_follow_test = {}
    for followed in follow_list:
        friends_follow_test[followed.username] = [api_call_follows(followed.id, access_token[1])]
        for k, v in friends_follow_test.iteritems():
            i = 0
            friends_follow_list = []
            if v[0] == "Private account":
                friends_follow_list.append("Private Account inserted at follower list")
                break
            else:
                while i < len(v[0]):
                    try:
                        friends_follow_list.append(v[0][i]['username'])
                        i += 1
                    except:
                        friends_follow_list.append("error on non-private account")
                        i += 1
            friends_follow[k] = [friends_follow_list]
    return friends_follow, friends_follow_test

# this function takes the usernames friends and his/her friends of friends and creates a networkx graph
def networkx_graph(follow_list, friends_follow, username):
    nxg = nx.Graph()
    [nxg.add_edge(username, follow.username) for follow in follow_list]
    \
    
    for name in friends_follows:
        [nxg.add_edge(name, follower) for follower in friends_follows[name][0]]
    return nxg

# main arguments
if __name__ == '__main__':
    access_token = ["XXXXX",
                    "XXXXX"]
    api = InstagramAPI(access_token=access_token[0])
    user_name = sys.argv[1]
    if user_name:
        user_id = api.user_search(user_name)[0].id
    else:
        user_id = "337135" # default to Itamar's account
    print user_id
    try: #error handling for private users
        friends = get_follow_list(user_id)
        friends_follows = get_friends_follow(friends[:10])[0] # to avoid rate limiting, taking the first 10 friends
        network_graph = networkx_graph(friends, friends_follows, user_name)
        nx.draw(network_graph)
        plt.show()
    except:
        print "Private User"
