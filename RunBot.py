import IGBotToolkit
import IGCommentBot


# the username
u = open(r"C:\Users\acesw\Documents\Python Projects\Instagram Bot\personal test files\username.txt", "r")
username = u.read()

# the password
p = open(r"C:\Users\acesw\Documents\Python Projects\Instagram Bot\personal test files\password.txt", "r")
password = p.read()

# link to ig post
ig_link = "https://www.instagram.com/p/CJRWbOHL8Pz/"
# following_path
following_path = "following.txt"
# follower_path
follower_path = "followers.txt"
# friends only?
friends = True
# users_to_comment_path
users_to_comment_path = "users_to_comment.txt"


# start the bot
#ig_comment_bot = IGCommentBot.CommentBot(username, password, ig_link, r"C:\geckodriver.exe")

#ig_comment_bot.generalCommentBot(["LETS ACQUIRE THE SIRE"], seperate = False)
#ig_comment_bot.giveAwayCommentBot(following_list_path=following_path, followers_list_path=follower_path, friends_only = friends, seperate=True, users_to_comment_path = users_to_comment_path, amount=88)
# ig_comment_bot.generalCommentBot(["that shit is dank", "ytreeee asdas"])

tool = IGBotToolkit.InstagramBotTools(username, password, r"C:\geckodriver.exe")
tool.login()
print(len(tool.getFollowersLis()))





