from dashboard import models
from django.test import TestCase
from django.utils import timezone


from datetime import timedelta


class ProjectModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup a Test Consultant
        models.Consultant.objects.create(
            full_name='Test Consultant full name',
            short_name='test_consultant',
            description='Consultant description',
        )

    def create_project(self, *args, **kwargs):
        """
        Create a test project
        """
        construction_type = kwargs.get('construction_type', 'building')
        status = kwargs.get('status', 1)
        consultant = models.Consultant.objects.get(short_name='test_consultant')
        employer = kwargs.get('employer', 'Test Employer name')
        full_name = kwargs.get('full_name', 'Project official full name')
        short_name = kwargs.get('short_name', 'Project short name')
        project_code = kwargs.get('project_code')
        description = kwargs.get('description')
        signing_date = kwargs.get('signing_date')
        site_handover = kwargs.get('site_handover')
        commencement_date = kwargs.get('commencement_date')
        period = kwargs.get('period')

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
            period=period
        )
        return project

    def test_get_original_completion_date_with_no_commencement_date_and_no_period(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with no
        commencement_date and no period
        """
        project = self.create_project()
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_commencement_date_and_no_period(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with a
        commencement_date but no period
        """
        commencement_date = timezone.now()
        project = self.create_project(commencement_date=commencement_date)
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_period_and_no_commencement_date(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with a period
        but not a commencement_date but
        """
        period = 100
        project = self.create_project(period=period)
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_period_and_commencement_date(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with both
        commencement_date and period
        """
        commencement_date = timezone.localdate()
        period = 100
        project = self.create_project(
            commencement_date=commencement_date,
            period=period
        )
        completion_date = commencement_date + timedelta(days=period)
        self.assertEqual(
            project.get_original_completion_date(),
            completion_date
        )
