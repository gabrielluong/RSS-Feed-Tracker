from lib.dropboxwrapper.dropboxwrapper import Dropbox

import feedparser
import re
import redis
import time
import requests

# Max age (in seconds) of each feed in the cache
MAX_CACHED_ELAPSED_TIME = 300

# Key-value store with the following structure:
# {'Feed URL': (Timestamp, RSS Feed)}
# {'Title': RSS Feed Entry}
cache = redis.StrictRedis(host='localhost', port=6379, db=0)


class FeedTracker(Dropbox):

    def __init__(self):
        # List of Feed objects
        self.feeds = []

    def add_feed(self, feed):
        self.feeds.append(feed)

    def remove_feed(self, feed):
        self.feeds.remove(feed)

    def update_feeds(self):
        for feed in self.feeds:
            feed.update()
            self.process_updates(feed)

    # If Dropbox client is connected, download file from entry link and upload
    # to Dropbox.
    def process_updates(self, feed):
        if self.client is not None:
            entries = feed.get_matches()

            while entries:
                entry = entries.pop(0)
                response = requests.get(entry.link)
                with open("temp.torrent", "wb") as f:
                    f.write(response.content)

                self.upload_file("temp.torrent")


class Feed(object):

    def __init__(self, url):
        self.feed_url = url
        # List of regex search patterns that will pattern match with a feed
        # entry title
        self.filters = []
        self.new_matches = []
        self.cache_feed_entry()

    def is_cached(self):
        # Try to get the tuple (Timestamp, RSS Feed) from the cache.
        feed = cache.get(self.url)

        if feed:
            # Feed is cached. Check if the cache of the feed has expired.
            elapsed_time = time.time() - feed[0]

            # Cache for this feed has expired, and no longer valid.
            if elapsed_time > MAX_CACHED_ELAPSED_TIME:
                return False
            else:
                return True
        else:
            # Feed is not cached.
            return False

    def is_cached(self, title):
        return cache.get(title)

    def get_feed(self):
        if not self.is_cached():
            self.set_feed()
        return cache.get(self.feed_url)[1]

    def update(self):
        feed = self.get_feed()

        for entry in feed['items']:
            if not self.is_cached(entry.title):
                cache.set(entry.title, entry)
                self.find_matches(entry)
            else:
                break

    # TODO: Check for errors
    def parse_feed(self):
        return feedparser.parse(self.feed_url)

    def set_feed(self):
        feed = self.parse_feed()
        cache.set(self.feed_url, (time.time(), feed))

    def add_filter(self, pattern):
        self.filters.append(re.compile(pattern))

    def get_filters(self):
        return self.filters

    def get_matches(self):
        return self.new_matches

    def is_match(self, pattern, title):
        return pattern.match(title)

    def find_matches(self, entry):
        patterns = self.get_filters()

        for pattern in patterns:
            if self.is_match(entry.title):
                if not entry.title in self.new_matches:
                    self.new_matches.append(entry.title)
                break

    def remove_match(self, title):
        self.new_matches.remove(title)

if __name__ == "__main__":
    pass
