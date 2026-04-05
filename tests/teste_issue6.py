# test_issue6.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from quadtree import QuadTree

# ── Monta imagem com 4 quadrantes bem distintos ───────────
#   TL=10  TR=200
#   BL=50  BR=150
pixels = np.zeros((8, 8), dtype=np.uint8)
pixels[0:4, 0:4] = 10  # TL
pixels[0:4, 4:8] = 200  # TR
pixels[4:8, 0:4] = 50  # BL
pixels[4:8, 4:8] = 150  # BR

qt = QuadTree(limiar=5.0)
qt.inserir(pixels)

# ── Teste 1: cada quadrante retorna a folha correta ───────
no_tl = qt.buscar_pixel(1, 1)  # dentro do TL
no_tr = qt.buscar_pixel(6, 1)  # dentro do TR
no_bl = qt.buscar_pixel(1, 6)  # dentro do BL
no_br = qt.buscar_pixel(6, 6)  # dentro do BR

assert (
    no_tl.eh_folha and no_tl.cor_media == 10
), f"TL esperado 10, got {no_tl.cor_media}"
assert (
    no_tr.eh_folha and no_tr.cor_media == 200
), f"TR esperado 200, got {no_tr.cor_media}"
assert (
    no_bl.eh_folha and no_bl.cor_media == 50
), f"BL esperado 50, got {no_bl.cor_media}"
assert (
    no_br.eh_folha and no_br.cor_media == 150
), f"BR esperado 150, got {no_br.cor_media}"
print("✅ Teste 1: todos os quadrantes retornam a folha correta")

# ── Teste 2: pixel nas bordas extremas ────────────────────
no_origem = qt.buscar_pixel(0, 0)  # canto superior esquerdo
no_final = qt.buscar_pixel(7, 7)  # canto inferior direito

assert no_origem.eh_folha
assert no_final.eh_folha
print("✅ Teste 2: pixels nas bordas extremas encontrados")

# ── Teste 3: o nó retornado CONTÉM o pixel buscado ────────
for px, py in [(0, 0), (3, 3), (4, 4), (7, 7), (2, 5), (5, 2)]:
    no = qt.buscar_pixel(px, py)
    assert (
        no.x <= px < no.x + no.largura
    ), f"px={px} fora do nó x=[{no.x},{no.x + no.largura})"
    assert (
        no.y <= py < no.y + no.altura
    ), f"py={py} fora do nó y=[{no.y},{no.y + no.altura})"
print("✅ Teste 3: nó retornado sempre contém o pixel buscado")

# ── Teste 4: erros esperados ──────────────────────────────
qt_vazio = QuadTree(limiar=10.0)
try:
    qt_vazio.buscar_pixel(0, 0)
    assert False
except ValueError as e:
    print(f"✅ Teste 4a: árvore vazia → '{e}'")

try:
    qt.buscar_pixel(99, 99)  # fora dos limites
    assert False
except ValueError as e:
    print(f"✅ Teste 4b: pixel fora dos limites → '{e}'")

# ── Teste 5: comparativo O(log n) vs O(n) ─────────────────
import time

np.random.seed(0)
pixels_grande = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
qt_grande = QuadTree(limiar=20.0)
qt_grande.inserir(pixels_grande)

N = 1000
pontos = [(np.random.randint(0, 512), np.random.randint(0, 512)) for _ in range(N)]

# Busca pela Quadtree — O(log n)
t0 = time.perf_counter()
for px, py in pontos:
    qt_grande.buscar_pixel(px, py)
t_arvore = (time.perf_counter() - t0) * 1000

# Busca linear (força bruta simulada) — O(n folhas)
folhas = []


def coletar_folhas(no):
    if no.eh_folha:
        folhas.append(no)
        return
    for f in no.filhos:
        if f:
            coletar_folhas(f)


coletar_folhas(qt_grande.raiz)

t0 = time.perf_counter()
for px, py in pontos:
    for no in folhas:
        if no.x <= px < no.x + no.largura and no.y <= py < no.y + no.altura:
            break
t_linear = (time.perf_counter() - t0) * 1000

print(f"\nComparativo ({N} buscas em imagem 512x512):")
print(f"   Quadtree O(log n): {t_arvore:.2f} ms")
print(f"   Linear   O(n):     {t_linear:.2f} ms")
print(f"   Speedup:           {t_linear / t_arvore:.1f}x mais rápido")

print("\n Issue #6 concluída com sucesso!")
