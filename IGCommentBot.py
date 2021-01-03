import IGBotToolkit
import random
import time
class CommentBot:
    def __init__(self, username, password, ig_post_link, driver_path):
        self.username = username
        self.password = password
        self.ig_post_link = ig_post_link
        self.driver_path = driver_path
        
        self.ig_bot_kit = IGBotToolkit.InstagramBotTools(username, password, driver_path)


    def generalCommentBot(self, comment_lis, seperate = True):
        """
        unlike the giveAwayCommentBot, this will allow you to comment whatever you want on a post

        ig_post_link - the ig post to comment on
        comment_lis - a lis of strings with comments you want to make
        seperate - if you want all the comments on the same line
        """

        

        # login instagram account
        self.ig_bot_kit.login()


        wait_time = random.randint(3, 6)
        time.sleep(wait_time)

        # runs the bot
        self.ig_bot_kit.commentBot(self.ig_post_link, comment_lis, seperate)


        wait_time = random.randint(3, 6)
        time.sleep(wait_time)

        # shut down the driver
        self.ig_bot_kit.driver.quit()


    def giveAwayCommentBot(self, following_list_path=None, followers_list_path=None, amount = 75, friends_only = True, seperate = True, users_to_comment_path = None):
        """
        comment friends on chosen ig giveaway post

        following_list_path - the path to the text file 
        followers_list_path- the path to the text file
        ig_post_link - the link to the ig post
        friends_only - if True will only comment the ig friends who you follow and who follows you back
        seperate - if False then comment all name in one comment
        """


        # login instagram account
        self.ig_bot_kit.login()

        if followers_list_path is None:
            # write the follower text to the directory this py file is in
            self.ig_bot_kit.writeFollowers()
            followers_list_path = r"output files\followers.txt"

            # reload profile
            self.ig_bot_kit.reloadProfile()

        # if either path doesn't exist
        if following_list_path is None:
            # write the following text to the directory this py file is in
            self.ig_bot_kit.writeFollowing()
            following_list_path = r"output files\following.txt"

            # reload profile
            self.ig_bot_kit.reloadProfile()

        
        wait_time = random.randint(3, 6)
        time.sleep(wait_time)

        # start the comment
        self.ig_bot_kit.commentFFBot(following_list_path, followers_list_path, self.ig_post_link, amount, friends_only, seperate, users_to_comment_path = users_to_comment_path)

        print("done")
        wait_time = random.randint(3, 6)
        time.sleep(wait_time)

        # shut down the driver
        self.ig_bot_kit.driver.quit()