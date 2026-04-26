from django import forms

from accounts.models import User
from complaints.models import Complaint, ComplaintComment


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["department", "category", "location", "description", "priority", "attachment"]


class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ["body"]


class ComplaintAssignmentForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.none())

    def __init__(self, *args, **kwargs):
        user_queryset = kwargs.pop("user_queryset", User.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = user_queryset


class ComplaintStatusUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=Complaint._meta.get_field("status").choices)
