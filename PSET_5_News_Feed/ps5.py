import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


#======================
# Data structure design
#======================

# Problem 1

class NewsStory (object):
    def __init__(self,guid,title,description,link,pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        
    def is_phrase_in(self,text):
        
        text_words= []
        text = text.lower()
        for ch in text:
            if ch not in string.punctuation:
                text_words.append(ch)
            else:
                text_words.append(" ")
        text_temp = "".join(text_words)
        text_string = " ".join(text_temp.split()) + " "
        phrase = self.phrase + " "
        if phrase in text_string:
            return 1
        else:
            return 0

    
# Problem 3
            
class TitleTrigger(PhraseTrigger):
    
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
            
class DescriptionTrigger(PhraseTrigger):
    
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
    
# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
  
    def __init__(self, pubdate):
        format = "%d %b %Y %H:%M:%S"
        date_time = datetime.strptime(pubdate,format)
        self.date_time = date_time
        

# Problem 6
class BeforeTrigger(TimeTrigger):
        
    def evaluate(self, story):
        try:
            if story.get_pubdate() < self.date_time:
                return 1
        except:
            self.date_time = self.date_time.replace(tzinfo= pytz.timezone("EST"))
            if story.get_pubdate() < self.date_time:
                return 1 
        return 0
    
class AfterTrigger(TimeTrigger):
    
    def evaluate(self, story):
        try:
            if story.get_pubdate() > self.date_time:
                return 1
        except:
            self.date_time = self.date_time.replace(tzinfo= pytz.timezone("EST"))
            if story.get_pubdate() > self.date_time:
                return 1 
        return 0

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trig = trigger
        
    def evaluate(self, story):
        if self.trig.evaluate(story) == 1:
            return 0
        else:
            return 1

# Problem 8
class AndTrigger(Trigger):
    def __init__(self,Trigger1,Trigger2):
        self.trig1 = Trigger1
        self.trig2 = Trigger2
    def evaluate(self, story):
        if self.trig1.evaluate(story) == 1:
            if self.trig2.evaluate(story) == 1:
                return 1
        return 0

# Problem 9
class OrTrigger(Trigger):
    def __init__(self,Trigger1,Trigger2):
        self.trig1 = Trigger1
        self.trig2 = Trigger2
    def evaluate(self, story):
        if self.trig1.evaluate(story) == 1:
            return 1
        if self.trig2.evaluate(story) == 1:
            return 1
        return 0

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    story_filtered = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story) == 1:
                story_filtered.append(story)
                break
    return story_filtered

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # 'lines' is the list of lines that you need to parse and for which you need
    # to build triggers

    # Initialize trigger mapping dictionary
    t_map = {"TITLE": TitleTrigger,
            "DESCRIPTION": DescriptionTrigger,
            "AFTER": AfterTrigger,
            "BEFORE": BeforeTrigger,
            "NOT": NotTrigger,
            "AND": AndTrigger,
            "OR": OrTrigger
            }

    # Initialize trigger dictionary, trigger list
    trigger_dict = {}
    trigger_list = [] 

    # Helper function to parse each line, create instances of Trigger objects,
    # and execute 'ADD'
    def line_reader(line):
        data = line.split(',')
        if data[0] != "ADD":
            if data[1] == "OR" or data[1] == "AND":
                trigger_dict[data[0]] = t_map[data[1]](trigger_dict[data[2]],
                        trigger_dict[data[3]])
            else:
                trigger_dict[data[0]] = t_map[data[1]](data[2])
        else: 
            trigger_list[:] += [trigger_dict[t] for t in data[1:]]

    for line in lines:
        line_reader(line)
    
    return trigger_list
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("election")
#        t2 = DescriptionTrigger("Trump")
#        t3 = DescriptionTrigger("Clinton")
#        t4 = AndTrigger(t2, t3)
#        triggerlist = [t1, t4]

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

