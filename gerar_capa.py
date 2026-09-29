"""Gera capa.png a partir de resultados.json — os valores calculados pelo Excel.

Uso: python gerar_capa.py   (depois de abrir e salvar modelo.xlsx no Excel)
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

AQUI = Path(__file__).parent
r = json.loads((AQUI / "resultados.json").read_text(encoding="utf-8-sig"))

fonte = "Segoe UI" if any("Segoe UI" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams["font.family"] = fonte

TINTA, TINTA2, APOIO, ACAO, METRICA, REGUA = "#0f172a", "#475569", "#64748b", "#1d4ed8", "#0e7490", "#e2e8f0"
OCULTO = "#cbd5e1"
brl = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
brl0 = lambda v: f"R$ {v:,.0f}".replace(",", ".")

fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor="#f8fafc")
fig.text(0.07, 0.935, "PROJETO C1 · CUSTO DE PARADA", fontsize=15, color=APOIO, fontweight="bold")
fig.text(0.07, 0.905, "A hora do operador não custa\nsalário ÷ 220.", fontsize=40, color=TINTA,
         fontweight="bold", va="top", linespacing=1.12)

fig.text(0.07, 0.715, brl(r["HoraSimplesOp"]), fontsize=64, color="#94a3b8", fontweight="bold")
fig.text(0.445, 0.722, "→", fontsize=48, color=APOIO)
fig.text(0.53, 0.715, brl(r["CustoHOp"]), fontsize=64, color=METRICA, fontweight="bold")
fig.text(0.07, 0.685, f"{r['AcrescimoHora']:.0%} a mais, só com encargos legais — operador de R$ 3.000",
         fontsize=19, color=TINTA2, va="top")

fig.text(0.07, 0.605, "E numa parada, quanto a ordem de serviço enxerga?", fontsize=22, color=TINTA, fontweight="bold")

ax = fig.add_axes([0.07, 0.15, 0.86, 0.43], facecolor=fig.get_facecolor())
cen = r["cenarios"]
ys = [y * 1.5 for y in range(len(cen))][::-1]
maior = max(c["total"] for c in cen)
for y, c in zip(ys, cen):
    # Rótulo acima da barra, alinhado à esquerda — nunca cortado pela margem.
    situacao = "dá para recuperar com hora extra" if c["recuperavel"] else "linha gargalo, produção perdida"
    ax.text(0, y + 0.52, f"Parada de {c['horas']:.0f} h  ·  {situacao}", fontsize=15, color=TINTA2, va="bottom")
    ax.barh(y, c["os"], color=ACAO, height=0.62)
    ax.barh(y, c["oculto"], left=c["os"] + maior * 0.004, color=OCULTO, height=0.62)
    ax.text(c["total"] + maior * 0.02, y, f"OS vê {c['pctOS']:.0%}", va="center", fontsize=17,
            color=TINTA, fontweight="bold")
ax.set_yticks([])
ax.set_ylim(min(ys) - 0.5, max(ys) + 1.1)
ax.set_xlim(0, maior * 1.2)
ax.set_xticks([])
for lado in ["top", "right", "bottom", "left"]:
    ax.spines[lado].set_visible(False)
ax.tick_params(left=False)

fig.text(0.07, 0.125, "■", fontsize=18, color=ACAO)
fig.text(0.1, 0.126, "registrado na ordem de serviço", fontsize=16, color=TINTA2)
fig.text(0.47, 0.125, "■", fontsize=18, color=OCULTO)
fig.text(0.5, 0.126, "operador parado, refugo, hora extra, margem", fontsize=16, color=TINTA2)

fig.text(0.07, 0.055, "Alíquotas pela legislação (Lucro Real ou Presumido). Salários, produção e peças\n"
         "são valores redondos de exemplo. Modelo aberto em Excel.", fontsize=14, color=APOIO, linespacing=1.4)
fig.savefig(AQUI / "capa.png", dpi=100, facecolor=fig.get_facecolor())
print("capa.png salva")
