from django.db.models import (Model, DateTimeField, ForeignKey, CASCADE, IntegerField, TextField)
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext as _

REASON_CHOICES = (
        (1, _('Spam')),
        # (2, 'محتوای خشن'),
        (3, _('Sexual content')),
        # (4, 'آزار یا زورگویی'),
        (5, _('Harmful or dangerous acts')),
        (6, _('Child abuse')),
        (7, _('Promotes terrorism')),
        # (8, 'محتوای نفرت پراکنی یا توهین آمیز'),
        # (9, 'حقوق من را نقض می کند'),
        # (10, 'مشکل زیرنویس ها'),
        # (11, 'حیوان آزاری'),
        # (12, 'کلاهبرداری یا فریب'),
        (13, _('False information')),
        # (14, "سازمان‌های خطرناک یا خشونت‌بار"),
        (15, _('Infringement of Intellectual Property')),
        # (16, "فروش کالاهای تحت نظارت یا غیر مجاز"),
        # (17, "خودکشی یا آسیب به خود"),
        (18, _('Insulting ethnicities or racism')),
        # (19, "محتوای نامناسب برای کودکان"),
        (20, _('Contrast the title and description with the content of the video.')),
        # (21, "استفاده تبلیغاتی غیرمجاز"),
        (22, _('Other')),
    )


class Report(Model):
    user = ForeignKey(to=User, on_delete=CASCADE)
    video = ForeignKey(to='Video', on_delete=CASCADE, related_name='reports')
    acted_at = DateTimeField(auto_now_add=True)

    RESULT_CHOICES = (
        (1, 'accepted'),
        (2, 'rejected'),
        (3, 'waiting'),
    )
    reason = IntegerField(choices=REASON_CHOICES)
    description = TextField(blank=True)
    result = IntegerField(choices=RESULT_CHOICES, default=3, blank=True, null=True)


class ReportForm(ModelForm):
    reason = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': ''}), choices=REASON_CHOICES, )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _('More explanation'), "rows": 5, "class": "ml-2 form-control"}
        ),
    )

    class Meta:
        model = Report
        fields = ['reason', 'description']
