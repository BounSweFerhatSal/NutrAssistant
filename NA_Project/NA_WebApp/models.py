from django.db import models
from django.contrib.auth.models import User


class Diseases(models.Model):
    diseaseName = models.CharField(max_length=100)

    def __str__(self):
        return self.diseaseName + ' (id: ' + str(self.id) + ')'


class Allergies(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' (id: ' + str(self.id) + ')'


class Labels(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' (id: ' + str(self.id) + ')'


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calorie = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    FDC_ID = models.CharField(max_length=8)

    def __str__(self):
        return self.name + ' (id: ' + str(self.id) + ',FDC_ID: ' + self.FDC_ID + ')'


class Profile(models.Model):
    # yes no enum
    class EnYesNo(models.IntegerChoices):
        NO = 0
        YES = 1

    # Gender enum
    class EnGender(models.IntegerChoices):
        Male = 1
        Female = 2
        Others = 3

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    # explanation :
    # here we tell the django store our files in 'profile_pics' folder which is in the folder that we specify in settings.py file with MEDIA_ROOT parameter
    # for this project it is set to media folder in the base dir of the project
    # hence , our avatar images will be stored in projectpath/media/profile_pics folder
    # Off courde we have to specify a url pattern to access taht medai path :
    # so add urls.py of project ( not app) below code :
    # if settings.DEBUG:
    #    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    #
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    gender = models.IntegerField(choices=EnGender.choices, null=True)
    birthYear = models.IntegerField(null=True)
    married = models.IntegerField(choices=EnYesNo.choices, null=True)
    hasKids = models.IntegerField(choices=EnYesNo.choices, null=True)

    # geo location points :
    lat = models.DecimalField(max_digits=20, decimal_places=18, null=True, default=41.086203)
    lng = models.DecimalField(max_digits=20, decimal_places=18, null=True, default=29.044378)

    def __str__(self):
        return self.user.username + ' Profile'


class Profile_Diseases(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.user.username + ' ' + self.disease.diseaseName


class Profile_Allergies(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergies, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.user.username + ' ' + self.allergy.name


class Profile_FoodPreferences(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.user.username + ' ' + self.label.name


class Profile_RestrictedLabels(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.user.username + ' ' + self.label.name


class Profile_RestrictedIngredients(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.user.username + ' ' + self.label.name
