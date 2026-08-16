from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Tweet


class HomeNavigationTests(TestCase):
    def test_root_url_loads_the_existing_index_page(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Welcome to the Tweet App')

    def test_home_and_feed_navigation_links_use_application_routes(self):
        response = self.client.get(reverse('index'))

        self.assertContains(response, f'href="{reverse("index")}"', count=2)
        self.assertContains(response, f'href="{reverse("tweet_list")}"')

    def test_layout_loads_the_matching_bootstrap_javascript_bundle(self):
        response = self.client.get(reverse('index'))

        self.assertContains(
            response,
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js',
        )


class TweetTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='owner')
        self.other_user = User.objects.create(username='other')

    def create_tweet(self, text, user=None, photo=None):
        return Tweet.objects.create(
            user=user or self.owner,
            text=text,
            photo=photo,
        )


class TweetFeedTests(TweetTestCase):
    def test_feed_loads_and_displays_newest_tweets_first(self):
        older_tweet = self.create_tweet('Older tweet')
        newer_tweet = self.create_tweet('Newer tweet')
        Tweet.objects.filter(pk=older_tweet.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        Tweet.objects.filter(pk=newer_tweet.pk).update(created_at=timezone.now())

        response = self.client.get(reverse('tweet_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Older tweet')
        self.assertContains(response, 'Newer tweet')
        self.assertLess(
            response.content.find(b'Newer tweet'),
            response.content.find(b'Older tweet'),
        )

    def test_empty_feed_loads_successfully(self):
        response = self.client.get(reverse('tweet_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the Tweet App')
        self.assertContains(response, 'No tweets yet.')


class TweetCreationTests(TweetTestCase):
    def test_authenticated_user_can_create_a_tweet(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('tweet_create'),
            {'text': 'A newly created tweet'},
        )

        self.assertRedirects(response, reverse('tweet_list'))
        tweet = Tweet.objects.get(text='A newly created tweet')
        self.assertEqual(tweet.user, self.owner)


class TweetAuthorizationTests(TweetTestCase):
    def test_unauthenticated_user_cannot_access_tweet_management_pages(self):
        tweet = self.create_tweet('Protected tweet')
        urls = [
            reverse('tweet_create'),
            reverse('tweet_edit', args=[tweet.pk]),
            reverse('tweet_delete', args=[tweet.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f'{reverse("login")}?next={url}')


class TweetEditTests(TweetTestCase):
    def test_owner_can_edit_their_tweet(self):
        tweet = self.create_tweet('Original tweet')
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('tweet_edit', args=[tweet.pk]),
            {'text': 'Updated tweet'},
        )

        self.assertRedirects(response, reverse('tweet_list'))
        tweet.refresh_from_db()
        self.assertEqual(tweet.text, 'Updated tweet')

    def test_user_cannot_edit_another_users_tweet(self):
        tweet = self.create_tweet('Another users tweet', user=self.other_user)
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('tweet_edit', args=[tweet.pk]),
            {'text': 'Unauthorized update'},
        )

        self.assertEqual(response.status_code, 404)
        tweet.refresh_from_db()
        self.assertEqual(tweet.text, 'Another users tweet')


class TweetDeleteTests(TweetTestCase):
    def test_delete_confirmation_shows_the_tweet_text(self):
        tweet = self.create_tweet('Tweet shown before deletion')
        self.client.force_login(self.owner)

        response = self.client.get(reverse('tweet_delete', args=[tweet.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tweet.text)

    def test_owner_can_delete_their_tweet(self):
        tweet = self.create_tweet('Tweet to delete')
        self.client.force_login(self.owner)

        response = self.client.post(reverse('tweet_delete', args=[tweet.pk]))

        self.assertRedirects(response, reverse('tweet_list'))
        self.assertFalse(Tweet.objects.filter(pk=tweet.pk).exists())

    def test_user_cannot_delete_another_users_tweet(self):
        tweet = self.create_tweet('Another users tweet', user=self.other_user)
        self.client.force_login(self.owner)

        response = self.client.post(reverse('tweet_delete', args=[tweet.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(pk=tweet.pk).exists())


class TweetSearchTests(TweetTestCase):
    def setUp(self):
        super().setUp()
        self.matching_tweet = self.create_tweet('Django search is useful')
        self.other_tweet = self.create_tweet('A different tweet')

    def test_empty_search_returns_the_normal_feed(self):
        response = self.client.get(reverse('tweet_list'))

        self.assertContains(response, self.matching_tweet.text)
        self.assertContains(response, self.other_tweet.text)
        self.assertEqual(response.context['search_query'], '')

    def test_whitespace_only_search_returns_the_normal_feed(self):
        response = self.client.get(reverse('tweet_list'), {'q': '   '})

        self.assertContains(response, self.matching_tweet.text)
        self.assertContains(response, self.other_tweet.text)
        self.assertEqual(response.context['search_query'], '')

    def test_matching_search_returns_only_matching_tweets(self):
        response = self.client.get(reverse('tweet_list'), {'q': 'search'})

        self.assertContains(response, self.matching_tweet.text)
        self.assertNotContains(response, self.other_tweet.text)

    def test_search_is_case_insensitive(self):
        response = self.client.get(reverse('tweet_list'), {'q': 'dJaNgO'})

        self.assertContains(response, self.matching_tweet.text)
        self.assertNotContains(response, self.other_tweet.text)

    def test_non_matching_search_shows_empty_result_state(self):
        response = self.client.get(reverse('tweet_list'), {'q': 'missing'})

        self.assertContains(response, 'No tweets found.')
        self.assertNotContains(response, self.matching_tweet.text)

    def test_search_query_is_preserved_after_submission(self):
        response = self.client.get(reverse('tweet_list'), {'q': '  Django  '})

        self.assertContains(response, 'value="Django"')
        self.assertEqual(response.context['search_query'], 'Django')


class TweetPhotoDisplayTests(TweetTestCase):
    def test_feed_displays_tweets_with_and_without_photos(self):
        tweet_with_photo = self.create_tweet(
            'Tweet with a photo',
            photo='tweets/photos/example.png',
        )
        tweet_without_photo = self.create_tweet('Tweet without a photo')

        response = self.client.get(reverse('tweet_list'))

        self.assertContains(response, tweet_with_photo.text)
        self.assertContains(response, 'src="/media/tweets/photos/example.png"')
        self.assertContains(response, 'alt="Photo for tweet by owner"')
        self.assertContains(response, tweet_without_photo.text)
        self.assertContains(response, '<img', count=1)
