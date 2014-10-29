from django.test import TestCase, Client
from models import *

class GrumblrModelsTest(TestCase):
    def test_simple_add_post(self):
        self.assertTrue(TextPost.objects.all().count() == 0)
        self.assertTrue(User.objects.all().count() == 0)
        user = User(username='hello', email='hello@blah.com', password='fun')
        user.save()
        self.assertTrue(User.objects.all().count() == 1)
        new_post = TextPost(user=user, text='test item')
        new_post.save()
        self.assertTrue(TextPost.objects.all().count() == 1)
        self.assertTrue(TextPost.objects.filter(text__contains='test'))
        

class GrumblrTest(TestCase):
                                # Seeds the test database with data we obtained
    fixtures = ['sample-data']  # from python manage.py dumpdata 


    def test_home_page(self):
        client = Client()
        client.post('/login/', {'username': 'notajingoist', 'password': 'test'})
        response = client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        client = Client()
        client.post('/login/', {'username': 'notajingoist', 'password': 'test'})
        
        sample_post = 'This is the text for my sample post'
        sample_comment = 'This is the text for my sample comment'
        client.post('/text-post/', {'text': sample_post})
        response = client.get('/home/')
        self.assertTrue(response.content.find(sample_post) > 0)
        
        response = client.post('/comment/home/1/1/', {'text': sample_comment})
        self.assertTrue(response.content.find(sample_comment) > 0)
