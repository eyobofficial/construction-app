from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from dashboard import models


class ProjectForm(forms.ModelForm):
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
        )

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
