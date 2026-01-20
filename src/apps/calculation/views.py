from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django import forms
from apps.schedule.models import Teacher, Pair
import re


def interpret_pair_num(pair_num):
    """
    Convert pair number to time range
    """
    time_ranges = {
        1: "08:00-09:30",
        2: "09:40-11:10",
        3: "11:20-12:50",
        4: "13:20-14:50",
        5: "15:00-16:30",
        6: "16:40-18:10"
    }
    return time_ranges.get(pair_num, "Неизвестно")


def interpret_work_type(text):
    """
    Interpret work type from text
    """
    text_lower = text.lower()
    # Use only literal contents within parentheses per requirements
    parentheses_content = " ".join(re.findall(r"\(([^)]*)\)", text_lower))

    # Check for practice (п followed by digits)
    practice_match = re.search(r"[пП]\s*\d+", parentheses_content)
    if practice_match:
        return "Практика"

    # Check for lecture (л followed by digits)
    lecture_match = re.search(r"[лЛ]\s*\d+", parentheses_content)
    if lecture_match:
        return "Лекция"

    # Check for exam
    if "экзамен" in parentheses_content:
        return "Экзамен"

    # Check for credit
    if "зачет" in parentheses_content:
        return "Зачет"

    # Check for consultation
    if "консультация" in parentheses_content:
        return "Консультация"

    # Default to other if no specific type found
    return "Другое"


class PairSearchForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
        label='Дата начала'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
        label='Дата окончания'
    )
    teacher = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Начните вводить ФИО (можно оставить пустым)',
                'autocomplete': 'off',
            }
        ),
        required=False,
        label="Преподаватель"
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название предмета'}),
        required=False,
        label="Предмет"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher_options = list(
            Teacher.objects.order_by("name").values_list("name", flat=True)
        )

    def clean_teacher(self):
        teacher_name = self.cleaned_data["teacher"].strip()
        if not teacher_name:
            return None
        matches = Teacher.objects.filter(name__iexact=teacher_name)
        if not matches.exists():
            raise forms.ValidationError("Преподаватель не найден.")
        if matches.count() > 1:
            raise forms.ValidationError("Найдено несколько преподавателей, уточните ФИО.")
        return matches.first()


class PairSearchView(LoginRequiredMixin, FormView):
    template_name = 'calculation/pair_search.html'
    form_class = PairSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск занятий'
        context.setdefault('search_performed', False)
        context.setdefault('pairs', [])
        form = context.get("form")
        if form and hasattr(form, "teacher_options"):
            context["teacher_options"] = form.teacher_options
        return context

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        teacher = form.cleaned_data['teacher']
        subject = form.cleaned_data['subject'].strip()

        pairs = Pair.objects.filter(
            date__range=[start_date, end_date],
        ).select_related('insertion').prefetch_related('groups').distinct().order_by('date', 'num', 'id')
        if teacher:
            pairs = pairs.filter(teachers=teacher)
        if subject:
            pairs = pairs.filter(subject__icontains=subject)

        processed_pairs = []
        for pair in pairs:
            for group in pair.groups.all():
                group_name = group.name.strip() if group.name else ""
                course = group_name[0] if group_name else ""

                processed_pairs.append({
                    'date': pair.date,
                    'time_range': interpret_pair_num(pair.num),
                    'work_type': interpret_work_type(pair.text),
                    'course': course,
                    'group': group.name,
                    'hours': 2,  # Constant as specified
                    'notes': ""  # Empty as specified
                })

        context = self.get_context_data(
            form=form,
            pairs=processed_pairs,
            search_performed=True,
        )
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(
            form=form,
            search_performed=True,
            search_error="Исправьте ошибки в форме и повторите поиск.",
        )
        return self.render_to_response(context)
