from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Messages(models.Model):
    #timestamp = models.DateTimeField(auto_now_add=True)
    #uuser = models.ForeignKey("Users")
    username = models.CharField(max_length=256)
    title = models.CharField(max_length=512)
    content = models.TextField(max_length=256)
    publish = models.DateTimeField(auto_now_add=True)

    # 为了显示
 #   def __str__(self):
  #      tpl = '<Message:[username={username}, title={title}, content={content}, publish={publish}]>'
   #     return tpl.format(username=self.username, title=self.title, content=self.content, publish=self.publish)


