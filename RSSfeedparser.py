from pprint import pprint
import feedparser
import redis
import time

# Max age (in seconds) of each feed in the cache
MAX_CACHED_ELAPSED_TIME = 300

# Key-value store with the following structure:
# {'Feed URL': (Timestamp, RSS Feed)}
# {'Title': (Timestamp, RSS Feed Entry)}
cache = redis.StrictRedis(host='localhost', port=6379, db=0)


class Feed(object):

    def __init__(self, url):
        self.feed_url = url

    def isCached(self):
        # Try to get the tuple (Timestamp, RSS Feed) from the cache.
        feed = cache.get(self.feed_url)

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

    def getFeed(self):
        if not self.isCached():
            self.setFeed()
        return cache.get(self.feed_url)[1]

    # TODO: Check for errors
    def parseFeed(self):
        return feedparser.parse(self.feed_url)

    def setFeed(self):
        feed = self.parseFeed()
        cache.set(self.feed_url, (time.time(), feed))


class FeedEntry(object):

    def __init__(self, title, link, summary, published):
        self.title = title
        self.link = link
        self.summary = summary
        self.published = published


if __name__ == "__main__":
    pass
