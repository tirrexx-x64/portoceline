from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Experience, Achievement, Profile, Testimonial
from .forms import TestimonialForm, ContactForm


def home(request):
    experiences = Experience.objects.all().order_by('-start_date')
    achievements = Achievement.objects.all().order_by('-date')
    licenses = achievements.filter(category='license')
    competitions = achievements.filter(category='competition')
    profile = Profile.objects.first()
    testimonials = Testimonial.objects.all()
    testimonial_form = TestimonialForm()
    contact_form = ContactForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "testimonial":
            testimonial_form = TestimonialForm(request.POST)
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(
                    request,
                    "Terima kasih! Testimoni kamu sudah tersimpan.",
                    extra_tags="testimonial",
                )
                return redirect(f"{request.path}#testimonials")
            else:
                messages.error(
                    request,
                    "Mohon periksa kembali isian testimoni kamu.",
                    extra_tags="testimonial",
                )

        elif form_type == "contact":
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                message_obj = contact_form.save()
                notify_email = getattr(settings, "CONTACT_NOTIFY_EMAIL", None)
                if notify_email:
                    email_body = (
                        "Ada pesan kolaborasi baru dari portfolio site.\n\n"
                        f"Nama : {message_obj.name}\n"
                        f"Email: {message_obj.email}\n"
                        f"Dikirim: {message_obj.created_at:%Y-%m-%d %H:%M:%S %Z}\n\n"
                        f"Pesan:\n{message_obj.message}"
                    )
                    email_msg = EmailMessage(
                        subject=f"Portfolio Inquiry from {message_obj.name}",
                        body=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[notify_email],
                        reply_to=[message_obj.email],
                    )
                    try:
                        email_msg.send(fail_silently=False)
                    except Exception:
                        messages.warning(
                            request,
                            "Pesan tersimpan, tetapi terjadi kendala saat mengirim email notifikasi.",
                            extra_tags="contact",
                        )
                    else:
                        messages.success(
                            request,
                            "Terima kasih! Pesan kamu sudah terkirim ke Celine.",
                            extra_tags="contact",
                        )
                else:
                    messages.success(
                        request,
                        "Terima kasih! Pesan kamu sudah tersimpan.",
                        extra_tags="contact",
                    )
                return redirect(f"{request.path}#contact")
            else:
                messages.error(
                    request,
                    "Mohon lengkapi form kontak sebelum mengirim.",
                    extra_tags="contact",
                )

    context = {
        'experiences': experiences,
        'achievements': achievements,
        'licenses': licenses,
        'competitions': competitions,
        'profile': profile,
        'testimonials': testimonials,
        'testimonial_form': testimonial_form,
        'contact_form': contact_form,
    }
    return render(request, "main/index.html", context)
