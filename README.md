# Reddit Giveaway Bot

This Reddit bot manages creating custom giveaways for items such as
  product keys (for video games, apps, etc.).
  
It can either be given a url of an existing Reddit post to crawl and award
  users or it can create a new post in a given subreddit with all the
  information necessary for users to understand the rules of the giveaway.

## Features

  * Intelligent assignment: a single account will be eligible for only one
    award, no matter how many comments are made by the account.
  * Limit by account age: eligible accounts can be limited to accounts created
    at least *N* days ago to prevent sockpuppets.
  * Keywords: to prevent chatter from distracting the bot, an optional
    keyword can be required for the bot for it to 
  * Reply or PM: the bot can either reply to the user with his/her prize,
    or directly PM the user to keep the information private.
  * Multiple sort options: prizes can be assigned either by timestamp
    (oldest first) or randomly, after a given wait time.
  * Completely customizable messages: every message that the bot sends to
    Reddit, whether it's the post contents, rules, or replies, may be
    tailored to a specific contest without having to edit any code.
  * Followup: Once the bot runs out of prizes to give out, it will edit
    the original post with a message that the contest is over.


## Warnings

  * The bot marks comments as *read* when it sees them the first time, so
    subsequent edits to those comments are ignored.
  * If a user comments and the account age is below the minimum, the account
    will be flagged as ineligible even if the contest extends long enough to
    make the user eligible before it ends.
  * There is no persistence built in to the bot. If (God forbid) it breaks
    midway through due to Reddit being down or the bot process is killed,
    there is no record of who was assigned which key (and thus no way to
    restart the contest where the bot left off).


## Setup

This Python program requires the [Reddit API](https://github.com/mellort/reddit_api)
to be installed before running.

A keyfile must be created before the bot can be run. This file consists of
a list of prizes (whether it be a product key, password, or something else),
one per line.

To customize the contest content, open the file `strings.py`. Between each pair
of quotes (triple quotes let you continue the string onto multiple lines)
type in the content that you wish the bot to post.

To determine which paramaters are available, what they do, and where to put
them just run the command `python redditgiveaway.py --help`.

## Examples

To just get the bot running with the simplest set of parameters, use this command:

    python redditgiveaway.py -u myuseragent -r askreddit keys.txt username password
