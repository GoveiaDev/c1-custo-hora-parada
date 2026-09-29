"""Lê os valores calculados de modelo.xlsx e grava resultados.json.

O Excel, o LibreOffice e o Google Planilhas (ao baixar como .xlsx) salvam o
resultado de cada fórmula junto com ela. Este script só lê esses valores — não
recalcula nada. Por isso: abra a planilha, altere, salve, e rode este script.

Uso: python exportar_resultados.py
"""
import json
from pathlib import Path

from openpyxl import load_workbook

AQUI = Path(__file__).parent
wb = load_workbook(AQUI / "modelo.xlsx", data_only=True)


def valor(nome):
    aba, ref = next(iter(wb.defined_names[nome].destinations))
    v = wb[aba][ref.replace("$", "")].value
    if v is None:
        raise SystemExit(f"'{nome}' está sem valor calculado. Abra modelo.xlsx numa planilha, salve e rode de novo.")
    return v


NOMES = ["FatorEncargos", "HoraSimplesOp", "CustoHOp", "AcrescimoHora", "CustoHTec", "C_Manut", "C_Pecas",
         "C_OS", "C_Ociosa", "C_Refugo", "C_HE", "C_Margem", "C_Oculto", "C_Total", "C_PorHora", "PctOS"]
saida = {n: valor(n) for n in NOMES}

ws = wb["Cenários"]
saida["cenarios"] = [{
    "rotulo": ws.cell(4, c).value, "horas": ws.cell(5, c).value, "recuperavel": ws.cell(6, c).value,
    "os": ws.cell(9, c).value, "ociosa": ws.cell(10, c).value, "refugo": ws.cell(11, c).value,
    "he": ws.cell(12, c).value, "margem": ws.cell(13, c).value, "oculto": ws.cell(14, c).value,
    "total": ws.cell(15, c).value, "porHora": ws.cell(16, c).value, "pctOS": ws.cell(17, c).value,
} for c in range(2, 8)]

(AQUI / "resultados.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"resultados.json gravado · hora real do operador: R$ {saida['CustoHOp']:.2f} · "
      f"OS registra de {min(c['pctOS'] for c in saida['cenarios']):.0%} a {max(c['pctOS'] for c in saida['cenarios']):.0%}")
