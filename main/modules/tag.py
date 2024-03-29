from django.utils import timezone

import time
import re

from main.models import SearchWord

from .crawler import Crawler


class TagSpider(Crawler):
    BASE_URL = 'https://www.instagram.com/'

    def __init__(self):
        super().__init__()

    def start(self):
        # self.login()
        while True:
            word = SearchWord.objects.filter(scored_at__isnull=True).order_by('id').first()
            if word is None:
                time.sleep(5)
            else:
                word.scored_at = timezone.now()
                word.save()
                for post_from_word in self.posts_from_word(True,
                                                           TagSpider.BASE_URL + 'explore/tags/' + word.word + '/'):
                    self.scoring(word.word, post_from_word)
                    for tag in SearchWord.objects.filter(scored_at__isnull=False).order_by('-score')[300:]:
                        tag.delete()

    def scoring(self, word, post):
        self.url = post
        self.driver.get(post)
        time.sleep(5)
        self.driver.get(post)
        time.sleep(5)
        try:
            text = self.wait.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/*[2]').text
            tags = re.compile(r'#(\w+)').findall(text)
            for tag in tags[:2]:
                if re.match(r'^[^a-zA-Z]*$', tag):
                    SearchWord.objects.update_or_create(word=tag)
            score = self.score(text)
            word_ob = SearchWord.objects.get(word=word)
            word_ob.score += score
            word_ob.save()
        except AttributeError:
            pass
