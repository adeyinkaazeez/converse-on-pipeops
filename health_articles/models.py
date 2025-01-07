from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from taggit.managers import TaggableManager
from prose.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex


# Create your models here.
class PublishedManager(models.Manager):    
    def get_queryset(self):        
        return super().get_queryset().filter(status=Healths.Status.PUBLISHED) #status field must be set to PUBLISHED too
    
class DraftManager(models.Manager):    
    def get_queryset(self):        
        return super().get_queryset().filter(status=Healths.Status.DRAFT)
    

class Healths(models.Model): 
    User = get_user_model()
    
    class Status(models.TextChoices):    #the status we have choices we can select from among Draft, Published, Pending. That is what TextChoices does like Drop down list box in html 
        DRAFT = 'DF', 'Draft'    
        PUBLISHED = 'PB', 'Published'
        PENDING= 'PD', 'Pending'

    tags = TaggableManager()
    
    title = models.CharField(max_length=250) 
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    #author field is saying that only registered and acceptable users can authored or write post and not anonymous person and the  a author can write as many post as possible and also delete his or her post 
    #Which author write(s) so so post(s)
    #If an author is deleted by admin maybe because of infractions, all the posts made by such User(author) will also be deleted(CASCADE)
    #unique_for_date will ensure no duplicate post with same slug in a particular day
    author = models.ForeignKey(User,                             
                                 on_delete=models.CASCADE,                   
                                related_name='health_posts' )
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now)  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    #status field define our status choices by making the three  choices(draft, published, pending) available then making published as default by utilizing our Status child class
    status = models.CharField(max_length=2,                     
                                choices=Status.choices,                     
                                default=Status.DRAFT)
   
    news_image = models.ImageField(default=' ',
                             upload_to='photo-news')
    news_image_two = models.ImageField(default=' ',
                             upload_to='photo-news')
    news_image_three = models.ImageField(default=' ',
                             upload_to='photo-news')
    news_image_four = models.ImageField(default=' ',
                             upload_to='photo-news')
    
    caption = models.CharField( default=' ' ) 
    caption_two = models.CharField( default=' ' ) 
    caption_three = models.CharField( default=' ' ) 
    caption_four = models.CharField( default=' ' ) 
    likes = models.ManyToManyField(User, related_name='liked_health_post', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', 
                                        related_query_name='hit_count_generic_relation') 
    section_name = models.CharField(max_length=50, default='Health Articles', editable=False)
    generatedField = models.GeneratedField(
        expression = SearchVector("title", config="english") + SearchVector("body", config="english"),
        output_field=SearchVectorField(),
        db_persist=True,
    )  

    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.  
    draft = DraftManager() 
    
 
 

    class Meta:  
        ordering = ['-publish'] #Last(newest) published to be at the top.
        indexes = [        
                models.Index(fields=['-publish']),  
                models.Index(fields=['-total_likes']),  
                GinIndex(fields=["generatedField"]),     
                      ]
        
   
     
    def __str__(self):       
         return self.title
    
    def get_absolute_url(self):
        return reverse('health_articles:post_detail',
                       args=[self.publish.year,                             
                              self.publish.month,                             
                              self.publish.day,                             
                              self.slug])
    
    def get_comments(self):
        return self.health_comments.filter(health_parent=None).filter(active=True)
    
class Healths_Comment(models.Model):
    User = get_user_model()     
    post = models.ForeignKey(Healths,                            
                             on_delete=models.CASCADE,                             
                             related_name='health_comments') 
    
    name = models.ForeignKey(User,  on_delete=models.CASCADE,            
                                related_name='healthuser_comments' ) 
    email = models.EmailField()    
    body = RichTextField()
    comment_image_one  = models.ImageField(default=' ',
                             upload_to='comment-photos')
    comment_image_two = models.ImageField(default=' ',
                             upload_to='comment-photos')
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)    
    active = models.BooleanField(default=True)
    health_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="health_replies", null=True)
    edited = models.BooleanField(default=False)
    edited_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_health_comment', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_health_comment', blank=True)
    section_name = models.CharField(max_length=50, default='Health Article Comment', editable=False)
    class Meta:        
        ordering = ['created']        
        indexes = [            
            models.Index(fields=['created']),       
              ]
    def __str__(self):        
        return f'Comment by {self.name} on {self.post}'
    
    def get_comments(self):
        return Healths_Comment.objects.filter(health_parent=self).filter(active=True)




