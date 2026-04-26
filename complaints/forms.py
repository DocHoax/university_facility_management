from django import forms

from complaints.models import Complaint, ComplaintComment


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["department", "category", "location", "description", "priority", "attachment"]


class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ["body"]
