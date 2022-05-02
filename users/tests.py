

from django.test import TestCase
from .models import *

# Create your tests here.
class JobseekerTestClass(TestCase):
    def setUp(self):
        self.user = User(
            id=1,username='Shar', email= 'sharon@gmail.com',first_name='Sharon',last_name='Korir', is_jobseeker=True)
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def tearDown(self):
        self.user.delete_user()

    def test_save_method(self):
        self.user.save_user()
        users  = User.objects.all()
        self.assertTrue(len(users)>0)

class TestJob(TestCase):
    def setUp(self):
        self.job = Job(id=1, title='12moi', location='Rongai')
        self.job.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.job, Job))

    def test_save_job(self):
        self.job.save()

    def test_delete_job(self):
        self.job.delete()

