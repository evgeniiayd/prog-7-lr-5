from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    choices = forms.CharField(
        widget=forms.Textarea,
        help_text="Введите варианты ответа, каждый с новой строки"
    )

    class Meta:
        model = Question
        fields = ['question_text']

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            # Создаём варианты ответов
            choices_text = self.cleaned_data['choices']
            for line in choices_text.splitlines():
                if line.strip():
                    Choice.objects.create(question=question, choice_text=line.strip())
        return question
