"""Gera o Markdown de Antes/Depois entre duas versões de um .docx do TCC.

Uso:
    python gerar_md_alteracoes.py ANTES.docx DEPOIS.docx SAIDA.md [--titulo "Assunto"]

Compara parágrafos e células de tabela, ignora o sumário e destaca com
<mark>…</mark> apenas os trechos alterados. Requer python-docx.
"""
import argparse
import difflib
import re

import docx


def titulo_secao(paragrafos, i):
    for k in range(i, -1, -1):
        if paragrafos[k].style.name.startswith("Heading"):
            return paragrafos[k].text
    return "Elementos pré-textuais"


def marcar(antes, depois):
    """Devolve as duas versões com os trechos diferentes em <mark>."""
    ta = re.findall(r"\S+|\s+", antes)
    tb = re.findall(r"\S+|\s+", depois)
    ops = difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes()
    # Junta mudanças separadas por trechos iguais curtos (até uma palavra),
    # para o destaque sair em blocos contínuos.
    juntos = []
    for n, op in enumerate(ops):
        tag, a0, a1, b0, b1 = op
        curto = tag == "equal" and (a1 - a0) <= 3 and n < len(ops) - 1
        if juntos and juntos[-1][0] != "equal" and (tag != "equal" or curto):
            juntos[-1] = ("replace", juntos[-1][1], a1, juntos[-1][3], b1)
        else:
            juntos.append(op)
    sa, sb = [], []
    for tag, a0, a1, b0, b1 in juntos:
        x, y = "".join(ta[a0:a1]), "".join(tb[b0:b1])
        if tag == "equal":
            sa.append(x)
            sb.append(y)
            continue
        for saida, t in ((sa, x), (sb, y)):
            nucleo = t.strip()
            if nucleo:
                ini = t[: len(t) - len(t.lstrip())]
                fim = t[len(t.rstrip()):]
                saida.append(f"{ini}<mark>{nucleo}</mark>{fim}")
            else:
                saida.append(t)
    return "".join(sa), "".join(sb)


def nome_tabela(doc, tabela, n):
    """Usa o parágrafo não vazio anterior à tabela (legenda ou título da ficha)."""
    anterior = tabela._tbl.getprevious()
    while anterior is not None:
        if anterior.tag.endswith("}p"):
            texto = "".join(t.text or "" for t in anterior.iter() if t.tag.endswith("}t")).strip()
            if texto:
                return texto
        anterior = anterior.getprevious()
    return f"Tabela {n + 1} (ordem no documento)"


def textos_paragrafos(doc):
    return [
        (p.text, p.style.name)
        for p in doc.paragraphs
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("antes")
    ap.add_argument("depois")
    ap.add_argument("saida")
    ap.add_argument("--titulo", default="Alterações no documento")
    args = ap.parse_args()

    A, B = docx.Document(args.antes), docx.Document(args.depois)
    pa, pb = textos_paragrafos(A), textos_paragrafos(B)
    out = [f"# {args.titulo}", "", "Os trechos alterados estão destacados com marca-texto.", ""]

    sm = difflib.SequenceMatcher(None, [t for t, _ in pa], [t for t, _ in pb], autojunk=False)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal":
            continue
        for k in range(max(a1 - a0, b1 - b0)):
            ia = a0 + k if a0 + k < a1 else None
            ib = b0 + k if b0 + k < b1 else None
            antes = pa[ia][0] if ia is not None else ""
            depois = pb[ib][0] if ib is not None else ""
            estilos = (pa[ia][1] if ia is not None else "") + (pb[ib][1] if ib is not None else "")
            if "toc" in estilos.lower() or not (antes.strip() or depois.strip()):
                continue
            secao = titulo_secao(B.paragraphs, ib) if ib is not None else titulo_secao(A.paragraphs, ia)
            ma, mb = marcar(antes, depois)
            out += [f"## {secao}", "", "**Antes:**", "", ma or "(parágrafo novo)", "",
                    "**Depois:**", "", mb or "(parágrafo removido)", "", "---", ""]

    # Tabelas: compara célula a célula quando a estrutura bate.
    for n, (ta, tb) in enumerate(zip(A.tables, B.tables)):
        linhas = []
        la = [[c.text for c in r.cells] for r in ta.rows]
        lb = [[c.text for c in r.cells] for r in tb.rows]
        sm = difflib.SequenceMatcher(None, ["	".join(r) for r in la], ["	".join(r) for r in lb], autojunk=False)
        for tag, a0, a1, b0, b1 in sm.get_opcodes():
            if tag == "equal":
                continue
            for k in range(max(a1 - a0, b1 - b0)):
                ca = la[a0 + k] if a0 + k < a1 else ["(linha nova)"]
                cb = lb[b0 + k] if b0 + k < b1 else ["(linha removida)"]
                linhas.append((ca, cb))
        if not linhas:
            continue
        out += [f"## {nome_tabela(B, tb, n)}", ""]
        cab = [c.text for c in tb.rows[0].cells]
        out += ["| Versão | " + " | ".join(cab) + " |", "|---" * (len(cab) + 1) + "|"]
        for ca, cb in linhas:
            out.append("| Antes | " + " | ".join(ca) + " |")
            out.append("| Depois | " + " | ".join(cb) + " |")
        out += ["", "---", ""]

    with open(args.saida, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"MD gerado em {args.saida}")


if __name__ == "__main__":
    main()
