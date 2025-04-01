from django.shortcuts import render, redirect
from .models import Project
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactMessage
from django.conf import settings

def home(request):
    projects = Project.objects.all()
    return render(request, 'main/home.html', {'projects': projects})

def about(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect("contact")

        try:
            ContactMessage.objects.create(name=name, email=email, message=message)

            admin_subject = f"New Portfolio Contact from {name}"
            admin_body = (
                f"Hello Vishal,\n\n"
                f"You have received a new message from your portfolio contact form:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Message:\n{message}\n\n"
                "Please respond as needed."
            )

            send_mail(
                admin_subject, 
                admin_body, 
                settings.EMAIL_HOST_USER, 
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )

            messages.success(request, "Thank you for reaching out! I will get back to you soon.")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

        return redirect("contact")

    return render(request, "main/contact.html")