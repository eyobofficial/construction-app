from django import forms
from form_utils.forms import BetterModelForm
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from . import models

from dashboard import models


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    full_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    job_title = forms.CharField(max_length=100)

    class Meta:
        model = models.CustomUser
        fields = ('username', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class ProjectForm(BetterModelForm):
    class Meta:
        model = models.Project
        fields = (
            'construction_type',
            'employer',
            'consultant',
            'full_name',
            'short_name',
            'description',
            'contract_amount',
            'signing_date',
            'site_handover',
            'commencement_date',
            'period',
            'status',
            'is_published',
        )
        fieldsets = [
            ('project_details', {
                'legend': 'PROJECT DETAILS',
                'fields': [
                    'construction_type', 'employer', 'consultant',
                    'full_name', 'short_name', 'description',
                ],
            }),
            ('contractual_details', {
                'legend': 'CONTRACTUAL DETAILS',
                'fields': [
                    'contract_amount', 'signing_date', 'site_handover',
                    'commencement_date', 'period',
                ],
            }),
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Project Summary',
                'construction_type',
                'status',
                'employer',
                'consultant',
                'full_name',
                'short_name',
                'description',
            ),
            Fieldset(
                'Contract Summary',
                'contract_amount',
                'signing_date',
                'site_handover',
                'commencement_date',
                'period',
            ),
        )
        super(ProjectForm, self).__init__(*args, **kwargs)
