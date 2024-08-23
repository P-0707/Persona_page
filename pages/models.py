from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Model for representing the user's skills.
class Skill(models.Model):
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    name = models.CharField(max_length=40)
    proficiency = models.CharField(max_length=12, choices=PROFICIENCY_LEVELS, default='beginner')
    icon = models.FileField(blank=True, null=True, upload_to="skills")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # You can now add skills directly via code using Skill.objects.create(name='...', proficiency='...', etc.)

# Model for storing the user's profile information.
class UserProfile(models.Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='avatar')
    job_title = models.CharField(max_length=200, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(blank=True, null=True, upload_to='cv')

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else f'{self.user.username}'

    # You can create a UserProfile via code like this:
    # UserProfile.objects.create(user=user_instance, first_name='...', last_name='...', etc.)

# Model for storing contact form submissions from the website.
class ContactEntry(models.Model):
    class Meta:
        verbose_name = 'Contact Entry'
        verbose_name_plural = 'Contact Entries'
        ordering = ["-submitted_at"]

    submitted_at = models.DateTimeField(auto_now_add=True)
    sender_name = models.CharField(verbose_name="Name", max_length=100)
    sender_email = models.EmailField(verbose_name="Email")
    message_content = models.TextField(verbose_name="Message")

    def __str__(self):
        return f'{self.sender_name} ({self.sender_email})'

    # You can create a ContactEntry via code like this:
    # ContactEntry.objects.create(sender_name='...', sender_email='...', message_content='...')

# Model for showcasing the user's projects or portfolio items.
class Project(models.Model):
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ["-published_date"]

    published_date = models.DateTimeField(blank=True, null=True)
    project_name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    detailed_description = RichTextField(blank=True, null=True)
    cover_image = models.ImageField(blank=True, null=True, upload_to="portfolio")
    slug = models.SlugField(null=True, blank=True)
    is_displayed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return f"/portfolio/{self.slug}"

    # You can create a Project via code like this:
    # Project.objects.create(project_name='...', short_description='...', etc.)

# Model for storing certifications or awards.
class Certification(models.Model):
    class Meta:
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        ordering = ["-awarded_date"]

    awarded_date = models.DateTimeField(blank=True, null=True)
    issuing_organization = models.CharField(max_length=50)
    certification_title = models.CharField(max_length=200, blank=True, null=True)
    certification_description = RichTextField(blank=True, null=True)
    certification_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.certification_title or "No Title"

    # You can create a Certification via code like this:
    # Certification.objects.create(issuing_organization='...', certification_title='...', etc.)
