from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Student(models.Model):
    OPTION_SELECT = 'Please select an option'
    MIDDLE_ONE = 'Middle 1'
    MIDDLE_TWO = 'Middle 2'
    MIDDLE_THREE = 'Middle 3'

    SENIOR_ONE = 'Senior 1'
    SENIOR_TWO = 'Senior 2'
    SENIOR_THREE = 'Senior 3'

    STUDENT_GRADE = [
        (OPTION_SELECT, 'Please select an option'),
        (MIDDLE_ONE, 'Middle 1'),
        (MIDDLE_TWO, 'Middle 2'),
        (MIDDLE_THREE, 'Middle 3'),
        (SENIOR_ONE, 'Senior 1'),
        (SENIOR_TWO, 'Senior 2'),
        (SENIOR_THREE, 'Senior 3'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    score = models.PositiveIntegerField()
    grade = models.CharField(max_length=50, choices=STUDENT_GRADE, default=OPTION_SELECT)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'


class FriendRequest(models.Model):
    from_student = models.ForeignKey(
        Student, related_name='sent_requests', on_delete=models.CASCADE)
    to_student = models.ForeignKey(
        Student, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_student', 'to_student')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    description = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.caption}, likes ({self.likes})'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    @property
    def likes(self):
        return self.liked_by.count()

class StudyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_groups')
    topic = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

class StudyGroupInvite(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='invites')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studygroup_invites')
    accepted = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)