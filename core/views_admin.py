from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from xhtml2pdf import pisa
from io import BytesIO

from .models import Order


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from xhtml2pdf import pisa
from io import BytesIO

from .models import Order


@staff_member_required
def order_list(request):
    """
    Lista de pedidos recebidos no painel admin
    """

    orders = (
        Order.objects
        .select_related("user", "requisition")
        .prefetch_related("orderitem_set__product")
        .order_by("-created_at")
    )

    pending_orders = orders.filter(status="PENDENTE").count()

    context = {
        "orders": orders,
        "pending_orders": pending_orders,
    }

    return render(request, "admin/orders.html", context)


@staff_member_required
def generate_pdf(request, id):
    """
    Gera PDF do pedido
    """

    order = get_object_or_404(Order, id=id)

    html_string = render_to_string(
        "pdf/order.html",
        {"order": order}
    )

    result = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(html_string.encode("UTF-8")),
        result
    )

    if pdf.err:
        return HttpResponse("Erro ao gerar PDF", status=500)

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = f'attachment; filename="pedido_{order.id}.pdf"'

    return response


@staff_member_required
def generate_pdf(request, id):
    """
    Gera PDF do pedido
    """

    order = get_object_or_404(Order, id=id)

    html_string = render_to_string(
        "pdf/order.html",
        {"order": order}
    )

    result = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(html_string.encode("UTF-8")),
        result
    )

    if pdf.err:
        return HttpResponse("Erro ao gerar PDF", status=500)

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = f'attachment; filename="pedido_{order.id}.pdf"'

    return response