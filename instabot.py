import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


#LATITUDE=28.6129
#LONGITUDE=77.2295
#SENDBOX USER = inta1996,

APP_ACCESS_TOKEN = '3227036965.6587353.0e99318ec6374c25aaca90275c07bf40'
BASE_URL = 'https://api.instagram.com/v1/'

calamities = ['flood', 'earthquake', 'tsunami', 'landslide', 'soil erosion', 'avalanche', 'cyclones', 'hurricane',
              'thunderstorm', 'drought']
locationid=[]

#Function to get self info
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
#For print self info
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#Function to get id of user by username
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()   #Information of user in json form

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


#Function to get user by username
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


#Function to get own information
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



#Function to get info of user by username
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#Function to get ID of post upload by user using username

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


#Function to like user post by username
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#Function to comment user post using username
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#Function to delete negative comment of user by username
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


#Function to get list of comments of post using username
def get_comments(insta_username):
    media_id = get_post_id(insta_username)
    if media_id == None:
        print "User doesn\'t exist"
        exit()
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    print user_media
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            print 'Comments Are:'
            position = 1
            for text in user_media['data']:
                print'\t%s. from %s: %s' % (
                position, text['from']['username'], text['text'])  # Printing list of comments of a post
                position = position + 1
        else:
                print'No comments found'
                return None

    else:
        print 'Status code other than 200 is received'
        exit()




# Function declaration to get the location where natural calamities has occured

def get_natural_calamities(lat,lng):
    request_url = (BASE_URL + 'media/search?lat=%s&lng=%s&distance=500&access_token=%s') % (lat, lng, APP_ACCESS_TOKEN)
    print 'GET reques url: %s' % (request_url)
    user_location = requests.get(request_url).json()
    print user_location
    if user_location['meta']['code'] == 200:
        if len(user_location['data']):
            image=user_location['data'][0]['images']['standard_resolution']['url']
            print image
            for temp in calamities:
                if user_location['data'][0]['tags']==temp:
                 print user_location['data'][0]['tags']
                 print user_location['data'][0]['location']
            print 'Tags are:%s' % (user_location['data'][0]['tags'])
            print 'Location is:%s' % (user_location['data'][0]['location'])
            print '%s is going on at %s' %(user_location['data'][0]['tags'],user_location['data'][0]['location'])
        else:
            print'media not found'
    else:
        print 'Status code other than 200 received'

def start_bot():
    while True:
        print '\n'
        print 'Hello! Welcome to instaBot!'
        print 'Select your menu options:'
        print "1.Get your own details"
        print "2.Get details of a user by insta_username"
        print "3.Get your own recent post"
        print "4.Get the recent post of a user by insta_username"
        print "5.Like the recent post of a user"
        print "6.Make a comment on the recent post of a user"
        print "7.Delete negative comments from the recent post of a user"
        print "8.Get list of comments of user"
        print "9.Get location of calamities"
        print "10.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            insta_username = raw_input("Enter the username of the insta_user: ")
            get_user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input("Enter the username of the insta_user: ")
            get_user_post(insta_username)
        elif choice == "5":
            insta_username = raw_input("Enter the username of the insta_user: ")
            like_a_post(insta_username)
        elif choice == "6":
            insta_username = raw_input("Enter the username of the insta_user: ")
            post_a_comment(insta_username)
        elif choice == "7":
            insta_username = raw_input("Enter the username of the insta_user: ")
            delete_negative_comment(insta_username)
        elif choice == "8":
            insta_username = raw_input("Enter the username of insta_user")
            get_comments(insta_username)
        elif choice == "9":
            lat = float(raw_input("Enter the latitude:"))
            lng = float(raw_input("Enter the longitude"))
            get_natural_calamities(lat, lng)
        elif choice == "10":
            exit()
        else:
            print "wrong choice"


start_bot()
