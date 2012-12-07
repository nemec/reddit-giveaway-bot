
# The title and body of self post created for the giveaway.
# Only relevant if the -r or --reddit options are provided
# on the command line.
submission_title = """Giveaway happening now!"""

submission_body = """Comment on this post to win a prize."""


# A message appended to the submission_body when a keyword is
# required to signal the bot for a giveaway (-k/--keyword).
# All occurances of {keyword} will be replaced with the
# keyword (leading and trailing whitespace will be stripped).
keyword_message = """To filter out chatter, the word
`{keyword}` must be present in your comment if you would
like to get a prize."""


# If prizes are distributed by submission time (the default),
# this message will be appended to the submission_body to
# let users know how prizes will be distributed.
timestamp_rule = """Prizes will be given out on a first-come
first-serve basis, comment now before all the prizes are gone!."""

# If prizes are distributed randomly, this message will be
# appended to the submission_body to let users know
# how prizes will be distributed.
# Parameters:
#   {wait}: Replaced with the wait time, humanized (eg. "30 minutes")
#   {utc}: Replaced with the exact UTC time that the bot will begin
#     distributing prizes.
random_rule = """Prizes will be given out randomly after a 
period of {wait} minutes (at {utc}). There is no guarantee that prizes
will be available once that time passes."""


what_is_this = """This contest is being managed by a bot.
To get him to cater at your next giveaway, please visit the
[Github page](https://github.com/nemec/reddit-giveaway-bot)!"""


# The title of the pm that winners will receive.
# This will not be used if the bot replies inline with the prizes.
reply_title = """Giveaway Prize"""

# The contents of the reply/pm that winners will receive.
# Message is formatted via Reddit's Markup.
# All occurances of {prize} will be replaced with the prize value
# and occurances of {url} will be replaced with the post url.
# '{' and '}' can be entered into the message by doubling
# them up ({{ and }}).
prize_reply_message = """Congratulations, you are a lucky recipient of
a giveaway prize!

{prize}

[Which contest?]({url})"""

generic_reply_message = """Congratulations, you are the lucky recipient of
a giveaway prize!

Check your inbox for your prize."""

# A message edited onto the end of the post once
# bot has run out of prizes to give out.
end_message = "I'm all out of prizes! Thanks for playing."
