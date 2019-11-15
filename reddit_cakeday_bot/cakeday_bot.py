from datetime import datetime

import praw
import argparse

from praw.models import Redditor

from reddit_cakeday_bot.message_template import ReplyTemplate


class CakeDayBot:
    KEYWORD = "!cakecountdown"

    def __init__(self, subreddit: str):
        self.reddit = praw.Reddit('bot1')  # praw.ini file configured with credentials
        self.subreddit = self.reddit.subreddit(subreddit)

    def reply_to_command(self):
        comments = self.subreddit.stream.comments()

        for comment in comments:
            comment_text = comment.body

            if self.KEYWORD in comment_text:
                author = comment.author

                days_till_cakeday = self._calculate_difference(author)
                reply_message = self._create_reply_message(days_till_cakeday, author)

                comment.reply(reply_message)
                print("I just replied to the user!")

    def _calculate_difference(self, author: Redditor) -> int:
        author_cakeday_raw = author.created
        author_cakeday = datetime.fromtimestamp(int(author_cakeday_raw))
        time_now = datetime.now()

        difference = (author_cakeday - time_now).days % 365

        return difference

    def _create_reply_message(self, days_till_cakeday: int, author: Redditor) -> str:
        if days_till_cakeday is 0:
            reply_message = ReplyTemplate.REPLY_TEMPLATE_CAKEDAY.format(author_name=author.name)
        else:
            reply_message = ReplyTemplate.REPLY_TEMPLATE_NOT_CAKEDAY.format(author_name=author.name,
                                                                            days_till_cakeday=days_till_cakeday)
        reply_message += ReplyTemplate.DEVELOPER_INFORMATION
        return reply_message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter the subreddit where the bot is to be active.')
    parser.add_argument('--subreddit', help='Name of the subreddit', type=str, required=True)

    args = parser.parse_args()
    subreddit = args.subreddit
    CakeDayBot(subreddit).reply_to_command()
