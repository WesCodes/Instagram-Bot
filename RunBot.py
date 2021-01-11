import IGBotToolkit
import IGCommentBot

"""below are the login credential"""
# the username
u = open(r"login info\username.txt", "r")
username = u.read()

# the password
p = open(r"login info\password.txt", "r")
password = p.read()

"""below are the parameters for the comment bot"""
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


"""belows are the extra parameters for the give away picker bot"""
'''
filter_by - what to filter comment by (2d list)
                       ex: filter_by = [['full_date', beginning_date(formatted: yyyy-mm-day(ex:2020-03-07), end_date(formatted: yyyy-mm-day(ex:2020-03-08)]]
                       ex: filter_by = [['month', beginning_month(ex:yyyy-mm), end_month(ex:yyyy-mm)]]
                       ex: filter_by = [['user', [usernames](ex:['nike', 'adidas'])]]
                       ex: filter_by = [['keyword', [keywords](ex: ['acquire', 'sire'])]] not case sensitive
                       ex: if you want multiple filter_by then just put all the filter_by in a list in the order you want to filter by
                           [['month', '2021-01', '2021-01'], ['keyword', '@']]
'''
filter_list = [[]] # example: [['full_date', '2020-12-26', '2021-01-04'], ['keyword', ['acquire', 'sire']]]
				   #          the above filter will filter by the date then filer by keyword

k_winner = 0 # the amount of winning comments to pick from post

filter_duplicate_entries = True # set to false if you don't want to filter out duplicate comment entries

# path to the browser driver. Use the geckodriver(firefox)
driver_path = r"put path in here" # ex: r"C:\geckodriver.exe"


"""below are the bots you can run"""
# start the bot. Run either the two below line depending on which version of comment bot you want to use.
ig_comment_bot = IGCommentBot.CommentBot(username, password, ig_link, driver_path)
# run this line to comment all your 'friends' on an ig post
ig_comment_bot.giveAwayCommentBot(following_list_path=following_path, followers_list_path=follower_path, friends_only=friends, seperate=seperate, users_to_comment_path=users_to_comment_path, amount=comment_amount)
# run this line to comment anything you want
ig_comment_bot.generalCommentBot(["LETS ACQUIRE THE SIRE"], seperate = False)


# run this line to use the give away picker bot
picker = IGCommentPicker.IGCommentPicker(username, password, ig_link, driver_path)
print(picker.chooseComment(2, filter_by=[['full_date', '2020-12-26', '2021-01-04']], comment_amount=k_winner, no_duplicate_comment=filter_duplicate_entries))






