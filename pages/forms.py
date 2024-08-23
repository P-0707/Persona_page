from django import forms
from .models import ContactEntry

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactEntry
        fields = ['sender_name', 'sender_email', 'message_content']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name!',
                'class': 'form-control'
            }),
            'sender_email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address!',
                'class': 'form-control'
            }),
            'message_content': forms.Textarea(attrs={
                'placeholder': 'Your message please!',
                'rows': 7,
                'class': 'form-control'
            }),
        }
