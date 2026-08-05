from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Job, Application
from .forms import Jobform

class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'all_jobs'

class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['already_applied'] = Application.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()
        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = Jobform
    template_name = 'job_form.html'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('job-detail', kwargs={'pk': self.object.pk})

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = Jobform
    template_name = 'job_form.html'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

    def get_success_url(self):
        return reverse('job-detail', kwargs={'pk': self.object.pk})

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('my-jobs')

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class MyJobsListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'my_jobs_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    application, created = Application.objects.get_or_create(
        job=job, applicant=request.user
    )
    if created:
        messages.success(request, f'You applied to "{job.title}".')
    else:
        messages.info(request, 'You have already applied to this job.')
    return redirect('job-detail', pk=job.pk)

class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'my_applications_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')
