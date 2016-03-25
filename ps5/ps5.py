# 6.00 Problem Set 5
# RSS Feed Filter
# Name: Elijah Ada
# Collaborators:
# Time:

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory


class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()

        for punc in string.punctuation:
            text = text.replace(punc, " ")
        splitText = text.split(" ")
        return word in splitText


# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, otherTrigger):
        self.otherTrigger = otherTrigger


    def evaluate(self, story):
        return not self.otherTrigger.evaluate(story)

# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)



# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        title = story.get_title()
        subject = story.get_subject()
        summary = story.get_summary()
        return self.phrase in title or self.phrase in subject or self.phrase in summary

# ======================
# Part 3
# Filtering
# ======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStories.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


# ======================
# Part 4
# User-Specified Triggers
# ======================
def createTrigger(trigger_map, trigger_type, parameters, name):

        if trigger_type == "TITLE":
           trigger = TitleTrigger(parameters[0])

        elif trigger_type == "SUBJECT":
            trigger = SubjectTrigger(parameters[0])

        elif trigger_type == "SUMMARY":
            trigger = SummaryTrigger(parameters[0])

        elif trigger_type == "NOT":
            trigger = TitleTrigger(trigger_map[parameters[0]])

        elif trigger_type == "AND":
            trigger = AndTrigger(trigger_map[parameters[0]], trigger_map[parameters[1]])

        elif trigger_type == "OR":
            trigger = OrTrigger(trigger_map[parameters[0]], trigger_map[parameters[1]])

        elif trigger_type == "PHRASE":
            trigger = PhraseTrigger(" ".join(parameters))
        else:
            return None

        trigger_map[name] = trigger


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [line.rstrip() for line in triggerfile.readlines()]
    lines = []
    list_of_triggers = []
    trigger_map = {}
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

        # TODO: Problem 11
        # 'lines' has a list of lines you need to parse
        # Build a set of triggers from it and
        # return the appropriate ones
        # print "lines=", line

    for line in lines:
        splitline = line.split(" ")

        # adding trigger to list
        if splitline[0] == "ADD":
            for potentialTrigs in splitline[1:]:
                list_of_triggers.append(trigger_map[potentialTrigs])
        # making new trigger
        else:
           trigger = createTrigger(trigger_map, splitline[1], splitline[2:],splitline[0])

    # print "List of Triggers =", list_of_triggers
    return list_of_triggers



import thread


def main_thread(p):

    # TODO: Problem 11
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []

    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)

        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            print ". . .",
            if story.get_guid() not in guidShown:
                newstories.append(story)
        print ". . ."
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()
