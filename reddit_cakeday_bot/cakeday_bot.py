import praw
import argparse


class CakeDayBot:
    KEYWORD = "!cakecountdown"

    def __init__(self, subreddit):
        self.reddit = praw.Reddit('bot1')  # praw.ini file configured with credentials
        self.subreddit = self.reddit.subreddit(subreddit)

    def reply_to_summoning(self):
        comments = self.subreddit.stream.comments()

        for comment in comments:
            comment_text = comment.body

            if self.KEYWORD in comment_text:
                comment.reply("I am a bot and have no brain")
                print("I just replied to the user!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter the subreddit where the bot is to be active.')
    parser.add_argument('--subreddit', help='Name of the subreddit', type=str, required=True)

    args = parser.parse_args()
    subreddit = args.subreddit
    CakeDayBot(subreddit).reply_to_summoning()
