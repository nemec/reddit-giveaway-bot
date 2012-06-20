from datetime import datetime, timedelta
import argparse
import logging
import random
import reddit
import time
import sys

import strings


logger = logging.getLogger("giveawaybot")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

def humanize_seconds(seconds):
  """
  Returns a humanized string representing time difference
  between now() and the input timestamp.
  
  The output rounds up to days, hours, minutes, or seconds.
  4 days 5 hours returns '4 days'
  0 days 4 hours 3 minutes returns '4 hours', etc...
  """  
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  
  if hours > 0:
    if hours == 1:  return "{0} hour".format(hours)
    else:           return "{0} hours".format(hours)
  elif minutes > 0:
    if minutes == 1:return "{0} minute".format(minutes)
    else:           return "{0} minutes".format(minutes)
  elif seconds > 0:
    if seconds == 1:return "{0} second".format(seconds)
    else:           return "{0} seconds".format(seconds)
  else:
      return None

parser = argparse.ArgumentParser(description="Bot to run giveaways on Reddit.")
parser.add_argument('-u', '--useragent', metavar='name',
default='giveawaybot',
  help="The user agent to use when connecting to Reddit. Recommended to make "
    "it unique to your bot, though a default is provided.")
parser.add_argument('-a', '--age', type=int, default=1,
  help="The minimum age (in days) of user accounts that are eligible for "
    "the giveaway (prevents sockpuppet accounts)")
parser.add_argument('-p', '--poll', type=int, default=30,
  help="Seconds between polls for new comments. Recommended to be >30 seconds "
    "because Reddit caches results for that long.")
parser.add_argument('-k', '--keyword', default=None,
  help="If provided, this keyword must be present in the comment for it to "
    "be eligible for a prize. Prevents chatter from triggering a prize.")
parser.add_argument('--reply', choices=['inline', 'pm'], default='pm',
  help="Whether to reply with the prize inline or through pm. Defaults "
    "to pm.")


parser.add_argument('--random', action='store_true',
  help="Assigns prizes randomly instead of by submission time. -w is required "
    "if this argument is provided.")
parser.add_argument('-w', '--wait', type=int, default=None,
  help="Time in minutes to wait before checking comments. Only used in "
    "combination with --random. Recommended to be >30 minutes.")


group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--submission', default=None,
  help="URL of an existing post to crawl for submissions. Optional use "
    "instead of -r.")
group.add_argument('-r', '--reddit', default=None,
  help="The subreddit to post the giveaway to. This option creates a new "
    "post managed by the bot and must not be specified with -s.")

parser.add_argument('keyfile',
  help="A file path containing the keys to distribute (one per "
    "line). Leading and trailing whitespace will be removed from each key.")
parser.add_argument('username',
  help="The Reddit username to run the giveaway as. If a submission url is "
    "manually passed in, the same user who created it must be used.")
parser.add_argument('password',
  help="The password for the Reddit account.")

args = parser.parse_args(sys.argv[1:])


if args.random and not args.wait:
  logger.error("Random assignment of prizes must specify a wait time (-w), "
    "otherwise first responders will have higher probability of winning. "
    "At least 30 minutes of wait time is recommended.")
  sys.exit(1)


min_account_age = timedelta(days=args.age)

keys = []
try:
  with open(args.keyfile, 'r') as f:
    keys = f.readlines()
except IOError:
  logger.error("Could not open the key file {0}.".format(keyfile))
  sys.exit(1)


logger.info("Logging in...")
r = reddit.Reddit(user_agent=args.useragent)
r.login(args.username, args.password)


if args.reddit:
  try:
    logger.info("Creating submission...")
    body = strings.submission_body
    if args.keyword:  # Alert users that they need a keyword
      body += "\n\n" + strings.keyword_message.format(keyword=args.keyword)
    if args.random:  # Alert users that prizes are random
      utc_wait = (datetime.utcnow() + timedelta(minutes=30)).strftime("%H:%M:%S UTC")
      body += "\n\n" + strings.random_rule.format(wait=args.wait, utc=utc_wait)
    else:  # Alert users that prizes 
      body += "\n\n" + strings.timestamp_rule
    sub = r.submit(args.reddit, strings.submission_title, text=body)
    args.submission = sub.permalink
    logger.warning("Submission can be found at " + str(sub.permalink))
  except reddit.errors.APIException as err:
    logger.error("Error with submission: " + str(err))
    

authors = set([args.username])  # Contains usernames of users that already won or accounts too young
checked_comment_ids = set()

if args.random:
  logger.info("Sleeping for {0} minutes while users comment...".format(args.wait))
  time.sleep(args.wait * 60)

while len(keys) > 0:
  awarded = len(keys)
  logger.info("Checking comments...")
  s = r.get_submission(args.submission)
  if args.random:
    random.shuffle(s.comments)
  else:
    s.comments.sort(key=lambda c: c.created_utc)
  for comment in s.comments:
    if len(keys) == 0:
      break

    author = comment.author
    # Have we seen this comment before?
    if (author is not None and author.name not in authors and
        comment.id not in checked_comment_ids):
      #checked_comment_ids.add(comment.id)
      # Ensure keyword is present if required
      if args.keyword and args.keyword not in comment.body:
        continue
      
      # Check account age
      created_date = datetime.fromtimestamp(int(author.created_utc))
      #authors.add(author.name)
      if (datetime.now() - min_account_age) < created_date:
        logger.warn("Author {0} is too new.".format(author.name))
        continue
      
      try:
        message = strings.reply_message.format(prize=keys.pop(0).strip(),
          url=args.submission)
        if args.reply == "inline":
          comment.reply(message)
        else:
          r.compose_message(author.name, strings.reply_title, message)
      except AttributeError as err:
        logging.error("Missing value in strings file: {0}".format(err))
        sys.exit(1)
  
  if len(keys) < awarded:
    logger.info("Awarded {0} new prizes!".format(awarded - len(keys)))
  if len(keys) > 0:
    time.sleep(args.poll)
try:
  if s.selftext:
    s.edit(s.selftext + "\n\n**EDIT:** " + strings.end_message)
  else:
    s.edit(strings.end_message)
except reddit.errors.APIException:
  logger.warning("Unable to edit original post to warn that giveaway "
    "is over. Recommend manually editing the post.")
logger.info("Prizes are all distributed, exiting.")
