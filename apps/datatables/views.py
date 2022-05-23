from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from apps.datatables.forms import TransactionForm
from apps.home.models import Data
from apps.utils import set_pagination


class TransactionView(View):
    context = {"segment": "transactions"}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == "edit":
                edit_row = self.edit_row(pk)
                return JsonResponse({"edit_row": edit_row})
            elif pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({"edit_row": edit_row})

        if pk and action == "edit":
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect("transactions")

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse(
            {
                "valid": "success" if is_done else "warning",
                "message": message,
                "edit_row": edit_row,
            }
        )

    def delete(self, request, pk, action=None):
        transaction = self.get_object(pk)
        transaction.delete()

        redirect_url = None
        if action == "single":
            messages.success(request, "Item deleted successfully")
            redirect_url = reverse("transactions")

        response = {
            "valid": "success",
            "message": "Item deleted successfully",
            "redirect_url": redirect_url,
        }
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        filter_params = None
        transactions = Data.objects.filter(type="transaction")

        search = request.GET.get("search")
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = Q(name__icontains=key.strip())
                    else:
                        filter_params |= Q(name__icontains=key.strip())

        if filter_params:
            transactions = transactions.filter(filter_params)

        self.context["transactions"], self.context["info"] = set_pagination(
            request, transactions
        )
        if not self.context["transactions"]:
            return False, self.context["info"]

        return self.context, "transactions/list.html"

    def edit(self, request, pk):
        transaction = self.get_object(pk)

        self.context["transaction"] = transaction
        self.context["form"] = TransactionForm(instance=transaction)

        return self.context, "transactions/edit.html"

    """ Get Ajax pages """

    def edit_row(self, pk):
        transaction = self.get_object(pk)
        form = TransactionForm(instance=transaction)
        context = {"instance": transaction, "form": form}
        return render_to_string("transactions/edit_row.html", context)

    """ Common methods """

    def get_object(self, pk):
        transaction = get_object_or_404(Data, id=pk)
        return transaction

    def get_row_item(self, pk):
        transaction = self.get_object(pk)
        edit_row = render_to_string(
            "transactions/edit_row.html", {"instance": transaction}
        )
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        transaction = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = TransactionForm(form_data, instance=transaction)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, "Transaction saved successfully")

            return True, "Transaction saved successfully"

        if not is_urlencode:
            messages.warning(request, "Error Occurred. Please try again.")
        return False, "Error Occurred. Please try again."
