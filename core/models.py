from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('Baru', 'Baru'),
        ('Dibaca', 'Dibaca'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Baru')

    def __str__(self):
        return f"{self.subject} - {self.name}"
