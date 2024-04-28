from django.db import models
# from users.models import Admin
#from category.models import Category
#categories of products
class Category(models.Model):
  name=models.CharField(max_length=255)
  #itemCount=models.IntegerField(blank=True, null=True)
  description=models.TextField(max_length=255, blank=True, null=True)
  image = models.ImageField(upload_to='category/images', default='static/images/notfound.png')
  # image = models.ImageField(upload_to='category/images/',null=True)
  # imageUrl = models.URLField(null=True)

  #parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
  # admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,default=1)

  def __str__(self):
    return self.name
  

class SubCategory(models.Model):
    name=models.CharField(max_length=200)
    parentCategory=models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE,related_name='chiled' )
    def __str__(self):
        return self.name
