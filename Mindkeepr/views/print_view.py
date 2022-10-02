
from Mindkeepr.models import  Element
from Mindkeepr.models.models import PrintList

import csv

from Mindkeepr.printer import Printer
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def barcode(request, pk):
    p = Printer()
    element = get_object_or_404(Element, pk=pk)
    p.add_element_to_print_list(element)
    pl = p.render_print_list()
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep


@login_required(login_url='/accounts/login')
def print_print_list(request):
    p = Printer()

    print_list, created = PrintList.objects.get_or_create(user=request.user)
    for print_elt in print_list.printelements.all():
        p.add_element_to_print_list(print_elt.element, print_elt.quantity)
    # return HttpResponse(, content_type='application/octet-stream')
    # print(p.print_print_list())
    pl = p.render_print_list()
    # print(pl)
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep


@login_required(login_url='/accounts/login')
def add_to_print_list(request, pk, qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list, created = PrintList.objects.get_or_create(user=request.user)
    print_list.add_to_list(elt, max(0, min(qty, 100)))
    print_list.save()
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})


@login_required(login_url='/accounts/login')
def remove_from_print_list(request, pk, qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list, created = PrintList.objects.get_or_create(user=request.user)
    print_list.remove_from_list(elt, qty)
    print_list.save()
    # todo
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})


@login_required(login_url='/accounts/login')
def print_list_disp(request):
    # Temp fix
    response = HttpResponse(
        content_type='text/csv',
      #  headers={'Content-Disposition': 'attachment; filename="export.csv"'},
    )
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    writer = csv.writer(response)
    for obj in Element.objects.all():
        row = []
        for field in ["id","name", "format_book","platform","__class__"]:
            try:
                row.append(str(getattr(obj, field)))
            except AttributeError:
                row.append("")
        writer.writerow(row)
    #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    #writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response
    #print_list, created = PrintList.objects.get_or_create(user=request.user)
    # todo
    #return render(request, "printlist.html", {"print_list": print_list.printelements.all()})

