from datetime import datetime

import celery
from django.db import DatabaseError, transaction

from clouds.models import SubmittedUrls, Words
from lib.html_parser import parse_url


def count_words(html_text: str) -> dict:
    """count words in html text

    Args:
        html_text (str): return text from beautifulsoup

    Returns:
        dict: dictionary of counts
    """
    text_in_list = html_text.split(" ")

    word_count = {}
    for text in text_in_list:
        lower_case_text = text.lower()
        if word_count.get(lower_case_text):
            word_count[lower_case_text] += 1
        else:
            word_count[lower_case_text] = 1

    return word_count


def update_words(word_count: dict) -> None:
    """Update specific word counts

    Args:
        word_count (dict): dicitonary of words and count
    """
    for k, v in word_count.items():
        try:
            # Ensure when the word is grabbed from the db
            # nothing else can update it
            word = Words.objects.select_for_update().get(word=k)
        except Words.DoesNotExist:
            Words.objects.create(word=k, count=v)
            continue

        word.count += v
        word.save()


@celery.task(name="clouds.tasks.add")
def add() -> None:

    with transaction.atomic():
        try:
            # Adding check that will make a query fail if there is already a lock to prevent duplicate loops
            submitted_url = (
                SubmittedUrls.objects.select_for_update(nowait=True)
                .filter(is_processing=False)
                .earliest("submit_datetime_utc")
            )
        except SubmittedUrls.DoesNotExist:
            print("nothing to process at the moment")
            return
        except DatabaseError as e:
            print("row is locked, skipping")
            return

        # Commit everything or nothing
        submitted_url.is_processing = True
        submitted_url.processing_start_datetime_utc = datetime.now()

        if html_text := parse_url(submitted_url.url):
            word_count = count_words(html_text)
            update_words(word_count)

        submitted_url.is_complete = True
        submitted_url.save()
