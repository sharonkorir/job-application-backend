

from django.test import TestCase
from .models import *
# Create your tests here.

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

