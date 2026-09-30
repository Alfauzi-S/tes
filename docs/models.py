from django.db import models

PFX = {'po': 'PO', 'nota': 'NP', 'invoice': 'INV'}
LABEL = {'po': 'Purchase Order', 'nota': 'Nota Pembelian', 'invoice': 'Invoice'}


class Document(models.Model):
    type = models.CharField(max_length=10, choices=LABEL.items())
    number = models.CharField(max_length=40, unique=True, editable=False)
    date = models.DateField('Tanggal')
    party = models.CharField('Nama', max_length=200)
    addr = models.TextField('Alamat', blank=True)
    phone = models.CharField('Telepon', max_length=50, blank=True)
    notes = models.TextField('Keterangan', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return self.number

    def save(self, *a, **k):
        if not self.number:
            n = Document.objects.filter(type=self.type, date=self.date).count() + 1
            while Document.objects.filter(number=(num := f'{PFX[self.type]}-SP-{self.date:%Y%m%d}-{n:03d}')).exists():
                n += 1
            self.number = num
        super().save(*a, **k)

    @property
    def total(self):
        return sum(i.total for i in self.items.all())


class Item(models.Model):
    doc = models.ForeignKey(Document, related_name='items', on_delete=models.CASCADE)
    name = models.CharField('Nama', max_length=200)
    qty = models.DecimalField('Jumlah', max_digits=12, decimal_places=3, default=0)
    unit = models.CharField('Satuan', max_length=20, blank=True)
    price = models.DecimalField('Harga / Nilai', max_digits=14, decimal_places=0, default=0)

    class Meta:
        ordering = ['id']

    @property
    def total(self):  # invoice: nilai langsung; lainnya: jumlah x harga
        return self.price if self.doc.type == 'invoice' else self.qty * self.price
