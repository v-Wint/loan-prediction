from django.urls import path
from .views import home, BorrowerCreateView, LoanApplicationCreateView, LoanApplicationDetailView, BorrowerDetailView

urlpatterns = [
    path('', home, name='home'),
    path('borrowers/new/', BorrowerCreateView.as_view(), name='borrower-create'),
    path('loans/new/', LoanApplicationCreateView.as_view(), name='loan-create'),
    path('loans/<int:pk>/', LoanApplicationDetailView.as_view(), name='loan-detail'),
    path('borrowers/<int:pk>/', BorrowerDetailView.as_view(), name='borrower-detail'),
]
