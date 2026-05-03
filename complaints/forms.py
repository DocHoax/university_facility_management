from django import forms

from accounts.models import Department, User
from complaints.models import Complaint, ComplaintCategory, ComplaintComment


class ComplaintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.filter(is_active=True).order_by("name")
        self.fields["category"].queryset = ComplaintCategory.objects.filter(is_active=True).order_by("name")
        self.fields["department"].empty_label = "Select department"
        self.fields["category"].empty_label = "Select category"
        if user and getattr(user, "department_id", None):
            self.fields["department"].initial = user.department_id

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


class ComplaintTrackForm(forms.Form):
    ticket_id = forms.CharField(label="Ticket ID", max_length=20)


class ComplaintCategoryForm(forms.ModelForm):
    class Meta:
        model = ComplaintCategory
        fields = ["name", "description", "is_active"]
