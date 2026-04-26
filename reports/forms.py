from django import forms


class ReportFilterForm(forms.Form):
    ticket_id = forms.CharField(required=False)
    status = forms.CharField(required=False)
    category = forms.CharField(required=False)
    department = forms.CharField(required=False)
    priority = forms.CharField(required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
