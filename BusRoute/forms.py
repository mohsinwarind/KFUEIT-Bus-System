from django import forms
from .models import BusRoute,MissingComplaint,BusDriver,DriverReview

class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ['name']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MissingComplaintForm(forms.ModelForm):
    class Meta:
        model = MissingComplaint
        fields = ['item_name','description','location','date_lost','image','contact_email','contact_phone']
        widget = {
            'date_lost':forms.DateInput(attrs={'type':'date'})
        }



class DriverReviewForm(forms.ModelForm):
    class Meta:
        model = DriverReview
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3}),
        }