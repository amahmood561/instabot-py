
from instapy import InstaPy
from instapy import smart_run
instagram_username = ''  # <-  username here
instagram_password = ''  # <-  password here

# instapy object session
# set headless_browser=True to run InstaPy in the background
sesh = InstaPy(username=instagram_username,
                  password=instagram_password)

with smart_run(sesh):
    # general settings
    sesh.set_dont_include(["friend1", "friend2", "friend3"])

    # set % of ppl to follow
    sesh.set_do_follow(True, percentage=50)

    #sets the % of posts you want to place comment
    sesh.set_do_comment(True, percentage=100)

    #string list of comments bot will use
    sesh.set_comments(["hi @{}, have a look", "Great content @{} have a look", ":heart_eyes: :heart_eyes: :heart_eyes: @{}"])

    # set the quotas for the daily and hourly actions
    sesh.set_quota_supervisor(enabled=True, peak_comments_daily=250, peak_comments_hourly=30, peak_likes_daily=250,
                                 peak_likes_hourly=30, sleep_after=['likes', 'follows'])

    #config to figure out who to foloow
    sesh.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=True,
                                    max_followers=3000,
                                    min_followers=150,
                                    min_following=50)

    #tags to get posts from and amout is the actions you want
    sesh.like_by_tags(['python3','javascript'], amount=300)

sesh.end()