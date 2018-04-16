from dashboard import models
from django.test import TestCase
from django.utils import timezone


from datetime import timedelta


def create_consultant(*args, **kwargs):
    """
    Returns a test Consultant object
    """
    full_name = kwargs.get('full_name', 'Test Consultant full name')
    short_name = kwargs.get('short_name', 'Test Consultant')
    description = kwargs.get('description')

    consultant = models.Consultant.objects.create(
        full_name=full_name,
        short_name=short_name,
        description=description
    )
    return consultant


def create_notification(Project, triggered_by, notify_to, *args, **kwargs):
    """
    Returns a test Notification object
    """
    title = kwargs.get('title', 'test notification title')
    # body = kwargs.get('')


def create_project(*args, **kwargs):
    """
    Returns a test Project object
    """
    construction_type = kwargs.get('construction_type', 'building')
    status = kwargs.get('status', 1)
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


def create_user(username, *args, **kwargs):
    """
    Returns a test CustomUser object
    """
    email = 'test@user.com'
    password = 'TestPassword1234'

    user = models.CustomUser.objects.create_user(
        username,
        email,
        password
    )

    user.is_active = kwargs.get('is_active', True)
    user.avatar = kwargs.get('avatar')
    user.full_name = kwargs.get('full_name', 'Test User')
    user.job_title = kwargs.get('job_title', 'Job Title')
    user.bio = kwargs.get('bio')
    user.project_followed = kwargs.get('project_followed')
    user.project_administered = kwargs.get('project_administered')
    user.is_project_admin = kwargs.get('is_project_admin', False)
    user.save()


def create_notification(project, triggered_by, **kwargs):
    """
    Returns a test Notification object
    """
    notification_type = kwargs.get('notification_type', 'alert')
    title = kwargs.get('title', 'Test notification title')
    body = kwargs.get('body', 'Test notification body text')
    is_broadcast = kwargs.get('is_broadcast', False)

    notification = models.Notification.objects.create(
        notification_type=notification_type,
        project=project,
        triggered_by=triggered_by,
        title=title, body=body,
        is_broadcast=is_broadcast,
    )
    return notification


class ProjectModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup a Test Consultant
        create_consultant()

    def test_get_original_completion_date_with_no_commencement_date_and_no_period(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with no
        commencement_date and no period
        """
        project = create_project()
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_commencement_date_and_no_period(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with a
        commencement_date but no period
        """
        commencement_date = timezone.now()
        project = create_project(commencement_date=commencement_date)
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_period_and_no_commencement_date(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with a period
        but not a commencement_date but
        """
        period = 100
        project = create_project(period=period)
        self.assertIs(project.get_original_completion_date(), None)

    def test_get_original_completion_date_with_period_and_commencement_date(self, *args, **kwargs):
        """
        Test Project.get_original_completion_date() method with both
        commencement_date and period
        """
        commencement_date = timezone.localdate()
        period = 100
        project = create_project(
            commencement_date=commencement_date,
            period=period
        )
        completion_date = commencement_date + timedelta(days=period)
        self.assertEqual(
            project.get_original_completion_date(),
            completion_date
        )


class NotificationModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create A Test Data
        create_consultant()
        test_project = create_project()
        create_user('trigger')
        receiver1 = create_user('receiver1', email='receiver1@email.com')
        receiver2 = create_user('receiver2', email='receiver1@email.com')
        test_project.project_followers.add(receiver1, receiver2)
        test_project.save()

    def test_creating_notification(self, *args, **kwargs):
        project = models.Project.objects.get(pk=1)
        triggered_by = models.CustomUser.objects.get(username='trigger')

        notification = create_notification(project, triggered_by)
        self.assertIs(notification.triggered_by, triggered_by)
        self.assertEqual(len(notification.user_notifications.all()), 2)

