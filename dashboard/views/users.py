from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from . import forms


def signup(request):
    """
    Register a new user, login the new user and redirect to
    breakdowns:index page
    """

    # Check if user already logged
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form_class = forms.SignupForm
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            job_title = form.cleaned_date.get('job_title')
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            user.full_name = full_name
            user.email = email
            user.job_title = job_title
            user.is_active = False
            user.save()
            messages.success(
                request,
                'You have successfully created a new account.'
            )
            messages.warning(
                request,
                ('Your account must be activated before you can start '
                 'using it. Please contact the admin to quickly activate '
                 'your account.')
            )
                
            return redirect('dashboard:index')
    else:
        form = form_class()
    return render(request, template_name, {
        'form': form,
    })
