from django.test import TestCase, Client
from NA_WebApp.models import Recipe, Labels, Diseases, Allergies
from django.contrib.auth.models import User

csrf_client = Client(enforce_csrf_checks=True)


class Model_Test(TestCase):

    def setUp(self):
        # we dont need :
         self.user = User.objects.create_user('özgecangal@no.com', 'özgecangal@no.com', '30071985Fe')
         self.client.login(username='özgecangal@no.com', password='30071985Fe')

    def test_label(self):
        Labels.objects.create(name="test label")
        is_saved = Labels.objects.filter(name="test label").count()
        self.assertEquals(is_saved, 1)

    def test_Recipe(self):
        rid = Recipe.objects.create(title="test recipe", description="test recipe desc", prepTime=10, cookTime=20, difficulity=1, user_id=self.user.id,
                                    instructions="test instructions", portions=4)

        is_saved = Recipe.objects.filter(id=rid.id).count()
        self.assertEquals(is_saved, 1)
