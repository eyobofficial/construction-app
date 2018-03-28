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

        # Setup a Test Contractor
        models.Contractor.objects.create(
            full_name='Contractor full name',
            short_name='Contractor short name',
            description='Contractor description',
            is_active=True,
        )

    def create_project(self, *args, **kwargs):
        """
        Create a test project
        """
        construction_type = kwargs.get('construction_type', 'building')
        consultant = models.Consultant.objects.get(pk=1)
        contractor = models.Contractor.objects.get(pk=1)
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
            consultant=consultant,
            contractor=contractor,
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

    def create_project_status(self, project, status):
        return models.ProjectStatus.objects.create(
            project=project,
            status=status,
        )

    def test_get_last_status_for_project_with_no_status(self):
        project = self.create_project()
        self.assertEqual(project.get_last_status(), None)

    def test_get_last_status_for_project_with_status(self):
        # Create a default test project
        project = self.create_project()

        # Add status to the project
        project.project_status.create(
            status='active',
        )
        last_status = project.get_last_status()
        self.assertEqual(last_status.status, 'active')
