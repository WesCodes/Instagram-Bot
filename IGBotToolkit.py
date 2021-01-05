import io

from CountDownConsole import countdown

from random import randint
from time import sleep
from collections import defaultdict
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class InstagramBotTools:
    def __init__(self, username, password, fire_fox_driver_path):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox(executable_path = fire_fox_driver_path)


    def login(self):
        """
        login into Instagram and direct to profile page
        """

        # go to login page
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        # enter username
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(self.username)

        # enter password
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(self.password)

        # click login button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/div[text()='Log In']"))).click()

        # clicking the not now button for saving login
        WebDriverWait(self.driver, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Not Now"]')).click() 

        # clicking the not now button for turn on notification
        WebDriverWait(self.driver, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Not Now"]')).click() 

        # wait
        sleep(randint(3, 6))
        
        # go to profile page
        self.goToProfile()
        



    def getFollowersLis(self):
        """
        returns a list of followers username with the @ tag infront
        """

        # check follower count
        follower_count = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[2]/a/span"))).text
        print(follower_count)
        if int(follower_count) == 0:
            return []


        # the link to the followers from profile page
        follower_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "followers")))
        follower_link.click()

        # wait
        sleep(randint(3, 6))

        # the screen that pops up when followers are clicked
        follower_modal = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))
    
        # to scroll the follower modal and load all the following
        prev_scroll_height = 0
        curr_scroll_height = 1
        while prev_scroll_height != curr_scroll_height:
            sleep(1)
            prev_scroll_height = curr_scroll_height
            js_scroll_script = "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight"
            curr_scroll_height = self.driver.execute_script(js_scroll_script, follower_modal)

        
        # find all the users
        follower_list = follower_modal.find_elements_by_css_selector('li')
        return ["@" + name.find_element_by_css_selector('a').get_attribute('href').split('/')[3].strip() for name in follower_list]


    def getFollowingLis(self):
        """
        returns a list of following username with the @ tag infront
        """
        
        # check follower count
        following_count = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//li[3]/a/span"))).text
        print(following_count)
        if int(following_count) == 0:
            return []

        # the link to the followers from profile page
        following_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "following")))
        following_link.click()
        
        sleep(randint(3, 6))

        # the screen that pops up when following are clicked
        following_modal = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))
    
        # to scroll the following modal and load all the following
        prev_scroll_height = 0
        curr_scroll_height = 1
        while prev_scroll_height != curr_scroll_height:
            sleep(1)
            prev_scroll_height = curr_scroll_height
            js_scroll_script = "arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight"
            curr_scroll_height = self.driver.execute_script(js_scroll_script, following_modal)


        # find all the users
        following_list = following_modal.find_elements_by_css_selector('li')
        return ["@" + name.find_element_by_css_selector('a').get_attribute('href').split('/')[3].strip() for name in following_list]


    def writeFollowers(self, path="output files"):
        """
        write text file of followers to destinated path
        Return False if there are no followers

        path - the path to write to
        """

        print("inside write follower")
        # save the follower into txt file
        file1 = open(path + r"\followers.txt","w+")

        follower_string = '\n'.join(self.getFollowersLis())
        file1.write(follower_string)
        file1.close()
        print("write Follower done")
        
        if len(follower_string.strip()) == 0:
            return False
        return True


    def writeFollowing(self, path="output files"):
        """
        write text file of following to destinated path
        Returns False if there are no followings

        path - the path to write to
        """

        # save the following into txt file
        file1 = open(path + r"\following.txt","w+") 

        follower_string = '\n'.join(self.getFollowingLis())
        file1.write(follower_string)
        file1.close()

        if len(follower_string.strip()) == 0:
            return False
        return True


    def writeFriends(self, following_list_path, followers_list_path, output_file_path, friends_only = True):
        """
        This writes a new text file with the following and followers.
        If friends_only is set to True, then the text files will contain users who you follow and who follows you back
        Else, text file will have the combination of followers and following with duplicates removed

        following_list_path - the path to the text file printed by getFollowersLis
        followers_list_path- the path to the text file printed by getFollowingLis
        output_file_path - the path to the output file
        friends_only - if True will only comment the ig friends who you follow and who follows you back
        """

        # opening text files and converting to list
        followers_file = open(followers_list_path,"r") 
        following_file = open(following_list_path, "r")
        followers = followers_file.read().split('\n')
        following = following_file.read().split('\n')


        # getting rid of empty string in case followers or following are 0
        following_s = set(following)
        followers_s = set(followers)
        if '' in following_s:
            following_s.remove('')
        if '' in followers_s:
            followers_s.remove('')

        # get the friends only
        if friends_only:
            users = list(following_s & followers_s)
        else:
            # get both followers and following without duplicates
            users = list(following_s | followers_s)
            print(users)

        print("creating user file")
        # write the result to text file
        
        output_file = open(output_file_path, "w")
        output_file.write('\n'.join(users))
        output_file.close()



    def goToProfile(self):
        """
        reload profile page
        """

        self.driver.get("https://www.instagram.com/" + self.username)
        

    def commentBot(self, ig_post_link, users, seperate = True):
        """
        This will allow you to post comments(including tagging users) on an ig post

        users - a lis of strings with ig username, each username should be formatted as '@[user_name]'
                     example input: ['@generic_kevin', '@generic_tiffany']. 
                Can also be a list of regular comments
        ig_post_link - the link to the ig post
        seperate - if False then comment all name in one comment
        """

        # goes to link
        self.driver.get(ig_post_link)

        # wait three second
        wait_interaction = randint(3, 6)
        sleep(wait_interaction)

        if seperate is False:
            # to comment on same line
            account_str = ""
            for i, account in enumerate(users):
                account_str += account

                if i != len(users) - 1:
                    account_str += " "

            comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
            comment_area.clear()
            comment_area.click()
            
            # Locating comment box due to the html element changing after clicking. From Ypffh to Ypffh focus-visible
            comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
            comment_area.send_keys(account_str)

            wait_submit = randint(3, 5)
            wait_submit_header = f"Waiting {wait_submit} seconds to submit comment, '{account_str}'"
            countdown(wait_submit, wait_submit_header)

            comment_area.submit()
            print("Submitted")
            
        else:
            # loop to comment each friend as seperate comment
            for i, account in enumerate(users):
                try:
                    wait_before_comment = randint(40, 65)
                    wait_before_comment_header = f"Waiting {wait_before_comment} seconds before commenting"
                    countdown(wait_before_comment, wait_before_comment_header)

                    comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
                    comment_area.clear()
                    comment_area.click()
                    
                    # Locating comment box due to the html element changing after clicking. From Ypffh to Ypffh focus-visible
                    comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
                    comment_area.send_keys(account)

                    wait_submit = randint(3, 5)
                    wait_submit_header = f"Waiting {wait_submit} seconds to submit comment, '{account}'"
                    countdown(wait_submit, wait_submit_header)

                    comment_area.submit()
                    print("Submitted")
                except Exception as E:
                    print("err")
                    print(str(E))


    def commentFFBot(self, following_list_path, followers_list_path, ig_post_link, amount, friends_only = True, seperate = True, users_to_comment_path = None):
        """
        This allows you tag your followers/following on an ig post. Comment at a rate of around 60 comments an hour

        following_list_path - the path to the text file printed by getFollowersLis
        followers_list_path- the path to the text file printed by getFollowingLis
        ig_post_link - the link to the ig post
        amount - the default amount to comment is 60. Not recommending increasing as this can result in a ban by IG
        friends_only - if True will only comment the ig friends who you follow and who follows you back
        seperate - if False then comment all name in one comment
        users_to_comment_path - if none, then a new text file will be created from the following_list and followers_list text files 
                                else, the users_to_comment text file will be used instead
        """

        print(amount)
        if users_to_comment_path is None:
            users_to_comment_path = r"output files\users_to_comment.txt"
            self.writeFriends(following_list_path, followers_list_path, users_to_comment_path, friends_only)

        # goes to link
        self.driver.get(ig_post_link)

        # wait three second
        wait_interaction = randint(3, 6)
        sleep(wait_interaction)

        print("wow")
        # opening the text file to comment from
        user_comment_file = open(users_to_comment_path, "r")

        if seperate is False:
            # to comment on same line
            print("not seperate")
            account_str = ""
            for i in range(amount):
                # reading the text file line by line
                account_str += user_comment_file.readline().strip('\n')
                if account_str.strip() == "":
                    break
                if i != len(users) - 1:
                    account_str += " "

            # read the remaining users
            remaining_users = user_comment_file.readlines()
            user_comment_file.close()

            print("updating user file")
            # updating the text file by getting rid of users who's been commmented
            with open(users_to_comment_path, "w") as file:
                for u in remaining_users:
                    file.write(u)
                file.close()

            comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
            comment_area.clear()
            comment_area.click()
            
            # Locating comment box due to the html element changing after clicking. From Ypffh to Ypffh focus-visible
            comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
            comment_area.send_keys(account_str)

            wait_submit = randint(3, 6)
            wait_submit_header = f"Waiting {wait_submit} seconds to submit comment, '{account_str}'"
            countdown(wait_submit, wait_submit_header)

            comment_area.submit()
            print("Submitted")
        else:
            for i in range(amount):
                try:
                    # reading the text file line by line
                    account = user_comment_file.readline().strip('\n')

                    # if text is empty
                    if account.strip() == "":
                        print("empty")
                        break

                    wait_before_comment = randint(40, 65)
                    wait_before_comment_header = f"Waiting {wait_before_comment} seconds before commenting"
                    countdown(wait_before_comment, wait_before_comment_header)
                    
                    comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
                    comment_area.clear()
                    comment_area.click()
                    
                    # Locating comment box due to the html element changing after clicking. From Ypffh to Ypffh focus-visible
                    comment_area = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[class^= 'Ypffh']")))
                    comment_area.send_keys(account)

                    wait_submit = randint(3, 5)
                    wait_submit_header = f"Waiting {wait_submit} seconds to submit comment, '{account}'"
                    countdown(wait_submit, wait_submit_header)

                    comment_area.submit()
                    print("sent, amount remaining: " + str(int(amount - i - 1)))

                except Exception as e:
                    print(str(e))
            
            # read the remaining users
            remaining_users = user_comment_file.readlines()
            user_comment_file.close()

            # updating the text file by getting rid of users who's been commmented
            with open(users_to_comment_path, "w") as file:
                for u in remaining_users:
                    file.write(u)
                file.close()


    def getComments(self, ig_post_link, amount = None, group_by = None, filter_by = None):
        """
        returns a dictionary of comments.
        if there is no filter specified, then the key-val pair will be ("comment", comments) with 
        comments being all the current comments(doesn't include replies) on the post

        ig_post_link - the link to the ig post
        amount - amount of comments to get
        group_by - the group by filters are ['full_date', 'user']
                   ex: full_date: Dec 26, 2020
                   ex: user: nike
        filter_by - what to filter comment by
                   ex: filter_by = ['full_date', beginning_date(formatted: yyyy-mm-day(ex:2020-03-07), end_date(formatted: yyyy-mm-day(ex:2020-03-08)]
                   ex: filter_by = ['month', beginning_month(ex:yyyy-mm), end_month(ex:yyyy-mm)]
                   ex: filter_by = ['user', [usernames](ex:['nike', 'adidas'])]
                   ex: filter_by = ['keyword', [keywords](ex: ['acquire', 'sire'])] not case sensitive
        """


        def filter_comments(comment_list, filter_by=None):
            """
            filter a selenium comment element by the filtered. returns the comment_list element that is filtered

            comment_list - the ul element that holds all the comment
            filter_by - what to filter comment by
                       ex: filter_by = ['full_date', beginning_date(formatted: yyyy-mm-day(ex:2020-03-07), end_date(formatted: yyyy-mm-day(ex:2020-03-08)]
                       ex: filter_by = ['month', beginning_month(ex:yyyy-mm), end_month(ex:yyyy-mm)]
                       ex: filter_by = ['user', [usernames](ex:['nike', 'adidas'])]
                       ex: filter_by = ['keyword', [keywords](ex: ['acquire', 'sire'])] not case sensitive
            """
            filter_type = filter_by[0]
            filtered_comment_list = []
            if filter_type == 'full_date':
                s_date = filter_by[1].split('-')
                e_date = filter_by[2].split('-')

                s_datetime = datetime(int(s_date[0]), int(s_date[1]), int(s_date[2]))
                e_datetime = datetime(int(e_date[0]), int(e_date[1]), int(e_date[2]))

                for comment in comment_list:
                    f_date = comment.find_element_by_css_selector("time[class='FH9sR Nzb55']").get_attribute('datetime').split('-')
                    
                    # converting to datetime
                    f_datetime = datetime(int(f_date[0]), int(f_date[1]), int(f_date[2][:2]))

                    if f_datetime >= s_datetime and f_datetime <= e_datetime:
                        filtered_comment_list.append(comment)
            
            if filter_type == 'month':
                s_year, s_month = filter_by[1].split('-')
                e_year, e_month = filter_by[2].split('-')

                print(s_year, s_month)
                print(e_year, e_month)

                for comment in comment_list:
                    f_date = comment.find_element_by_css_selector("time[class='FH9sR Nzb55']").get_attribute('datetime').split('-')
                    f_month = int(f_date[1])
                    f_year = int(f_date[0])

                    print(f_year, f_month)

                    if f_year >= int(s_year) and f_year <= int(e_year):
                        if int(e_year) > f_year:
                            # if the end year is greater than current year, then we just make sure the month is >= month
                            if f_month >= int(s_month):
                                filtered_comment_list.append(comment)
                        if int(e_year) == f_year:
                            # if the end year is equal to current year, then we check month
                            if f_month <= int(e_month):
                                filtered_comment_list.append(comment)

            if filter_type == 'user':
                user_set = set(filter_by[1])
                for comment in comment_list:
                    # the user name
                    user = comment.find_element_by_css_selector("a[class='sqdOP yWX7d     _8A5w5   ZIAjV ']").text

                    if user in user_set:
                        filtered_comment_list.append(comment)

            if filter_type == 'keyword':
                key_word_lis = filter_by[1]
                for comment in comment_list:
                    # the comment text
                    comment_text = comment.find_element_by_css_selector("span[class='']").text.lower()

                    # check if text contains any of the keyword
                    if any(c in comment_text for c in key_word_lis if c in comment_text):
                        filtered_comment_list.append(comment)

            return filtered_comment_list



        def group_comments(comment_list, group_by=None):
            """
            group a selenium comment element by the filtered. returns a dictionary by the group by group by

            comment_list - the ul element that holds all the comment
            group_by - the group by filters are ['full_date', 'user']
            """

            if group_by is None:
                group_by_dict = defaultdict(list)

                for comment in comment_list:
                    # the user name
                    user = comment.find_element_by_css_selector("a[class='sqdOP yWX7d     _8A5w5   ZIAjV ']").text

                    # the comment text
                    comment_text = comment.find_element_by_css_selector("span[class='']").text

                    group_by_dict["comments"].append((user, comment_text))
                return group_by_dict
            
            if group_by == 'user':
                group_by_dict = defaultdict(list)
                for comment in comment_list:
                    # the user name
                    user = comment.find_element_by_css_selector("a[class='sqdOP yWX7d     _8A5w5   ZIAjV ']").text

                    # the comment text
                    comment_text = comment.find_element_by_css_selector("span[class='']").text

                    group_by_dict[user].append(comment_text)
                return group_by_dict
            
            if group_by == 'full_date':
                group_by_dict = defaultdict(dict)
                for comment in comment_list:
                    f_date = comment.find_element_by_css_selector("time[class='FH9sR Nzb55']").get_attribute('datetime')
                    f_date_lis = f_date.split('-')
                    
                    # the dates
                    year = int(f_date_lis[0])
                    month = int(f_date_lis[1])
                    day = int(f_date_lis[2][:2])

                    # the comment text
                    comment_text = comment.find_element_by_css_selector("span[class='']").text

                    if year not in group_by_dict:
                        group_by_dict[year] = defaultdict(dict)
                    if month not in group_by_dict[year]:
                        group_by_dict[year][month] = defaultdict(dict)
                    if day not in group_by_dict[year][month]:
                        group_by_dict[year][month][day] = []

                    group_by_dict[year][month][day].append(comment_text)

                return group_by_dict



        # go to ig post
        self.driver.get(ig_post_link)

        sleep(2)

        # the area where the comments are displayed
        post_comment_area_modal = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "EtaWk")))

        # load all the comments unless amount is specified
        while True:
            # this will continue to load comments until the load more button can't be found
            try:
                # current list of comments
                comment_list = post_comment_area_modal.find_elements_by_css_selector("ul[class='Mr508']")
                print("amount: ", len(comment_list))
                
                # if there is an amount specified
                if amount is not None:
                    if len(comment_list) >= amount:
                        break
                
                wait_time = randint(1,2)
                sleep(wait_time)

                load_more_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='dCJp8 afkep']")))
                load_more_button.click()

                wait_time = randint(1,2)
                sleep(wait_time)
            except Exception as e:
                print(e)
                break

        comment_list = post_comment_area_modal.find_elements_by_css_selector("ul[class='Mr508']")[:amount]

        if filter_by is not None:
            comment_list = filter_comments(comment_list, filter_by)
        
        return group_comments(comment_list, group_by)
        #f = io.open(r"C:\Users\acesw\Documents\Python Projects\Instagram Bot\personal test files\comment_test.txt", "w", encoding="utf-8")
        #f.write('\n'.join(comments))
        #f.close()
        #print(len(comments), "\n", comments)






    