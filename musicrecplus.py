#!/usr/bin/python3

"""
Names: Annanya Jain
"""
filename = "musicrecplus.txt"

# i/o functions
def db_read():
    """ return db w/ user -> liked artists list
     """
    try:
        f_obj = open(filename,"r")
    except: #file open failure
        open(filename, 'x')
        return {}
    string = f_obj.read()
    f_obj.close()
    #print( string )
    lines = string.split("\n")
    db = {}
    for line in lines:
        #print( line )
        split_line = line.split(":")
        if len(  split_line ) < 2:
            continue
        user = split_line[0]
        artists = split_line[1].split(",")
        db[user] = artists
    return db


def db_write():
    """ writes db on memory to saved file """
    f_obj = open(filename, "w")
    write_str = ""
    for user in database:
        user_str = user + ':'
        for artist in database[user]:
            user_str = user_str + artist + ','
        if user_str[-1] == ',':
            user_str = user_str[:-1]
        write_str = write_str + user_str + '\n'
    f_obj.write(write_str)
    f_obj.close()

# helper functions
def grab_public_users():
    """ return list with public user
     """
    public_users = []
    for user in database:
        if len(user) == 0 or user[-1] != '$':
            public_users.append( user )
    return public_users

def artist_likes_count():
    """ return dict mapping artists -> likes count 
    """
    public_users = grab_public_users()
    likes_count = {}
    for user in public_users:
        for prefs in database[user]:
            if prefs not in likes_count:
                likes_count[prefs] = 1
            else:
                likes_count[prefs] += 1
    return likes_count


# sorting functions
def swap(aList, i, j):
    '''swaps the values of aList[i] and aList[j] '''
    aList[i], aList[j] = aList[j], aList[i]

def sort_standard(L):
    """ sorts in increasing order """ 
    for sorted_region in range(1, len(L)):
        for i in range(sorted_region, 0, -1):
            if L[i-1] > L[i]:
                swap(L, i-1, i)
            else:
                break 

def sort_dictReference(L, reference_dict):
    """ sorts in increasing order according to the dict """
    for sorted_region in range(1, len(L)): #index of the first unsorted element
        for i in range(sorted_region, 0, -1):
            if L[i-1] > L[i]:
                swap(L, i, i-1)
            else:
                break

            # user interface functions

def add_prefs(): #e
    new_pref = input("Enter an artist that you like (Enter to finish): \n")
    while new_pref != '':
        new_pref = new_pref[0].upper() + new_pref[1:].lower()
        if new_pref in database[username]:
            continue #no duplicate preferences
        database[username].append(new_pref)
        new_pref = input("Enter an artist that you like (Enter to finish): \n")


def grab_recommendations(): #r
    #match this user against all other users
    
    best_match = (0, [])
    this_prefs = set(database[username])
    for user in grab_public_users():
        if user == username:
            continue #no matching against yourself
        #calc matches
        user_prefs = set(database[user])
        match_count = 0
        possible_recs = []
        for pref in user_prefs:
            if pref in this_prefs:
                match_count += 1
            else:
                possible_recs.append(pref)
        #send in recommendations if we have a good match
        if match_count > best_match[0]:
            best_match = (match_count, possible_recs)
    if best_match[1] == []:
        print("No recommendations available at this time.")
        return
    for pref in best_match[1]:
        print(pref)

def grab_recommendations():
    best_match = (0, [])
    this_prefs = set(database[username])
    for user in grab_public_users():
        if user == username:
            continue  # no matching against yourself
        # calc matches
        user_prefs = set(database[user])
        match_count = 0
        possible_recs = []
        for pref in user_prefs:
            if pref in this_prefs:
                match_count += 1
            else:
                possible_recs.append(pref)
        # send in recommendations if we have a good match
        if match_count > best_match[0]:
            best_match = (match_count, possible_recs)

def howPopular(): #h
    """ prints out how many likes the most liked artist has
     """
    artist_likes = artist_likes_count()
    if len(artist_likes) == 0:
        print( "Sorry, no artists found" )
        return
    max_artist = 0
    for artist in artist_likes:
        if artist_likes[artist] > max_artist:
            max_artist = artist_likes[artist]
    print(max_artist)

def mostLiked_user(): #m
    """ for now just prints 1 cause i didnt finish it yet 
    """
    if len(database) == 0:
        print( "Sorry, no user found" )
        return
    public_users = grab_public_users();
    max_likes = 0;
    for user in public_users:
        if len(database[user]) > max_likes:
            max_likes = len(database[user])
    #max_likes contaisn the max likes for all user
    for user in public_users:
        if len(database[user]) == max_likes:
            print(user)

def show_prefs(): #s
    for artist in database[username]:
        print(artist)

def showmostpopular():
    
    likes = artist_likes_count()
    if not likes:
        print("Sorry, no artists found.")
    if len(likes) <= 3:
        for artist in likes:
            print(artist)
        return
    artists_list = list(likes.keys())
    sort_dictReference(artists_list, artist_likes_count)
    print(artists_list[-1])
    print(artists_list[-2])
    print(artists_list[-3])



database = db_read()
menu_interface = "\nEnter a letter to choose an option:\n e - Enter preferences\n r - Get recommendations\n p - Show most popular artists\n h - How popular is the most popular\n m - Which user has the most likes\n s - Show preferences\n q - Save and quit\n"
""" def handle_select(select):
    match select:
        case 'e':
            add_prefs()
        case 'r':
            grab_recommendations()
        case 'p':
            showmostpopular()
        case 'h':
            howPopular()
        case 'm':
            mostLiked_user()
        case 's':
            show_prefs()
        case 'q':
            print("cya later")
            db_write()
            exit()
        case _:
            return
 """

def handle_select(select):
    
    if select == 'e':
        add_prefs()
    elif select == 'r':
        grab_recommendations()
    elif select == 'h':
        howPopular()
    elif select == 'm':
        mostLiked_user()
    elif select == 's':
        show_prefs()
    elif select == 'p':
        showmostpopular()
    elif select == 'q':
        print("cya later")
        db_write()
        exit()
    else:
        return

#THE WAY USERNAME IS HANDLED ALLOWS A USERNAME WITH BOTH A PRIVATE AND PUBLIC ACCOUNT
#if a public account is created, and then a private account with the same username is made after
username = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private):")
if username + '$' in database and username not in database:
    username = username + '$'
if username in database and database[username] == []:
    add_prefs()
if username not in database and username + '$' not in database:
    database[username] = []
    add_prefs()

while True:
    print('\n', menu_interface)
    select = input()
    handle_select(select)

