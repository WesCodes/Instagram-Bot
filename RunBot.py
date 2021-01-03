import IGBotToolkit
import IGCommentBot


# the username
u = open(r"login info\username.txt", "r")
username = u.read()

# the password
p = open(r"login info\password.txt", "r")
password = p.read()

# link to ig post
ig_link = # link to ig post

# following_path
following_path = None
# follower_path
follower_path = None
# friends only?
friends = True
# one line comment or not
seperate = True
# amount to comment in one run, don't recommend going above 100 or you might get detected by instagram
comment_amount = 100

# users_to_comment_path
users_to_comment_path = None

# path to the browser driver. Recommend using the geckodriver(firefox)
driver_path = r"put path in here" # ex: r"C:\geckodriver.exe"


# start the bot
ig_comment_bot = IGCommentBot.CommentBot(username, password, ig_link, driver_path)

# run this line to comment all your 'friends' on an ig post
ig_comment_bot.giveAwayCommentBot(following_list_path=following_path, followers_list_path=follower_path, friends_only=friends, seperate=seperate, users_to_comment_path=users_to_comment_path, amount=comment_amount)

# run this line to comment anything you want
ig_comment_bot.generalCommentBot(["LETS ACQUIRE THE SIRE"], seperate = False)






