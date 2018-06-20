#I used the gpodder/mygpoclient API functions within my functions.
#I used flask to carry out my functions.
import sys
sys.path.insert(0, "mygpoclient")

import mygpoclient
from mygpoclient import simple
from mygpoclient import api
from mygpoclient import public

from app import app
from flask import Flask, render_template, request, session

##-----------------------------LOGGING IN-----------------------------------##
#Main Login Page
@app.route('/')
def index():
    return render_template('login.html')

#After logging in, I pull User/Pass and send devices to next page
@app.route('/loginresult', methods=['GET', 'POST'])
def loginresult():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        session['password'] = password
        client = api.MygPodderClient(username, password)
        devices = client.get_devices()
        #if user doesn't have a device yet, I make one called 'legacy'
        if not devices:
            devices = 'legacy'

        return render_template('getdevices.html', devices=devices)

#user chooses their device they want to use
@app.route('/deviceresult', methods=['GET', 'POST'])
def deviceresult():
    if request.method == 'POST':
        device = request.form['dev_id']
        session['device'] = device

        return render_template('home.html')

##--------------------------BEGIN NAV BAR--------------------------------##

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


##-----------------------------SEARCH-----------------------------------##
#User can search from home or the nav-bar
@app.route('/searchresult', methods=['GET', 'POST'])
def searchresult():
    if request.method == 'POST':
        client = public.PublicClient()
        Search = request.form['Search']
        session['Search'] = Search
        search_results = client.search_podcasts(Search)

        return render_template('searchresults.html', search_results=search_results, Search=Search)

#Sorts search results by dropdown menu
@app.route('/searchddform', methods=['GET', 'POST'])
def searchddform():
    if request.method == 'POST':
        client = public.PublicClient()
        Search = session.get('Search')
        search_results = client.search_podcasts(Search)
        option = request.form['Sort'] #finds the user's sorting preference
        podcast_list = []
        for podcast in search_results:
            podcast_list.append(podcast)

        #can sort by number of subscribers or alphabetically
        if option == 'Subscribers':
            podcast_list.sort(key=lambda x: x.subscribers, reverse=True)
        elif option == 'A->Z':
            podcast_list.sort(key=lambda x: x.title)

    return render_template('searchresults.html', search_results=search_results, podcast_list=podcast_list, Search=Search)


##-----------------------------CATEGORIES-----------------------------------##
#Main categories page, user can choose from list of categories
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    client = public.PublicClient()
    category_names = client.get_toptags()
    category_names.sort(key=lambda x: x.usage, reverse=True) #sorting by most used tags

    return render_template('categories.html', category_names=category_names)

#Sorting main categories page
@app.route('/categoryddform', methods=['GET', 'POST'])
def categoryddform():
    if request.method == 'POST':
        client = public.PublicClient()
        category_names = client.get_toptags()
        option = request.form['Sort'] #finds the user's sorting preference
        #user can sort by most popular or alphabetically
        if option == 'Most Popular':
            category_names.sort(key=lambda x: x.usage, reverse=True)
        elif option == 'A->Z':
            category_names.sort(key=lambda x: x.tag)

    return render_template('categories.html', category_names=category_names)

#After choosing a category, this page displays the podcasts in that category
@app.route('/tag', methods=['GET', 'POST'])
def tag():
    if request.method == 'POST':
        tag = request.form['category_tag'] #the category chosen
        session['tag'] = tag
        client = public.PublicClient()
        category_podcasts = client.get_podcasts_of_a_tag(tag)

        return render_template('category.html', tag=tag,  category_podcasts=category_podcasts)

#Sorts the podcasts in the chosen category
@app.route('/tagddform', methods=['GET', 'POST'])
def tagddform():
    if request.method == 'POST':
        tag = session.get('tag')
        client = public.PublicClient()
        category_podcasts = client.get_podcasts_of_a_tag(tag)
        option = request.form['Sort'] #finds the user's sorting preference
        podcast_list = []
        for podcast in category_podcasts:
            podcast_list.append(podcast)

        #can sort by most subscribers or alphabetically
        if option == 'Most Subscribers':
            podcast_list.sort(key=lambda x: x.subscribers, reverse=True)
        elif option == 'A->Z':
            podcast_list.sort(key=lambda x: x.title)

    return render_template('category.html', podcast_list=podcast_list)


##-----------------------------TOP PODCASTS-----------------------------------##
#lists the top-50 podcasts list by number of subscribers
@app.route('/toppodcasts', methods=['GET', 'POST'])
def toppodcasts():
    client = public.PublicClient()
    top_podcasts = client.get_toplist()

    return render_template('toppodcasts.html', top_podcasts=top_podcasts)


##-----------------------------SUGGESTIONS-----------------------------------##
#IF A USER HAS SUGGESTIONS it lists the suggestions for that user
#IF A USER DOES NOT HAVE SUGGESTIONS it takes the first word of the first 2
#of their subscriptions (for loading sake), searches that word, and returns
#the top 5 search results.
@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    username = session.get('username')
    password = session.get('password')
    device = session.get('device')
    client = simple.SimpleClient(username, password)
    suggestions_list = client.get_suggestions()
    suggestions = []
    if not suggestions_list:
        subscriptions_list = client.get_subscriptions(device)
        client = public.PublicClient()
        i = 0
        while i < 2:
            subscription = client.get_podcast_data(subscriptions_list[i])
            search = client.search_podcasts((subscription.title).split(' ', 1)[0])
            i = i + 1
            j = 0
            while j < 5:
                suggestions.append(search[j])
                j = j + 1
    else:
        for url in suggestions_list:
            suggestions.append(client.get_podcast_data(url))

    return render_template('suggestions.html', suggestions=suggestions)


##-----------------------------SUBSCRIPTIONS-----------------------------------##
#IF A USER HAS SUBSCRIPTIONS it lists them
#can not be done if a user doesn't have any subscriptions
@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    username = session.get('username')
    password = session.get('password')
    device = session.get('device')
    client = simple.SimpleClient(username, password)
    subscriptions_list = client.get_subscriptions(device)
    subscriptions = []
    for url in subscriptions_list:
        client = public.PublicClient()
        subscriptions.append(client.get_podcast_data(url))

    return render_template('subscriptions.html', subscriptions=subscriptions)

#Sorts the user's subscriptions
@app.route('/subscriptionddform', methods=['GET', 'POST'])
def subscriptionddform():
    if request.method == 'POST':
        username = session.get('username')
        password = session.get('password')
        device = session.get('device')
        client = simple.SimpleClient(username, password)
        subscriptions_list = client.get_subscriptions(device)
        subscriptions = []
        for url in subscriptions_list:
            client = public.PublicClient()
            subscriptions.append(client.get_podcast_data(url))
        option = request.form['Sort'] #finds the user's sorting preference
        podcast_list = []
        for podcast in subscriptions:
            podcast_list.append(podcast)

        #can sort alphabetically or by most subscribers
        if option == 'A->Z':
            podcast_list.sort(key=lambda x: x.title)
        elif option == 'Most Subscribers':
            podcast_list.sort(key=lambda x: x.subscribers, reverse=True)

        return render_template('subscriptions.html', subscriptions=subscriptions, podcast_list=podcast_list)


##-----------------------------LISTEN TO NEXT-----------------------------------##
#I wanted to get the number of episodes per week for the user's subscribed podcasts,
#but I couldn't find an api function for that; So, I assumed the user was subscribed
#to the top-25 podcasts, self-searched the number of episodes (either by finding
#the number listed on the website, or doing [20*number_of_pages_on_gpodder + amount_on_last_page]
#posted for those podcats,then sorted the top-25 podcasts by the most content/number of episodes.
@app.route('/listennext', methods=['GET', 'POST'])
def listennext():
    num_episodes = []
    client = public.PublicClient()
    top_podcasts = client.get_toplist()

    #found number of episodes for each podcast in my top-25 list
    num_episodes = [370, 646, 487, 528, 4931, 670, 622, 1864, 667, 675, 2086, 5271, 770, \
                    2481, 848, 1086, 461, 2495, 399, 61, 807, 1807, 1511, 346, 970]
    podcast_list = []

    #for the first 25 podcasts on my top-list, add a num_episodes variable to the podcast object
    #then set that equal to the index in the num_episodes array
    i = 0
    for podcast in top_podcasts:
        if i<25:
            podcast.num_episodes = num_episodes[i]
            i = i + 1
            podcast_list.append(podcast)

    #sort the podcast objects be the new num_episodes variable
    podcast_list.sort(key=lambda x: x.num_episodes, reverse=True)

    return render_template('listennext.html', podcast_list=podcast_list)
