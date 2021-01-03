import IGBotToolkit
import IGCommentBot


# the username
u = open(r"C:\Users\acesw\Documents\Python Projects\Instagram Bot\personal test files\username_test.txt", "r")
username = u.read()

# the password
p = open(r"C:\Users\acesw\Documents\Python Projects\Instagram Bot\personal test files\password_test.txt", "r")
password = p.read()

# link to ig post
ig_link = "https://www.instagram.com/p/CJUkCtVsVne/"
# following_path
following_path = "following.txt"
# follower_path
follower_path = "followers.txt"
# friends only?
friends = True
# users_to_comment_path
users_to_comment_path = "users_to_comment.txt"


# start the bot
ig_comment_bot = IGCommentBot.CommentBot(username, password, ig_link, r"C:\geckodriver.exe")

#ig_comment_bot.generalCommentBot(["LETS ACQUIRE THE SIRE"], seperate = False)
ig_comment_bot.giveAwayCommentBot(following_list_path=None, followers_list_path=None, friends_only = False, seperate=True, users_to_comment_path = None, amount=88)
# ig_comment_bot.generalCommentBot(["that shit is dank", "ytreeee asdas"])

# tool = IGBotToolkit.InstagramBotTools(username, password, r"C:\geckodriver.exe")
# tool.login()
# f = tool.getFollowingLis()
# print("following")
# print(f)
# print(len(f))
# print('\n')
# print('\n')
# print('\n')
# tool.reloadProfile()
# f = tool.getFollowersLis()
# print("follower")
# print(f)
# print(len(f))






