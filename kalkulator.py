import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
 
def sin_a(x):
    return math.sin(math.radians(x))

def cos_a(x):
    return math.cos(math.radians(x))

def tan_a(x):
    if x % 180 == 90:
        raise ValueError('Nilai Tan kelipatan 90 memiliki nilai tak terdefinisi')
    return math.tan(math.radians(x))

def asin_a(x):
    return math.degrees(math.asin(x))

def acos_a(x):
    return math.degrees(math.acos(x))

def atan_a(x):
    return math.degrees(math.atan(x))

fungsi = {
        'sin' : sin_a,
        'cos' : cos_a,
        'tan' : tan_a,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'pi': math.pi,
        'asin': asin_a,
        'acos': acos_a,
        'atan': atan_a,
        'faktorial': math.factorial,
        'pi': math.pi,
        'e': math.e,

    }

def siap_rumus(rumus):
    rumus_siap = rumus.replace('^', '**')
    rumus_siap = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', rumus_siap)
    rumus_siap = re.sub(r'(\))(\()', r'\1*\2', rumus_siap)
    return rumus_siap

def hitung_y(rumus, daftar_x):
    rumus_siap = siap_rumus(rumus)
    hasil_y = []
    for nilai_x in daftar_x:
        lokal = fungsi.copy()
        lokal['x'] = float(nilai_x)
        try:
            y = eval(rumus_siap, {"__builtins__": None}, lokal)
            hasil_y.append(np.nan if abs(y) > 1e6 else y)
        except (ValueError, ZeroDivisionError):
            hasil_y.append(np.nan)
    return np.array(hasil_y, dtype=float)

def integral(rumus, batas_bawah, batas_atas, gambar=True, n=1000):
    rumus_siap = siap_rumus(rumus)
    h = (batas_atas - batas_bawah) / n
    total = 0.0

    for i in range(n + 1):
        nilai_x = batas_bawah + i * h
        lokal = fungsi.copy()
        lokal['x'] = nilai_x
        nilai_y = eval(rumus_siap, {"__builtins__": None}, lokal)

        if i == 0 or i == n:
            total += nilai_y
        elif i % 2 == 1:
            total += 4 * nilai_y
        else:
            total += 2 * nilai_y

    hasil = (h / 3) * total

    if gambar:
        rentang = abs(batas_atas - batas_bawah)
        margin = rentang * 0.35 if rentang > 0 else 2.0
        x_kurva = np.linspace(min(batas_bawah, batas_atas) - margin, max(batas_bawah, batas_atas) + margin, 400)
        y_kurva = hitung_y(rumus, x_kurva)

        x_arsir = np.linspace(batas_bawah, batas_atas, 250)
        y_arsir = hitung_y(rumus, x_arsir)

        plt.figure(figsize=(8, 5))
        plt.plot(x_kurva, y_kurva, color='royalblue', linewidth=2, label=f'f(x) = {rumus}')
        plt.fill_between(x_arsir, y_arsir, color='skyblue', alpha=0.4,
                         label=f'Luas [{batas_bawah}, {batas_atas}] = {round(hasil, 5)}')
        plt.axhline(0, color='black', linewidth=0.9)
        plt.axvline(0, color='black', linewidth=0.9)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.title(f'Integral: ∫ ({rumus}) dx dari {batas_bawah} sampai {batas_atas}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.tight_layout()
        plt.show()

    return hasil

def grafik(rumus, x_min=-10, x_max=10):
    x_kurva = np.linspace(x_min, x_max, 500)
    y_kurva = hitung_y(rumus, x_kurva)

    plt.figure(figsize=(8, 5))
    plt.plot(x_kurva, y_kurva, color='crimson', linewidth=2, label=f'f(x) = {rumus}')
    plt.axhline(0, color='black', linewidth=0.9)
    plt.axvline(0, color='black', linewidth=0.9)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.title(f'Grafik Fungsi: f(x) = {rumus}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return f'Grafik f(x) = {rumus} ({x_min} sampai {x_max}) selesai ditampilkan.'

fungsi['integral'] = integral
fungsi['grafik'] = grafik

def opr():
    print('___________________________________________________________________________________________')
    print('                              KALKULATOR                                          ')
    print('___________________________________________________________________________________________')
    print('Petunjuk penggunaan')
    print('___________________________________________________________________________________________')
    data = {
        'Dasar & Mutlak': ['+, -, *, /', 'Pangkat: x^y', 'Akar: sqrt(x)', 'Mutlak: abs(x)'],
        'Log & Konstanta': ['Log10: log(x)', 'Log Natural: ln(x)', 'Konstanta: pi, e', 'Faktorial: faktorial(x)'],
        'Trigonometri': ['sin(x), cos(x), tan(x)', 'asin(x), acos(x), atan(x)', 'Pembulatan: ceil, floor', ''],
        'Grafik (Matplotlib)': ['integral("fx", a, b)', 'integral("fx", a, b, False)', 'grafik("fx", min, max)', '']
    } 
    
    df = pd.DataFrame(data, index = range(1, 5))
    print(df.to_string(index=False))
    print('__________________________________________________________________________________________')
    print('Contoh input : 2 + 3 x sin(30) - sqrt(16) + 2^3')
    print('Contoh 1 : integral("x^2 + 2x", 0, 3)   --> hitung integral & tampilkan arsiran grafik')
    print('Contoh 2 : grafik("sin(x)", -360, 360)  --> gambar kurva sinus dari -360° sampai 360°')
    print('Contoh 3 : grafik("abs(x - 2)", -5, 9)  --> gambar grafik nilai mutlak')
    print('tekan enter untuk hasilnya dan ketik "keluar" untuk berhenti perhitungan')

    ans = 0.0

    
    while True:
        a = input('Hitung: ').strip().lower()
        if a in ['keluar', 'exit', 'q']:
            print('kalkulator berhenti')
            break
        if not a:
            continue

        bagian = re.split(r'("[^"]*")', a)
        for i in range(0, len(bagian), 2):
            bagian[i] = bagian[i].replace('x', '*')
        b = ''.join(bagian).replace('^', '**')

        b = re.sub(r'(\d)(\()', r'\1*\2', b)
        b = re.sub(r'(\))(\()', r'\1*\2', b)
        b = re.sub(r'(\d)(sin|cos|tan|asin|acos|atan|log|ln|sqrt|abs|faktorial|integral|grafik|pi|ans|e(?![\d\+\-]))', r'\1*\2', b)

        fungsi['ans'] = ans

        try:
            hasil = eval(b,{"__builtins__": None}, fungsi)
            if isinstance(hasil, str):
                print(f'{hasil}\n')

            else:
                if isinstance(hasil, float) and hasil.is_integer():
                   hasil = int(hasil)
                elif isinstance(hasil, float):
                   hasil = round(hasil, 8)

            ans = hasil
            print(f'= {hasil}\n')
        except ZeroDivisionError:
            print('Error: Tidak bisa membagi dengan nol.\n')
        except ValueError as e:
            print(f'Error Matematika: {e}\n')
        except (SyntaxError, NameError, TypeError):
            print('Error: Format penulisan salah. Pastikan tanda kurung lengkap (contoh: sin(30)).\n')
opr()
