from django.db import models
from django.contrib.auth.models import User


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
    married = models.IntegerField(choices=EnYesNo.choices, null=True, default=EnYesNo.NO)
    hasKids = models.IntegerField(choices=EnYesNo.choices, null=True, default=EnYesNo.NO)

    # geo location points :
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, default=41.086203)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, default=29.044378)

    def __str__(self):
        return self.user.username + ' Profile'
