import requests
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.shortcuts import render
from .models import Borrower, LoanApplication
from .forms import BorrowerForm, LoanApplicationForm

def home(request):
    return render(request, 'app/home.html', {
        'borrowers': Borrower.objects.all(),
        'loans': LoanApplication.objects.select_related('borrower').all(),
    })

class BorrowerCreateView(CreateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = 'app/borrower_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next', '/')
        return f"{next_url}?borrower={self.object.pk}"


class LoanApplicationCreateView(CreateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'app/loan_form.html'

    def get_initial(self):
        initial = super().get_initial()
        borrower_pk = self.request.GET.get('borrower')
        if borrower_pk:
            initial['borrower'] = borrower_pk
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        loan = self.object
        self._run_prediction(loan)
        return response

    def _run_prediction(self, loan):
        try:
            payload = loan.to_loan_input().model_dump_json()
            result = requests.post(
                f"{settings.PREDICTION_SERVICE_URL}/predict",
                data=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            data = result.json()
            loan.decision = 'fund' if data['decision'] else 'skip'
            loan.confidence = data['confidence']
            loan.save()
        except Exception as e:
            print(e)
            pass

    def get_success_url(self):
        return reverse('loan-detail', kwargs={'pk': self.object.pk})


class LoanApplicationDetailView(DetailView):
    model = LoanApplication
    template_name = 'app/loan_detail.html'
    context_object_name = 'loan'

class BorrowerDetailView(DetailView):
    model = Borrower
    template_name = 'app/borrower_detail.html'
    context_object_name = 'borrower'
