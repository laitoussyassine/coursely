from django import forms
from .models import Subscriber
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
