from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Document, Item, LABEL

class DocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['date', 'party', 'phone', 'addr', 'notes']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
                   'addr': forms.Textarea(attrs={'rows': 2}), 'notes': forms.Textarea(attrs={'rows': 2})}

Items = forms.inlineformset_factory(Document, Item, fields=('name', 'qty', 'unit', 'price'), extra=6, can_delete=True)

@login_required
def home(request):
    return redirect('list', 'po')

@login_required
def listing(request, type):
    if type not in LABEL:
        raise Http404
    return render(request, 'docs/list.html', {'type': type, 'label': LABEL[type], 'labels': LABEL,
                                              'docs': Document.objects.filter(type=type).prefetch_related('items')})

@login_required
def edit(request, type=None, pk=None):
    doc = get_object_or_404(Document, pk=pk) if pk else None
    type = doc.type if doc else type
    if type not in LABEL:
        raise Http404
    inst = doc or Document(type=type)
    if request.method == 'POST':
        form, fs = DocForm(request.POST, instance=inst), Items(request.POST, instance=inst)
        if form.is_valid() and fs.is_valid():
            obj = form.save(commit=False)
            obj.type = type
            obj.save()
            fs.instance = obj
            fs.save()
            return redirect('cetak', obj.pk)
    else:
        initial = {}
        if not doc:  # isi otomatis dari dokumen terakhir
            last = Document.objects.filter(type=type).first()
            initial = {'date': timezone.localdate(), **({'party': last.party, 'addr': last.addr, 'phone': last.phone} if last else {})}
        form, fs = DocForm(instance=inst, initial=initial), Items(instance=inst)
    return render(request, 'docs/form.html', {'form': form, 'fs': fs, 'type': type, 'label': LABEL[type], 'doc': doc})

@login_required
def cetak(request, pk):
    d = get_object_or_404(Document, pk=pk)
    return render(request, 'docs/print.html', {'d': d, 'toko': settings.TOKO, 'label': LABEL[d.type].upper(), 'items': d.items.all()})

@login_required
@require_POST
def hapus(request, pk):
    d = get_object_or_404(Document, pk=pk)
    t = d.type
    d.delete()
    return redirect('list', t)
