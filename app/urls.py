from django.urls import path
from app.controllers.auth import LoginView, SignUpView
from app.controllers.expense import ExpenseView
from app.controllers.balance import BalanceView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

urlpatterns += [
    path("expense/list/", ExpenseView.as_view({"get": "list", "post": "create"})),
    path("expense/<int:id>/", ExpenseView.as_view({"get": "retrieve", "delete": "delete"})),
]

urlpatterns += [
    path("balance/", BalanceView.as_view({"get": "retrieve_by_user"})),
]
