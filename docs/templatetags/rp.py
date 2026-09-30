from django import template
register = template.Library()
S = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'sebelas']

def tb(n):
    if n < 12: return S[n]
    if n < 20: return tb(n - 10) + ' belas'
    if n < 100: return tb(n // 10) + ' puluh' + (' ' + tb(n % 10) if n % 10 else '')
    if n < 200: return 'seratus' + (' ' + tb(n - 100) if n > 100 else '')
    if n < 1000: return tb(n // 100) + ' ratus' + (' ' + tb(n % 100) if n % 100 else '')
    if n < 2000: return 'seribu' + (' ' + tb(n - 1000) if n > 1000 else '')
    for div, nm in ((10**9, 'miliar'), (10**6, 'juta'), (1000, 'ribu')):
        if n >= div:
            return tb(n // div) + ' ' + nm + (' ' + tb(n % div) if n % div else '')

@register.filter
def rp(v):
    return f'{int(v or 0):,}'.replace(',', '.')

@register.filter
def terbilang(v):
    n = int(v or 0)
    t = tb(n) if n else 'nol'
    return t[0].upper() + t[1:] + ' rupiah.'

HARI = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
BLN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

@register.filter
def tgl(d):
    return f'{HARI[d.weekday()]}, {d.day} {BLN[d.month - 1]} {d.year}'
