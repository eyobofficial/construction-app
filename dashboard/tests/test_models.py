from dashboard import models
from django.test import TestCase


class ProjectModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup a Test Consultant
        models.Consultant.objects.create(
            full_name='Test Consultant full name',
            short_name='Test Consultant short name',
            description='Consultant description',
        )

    def create_project(self, *args, **kwargs):
        """
        Create a test project
        """
        construction_type = kwargs.get('construction_type', 'building')
        status = kwargs.get('status', 'unknown'),
        consultant = models.Consultant.objects.get(pk=1)
        employer = kwargs.get('employer', 'Test Employer name')
        full_name = kwargs.get('full_name', 'Project official full name')
        short_name = kwargs.get('short_name', 'Project short name')
        project_code = kwargs.get('project_code')
        description = kwargs.get('description')
        signing_date = kwargs.get('signing_date')
        site_handover = kwargs.get('site_handover')
        commencement_date = kwargs.get('commencement_date')
        period = kwargs.get('period')
        completion_date = kwargs.get('completion_date')
        is_published = kwargs.get('is_published', False)

        project = models.Project.objects.create(
            construction_type=construction_type,
            status=status,
            consultant=consultant,
            employer=employer,
            full_name=full_name,
            short_name=short_name,
            project_code=project_code,
            description=description,
            signing_date=signing_date,
            site_handover=site_handover,
            commencement_date=commencement_date,
            period=period,
            completion_date=completion_date,
            is_published=is_published,
        )
        return project
