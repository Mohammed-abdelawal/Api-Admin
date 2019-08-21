from django.contrib import admin
from .models import Article, Category, Comment, Profile, User
from django.contrib.auth.admin import UserAdmin
from image_cropping import ImageCroppingMixin

# Register your models here.


class CommentInline(admin.TabularInline):
    readonly_fields = ['time']
    ordering = ['time']
    model = Comment
    extra = 1


def approve(modeladmin, request, queryset):
    queryset.update(
        approved = True
    )

@admin.register(Article)
class ArticleAdmin(ImageCroppingMixin, admin.ModelAdmin): 
    actions = [approve]
    date_hierarchy = 'pub_date'
    model = Article
    inlines = [CommentInline]
    list_display = ['id','user','title','pub_date','approved','comments_num']
    ordering = ['pub_date']
    list_filter = ['user','category','pub_date']
    search_fields = ['title','user__username']
    filter_horizontal = ['category']
    exclude = []
    prepopulated_fields = {'slug':('title',)}
    fieldsets = (
        (None,
        {
            'classes': ('extrapretty',) ,
            'fields':(
            ('user','pub_date','approved'),
            ('title','slug'),
            ('pic','cropping'),
            'category',
            'article' )
    }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        list_ro = ['pub_date']
        if obj :
            list_ro += ['user','approved'] if obj.approved else ['user']
        else :
            list_ro += ['cropping']
        return list_ro

@admin.register(Category)
class CategoryAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = Category
    search_fields = ['title']
    list_display = ['id', 'title', 'articles_num']
    save_as = True






# custom user to add profile model

def not_staff(modeladmin, request, queryset):
    if request.user.is_superuser :
        queryset.update(
            is_staff = False
        )
not_staff.short_description = 'desactive staff'

class ProfileInline(ImageCroppingMixin,admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
    fk_name = 'user'
    radio_fields = {'is_male':admin.HORIZONTAL}



class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]
    UserAdmin.actions += [not_staff]
    
    #UserAdmin.list_display += ('username',) 

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)