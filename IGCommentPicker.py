import IGBotToolkit
from random import choice
from time import sleep

class IGCommentPicker:
    def __init__(self, username, password, ig_post_link, driver_path):
        self.username = username
        self.password = password
        self.ig_post_link = ig_post_link
        self.driver_path = driver_path
        
        self.ig_bot_kit = IGBotToolkit.InstagramBotTools(username, password, driver_path)
        self.ig_bot_kit.login()

    def chooseComment(self, amount_to_choose, filter_by, comment_amount=None, no_duplicate_comment=True):
        """
        randomly pick specified amount of comments and return the (user, comment) tuple

        amount_to_choose - specified amount to pick
        filter_by - what to filter comment by (2d list)
                       ex: filter_by = [['full_date', beginning_date(formatted: yyyy-mm-day(ex:2020-03-07), end_date(formatted: yyyy-mm-day(ex:2020-03-08)]]
                       ex: filter_by = [['month', beginning_month(ex:yyyy-mm), end_month(ex:yyyy-mm)]]
                       ex: filter_by = [['user', [usernames](ex:['nike', 'adidas'])]]
                       ex: filter_by = [['keyword', [keywords](ex: ['acquire', 'sire'])]] not case sensitive
                       ex: if you want multiple filter_by then just put all the filter_by in a list in the order you want to filter by
                           [['month', '2021-01', '2021-01'], ['keyword', '@']]
        comment_amount - choose a speicific amount of comment to choose from. If none, then will choose all comment on post
        no_duplicate_comment - if true, don't count duplicate comments
                               else, count duplicate commments
        """

        # a dictionary with one key("comments") and value(a list) of tuple where the tuples are (username, comment))
        comments_list = self.ig_bot_kit.getComments(self.ig_post_link, amount=comment_amount, filter_by=filter_by, duplicate=no_duplicate_comment)["comments"]

        
        winner = []
        for i in range(amount_to_choose):
            # compile all comments

            if len(comments_list) != 0:
                rand_choice = choice(comments_list)
                print(rand_choice)

                winner.append(rand_choice)

                # remove the winning user
                comments_list[:] = [c for c in comments_list if c[0]!=rand_choice[0]]
                print(len(comments_list))
            else:
                return winner
        return winner

            



