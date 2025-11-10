from django import forms

from .models import Testimonial, ContactMessage


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "role", "organization", "focus_area", "rating", "quote"]
        labels = {
            "name": "Nama lengkap",
            "role": "Peran atau jabatan",
            "organization": "Organisasi",
            "focus_area": "Fokus kolaborasi",
            "rating": "Rating",
            "quote": "Testimoni",
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        labels = {
            "name": "Name",
            "email": "Email",
            "message": "Message",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "class": "input-control",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "class": "input-control",
                "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Let's talk about your business challenge...",
                "rows": 4,
                "class": "input-control",
            }),
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Full name",
                "class": "input-control"
            }),
            "role": forms.TextInput(attrs={
                "placeholder": "Role or title",
                "class": "input-control"
            }),
            "organization": forms.TextInput(attrs={
                "placeholder": "Organization (optional)",
                "class": "input-control"
            }),
            "focus_area": forms.TextInput(attrs={
                "placeholder": "Focus area e.g., Leadership",
                "class": "input-control"
            }),
            "rating": forms.Select(
                choices=[(5, "★★★★★"), (4, "★★★★☆"), (3, "★★★☆☆"), (2, "★★☆☆☆"), (1, "★☆☆☆☆")],
                attrs={"class": "input-control"}
            ),
            "quote": forms.Textarea(attrs={
                "placeholder": "Share your experience working with Celine…",
                "rows": 4,
                "class": "input-control",
            }),
        }
