from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Certification, Project
from .forms import ContactForm
from django.http import Http404
from django.template import TemplateDoesNotExist

# View for the home page
def home(request):
    return render(request, 'core/home.html')

# View for the portfolio page
def projects(request):
    projects = Project.objects.all()  # Get all projects
    return render(request, 'core/projects.html', {'projects': projects})

# View for a single project's detail page
def project_detail(request, id):
    template_name = f'core/proj/project_{id}.html'
    try:
        return render(request, template_name, {'id': id})
    except TemplateDoesNotExist:
        raise Http404("Project not found")


# View for a single certification's detail page
def certification_detail(request, cert_id):
    # Format the template path for dynamic certification details
    template_name = f'core/cert/certification_{cert_id}.html'
    try:
        return render(request, template_name, {'cert_id': cert_id})
    except TemplateDoesNotExist:
        raise Http404("Certification not found")

# View for the contact page
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the ContactEntry model instance
            messages.success(request, 'Thank you for reaching out. I have received your message and will be in touch shortly.')
            return redirect('pages:contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
