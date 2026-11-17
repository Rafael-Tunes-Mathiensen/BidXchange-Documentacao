"""Gera CasosDeUso/EstadosCotacao.png (Figura 5 da monografia).

Fonte dos estados e das transições: código do BidXchange, revisão 1aa8783
(bidxchange/models/quotes.py, services/quotes.py e services/proposals.py).
Uso: python gerar_estados_cotacao.py (requer matplotlib).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

BLUE = '#1D4E89'; FILL = '#EAF1F9'; INK = '#1F2933'; GRAY = '#6B7280'; AMBER = '#B45309'
W, H = 140, 118
fig = plt.figure(figsize=(14, 11.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

def box(cx, cy, w, h, text, dashed=False, size=10.5):
    ec = GRAY if dashed else BLUE
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle='round,pad=0,rounding_size=2.2',
                                fc='#F3F4F6' if dashed else FILL, ec=ec, lw=1.8, ls=(0, (4, 3)) if dashed else '-'))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=size, color=GRAY if dashed else INK,
            style='italic' if dashed else 'normal')
    return (cx, cy, w, h)

def edge(b, side):
    cx, cy, w, h = b
    return {'l': (cx - w / 2, cy), 'r': (cx + w / 2, cy), 't': (cx, cy + h / 2), 'b': (cx, cy - h / 2)}[side]

def arrow(p1, p2, label=None, lp=None, dashed=False, rad=0.0, ha='center', color=None, size=9):
    c = color or (GRAY if dashed else INK)
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=13, lw=1.6, color=c,
                                 ls=(0, (4, 3)) if dashed else '-', connectionstyle=f'arc3,rad={rad}',
                                 shrinkA=0, shrinkB=0))
    if label:
        x, y = lp
        ax.text(x, y, label, ha=ha, va='center', fontsize=size, color=GRAY if dashed else '#374151',
                linespacing=1.25)

def start(x, y):
    ax.add_patch(Circle((x, y), 1.6, fc=INK, ec=INK))
    return (x + 1.6, y)

def title(x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=14, color=BLUE, fontweight='bold')

# ---------------- Cotação
title(70, 115, 'Cotação')
asc = box(62, 98, 24, 10, 'Aberta')
ras = box(20, 98, 24, 10, 'Rascunho')
cesc = box(116, 106, 28, 10, 'Encerrada\ncom escolha')
sesc = box(116, 90, 28, 10, 'Encerrada\nsem escolha')
can = box(20, 76, 24, 9, 'Cancelada')
susp = box(62, 76, 24, 9, 'Suspensa\n(não existe)', dashed=True, size=9.5)

s1 = start(4, 98); arrow(s1, edge(ras, 'l'), 'criar rascunho\n(CU12)', (9, 104.5))
ax.add_patch(Circle((43, 109), 1.6, fc=INK, ec=INK))
arrow((44.4, 108.2), (54.5, 103.2), None)
ax.text(34, 113, 'criar e publicar\n(CU12)', ha='center', va='center', fontsize=9, color='#374151', linespacing=1.25)

arrow(edge(ras, 'r'), edge(asc, 'l'), 'publicar\n(CU12 ou CU13)', (41, 102.6))
arrow(edge(ras, 'b'), edge(can, 't'), 'cancelar rascunho (CU14)', (21.5, 87), ha='left')
arrow((edge(asc, 'r')[0], 100.5), edge(cesc, 'l'), 'selecionar proposta (CU15)', (88, 106.8), rad=-0.08)
arrow((edge(asc, 'r')[0], 96), edge(sesc, 'l'), 'encerrar sem escolha (CU14)', (88, 90.2), rad=0.0)

arrow(edge(asc, 'b'), edge(susp, 't'), 'suspender', (65, 86.7), dashed=True, ha='left')
arrow((edge(susp, 'l')[0], 74), (edge(can, 'r')[0] + 0.2, 74), None, dashed=True) if False else None

# prazo
ax.add_patch(FancyBboxPatch((78, 60), 59, 11, boxstyle='round,pad=0,rounding_size=1.5', fc='white', ec=AMBER, lw=1.5, ls=(0, (4, 3))))
ax.text(107.5, 65.5, 'Fim do prazo (closes_at): bloqueia novos envios de propostas,\nmas a cotação continua Aberta; não há encerramento automático (RF12).\nSuspender e reabrir cotação não existem no código.',
        ha='center', va='center', fontsize=9, color=AMBER, linespacing=1.35)
ax.add_patch(FancyArrowPatch((98, 71), (68, 92.5), arrowstyle='-', lw=1.2, color=AMBER, ls=(0, (3, 3)), connectionstyle='arc3,rad=0.0'))

# legenda
ax.add_patch(FancyBboxPatch((2, 58), 128, 0.01, boxstyle='square,pad=0', fc='none', ec='none'))
ax.plot([2, 138], [57.5, 57.5], color='#D1D5DB', lw=1)

# ---------------- Proposta
title(32, 53, 'Proposta')
ati = box(22, 42, 22, 9, 'Ativa')
sub = box(56, 42, 24, 9, 'Substituída')
sel = box(22, 22, 24, 9, 'Selecionada')
nsel = box(56, 22, 26, 9, 'Não\nselecionada')
ret = box(22, 8, 24, 8, 'Retirada\n(não usada)', dashed=True, size=9)
s3 = start(3, 42); arrow(s3, edge(ati, 'l'), 'enviar\n(CU09)', (7.5, 47))
arrow(edge(ati, 'r'), edge(sub, 'l'), 'nova versão\ndo fornecedor (CU09)', (39, 48))
arrow(edge(ati, 'b'), edge(sel, 't'), 'escolhida (CU15)', (23.5, 32), ha='left')
arrow((edge(ati, 'r')[0] - 3, 37.6), (50, 26.6), 'demais\nativas (CU15)', (45, 35), rad=0.0)
ax.text(40, 14, 'Ao encerrar sem escolha (CU14), as propostas\nativas permanecem Ativas.', ha='left', va='center', fontsize=9, color=AMBER, linespacing=1.3)

# ---------------- Votação
title(108, 53, 'Votação interna')
vab = box(98, 42, 24, 9, 'Aberta')
vfe = box(98, 22, 28, 9, 'Encerrada\n(pelo prazo)')
vras = box(128, 42, 20, 9, 'Rascunho\n(não usado)', dashed=True, size=9)
s4 = start(80, 42); arrow(s4, edge(vab, 'l'), None)
ax.text(83.5, 47.5, 'criar votação (CU24)', ha='left', va='center', fontsize=9, color='#374151')
ax.text(83.5, 52.2 - 0.2, '', fontsize=9)
arrow(edge(vab, 'b'), edge(vfe, 't'), 'passa o prazo da\nvotação (closes_at)', (99.5, 32.4), ha='left')
ax.text(80, 12, 'A votação só nasce com a cotação Aberta e ao menos uma proposta Ativa,\ncriada por proprietário ou aprovador. O estado gravado continua Aberta;\na tela mostra Encerrada depois do prazo. Ela não encerra nem seleciona\na cotação: o resultado orienta, e a seleção continua no CU15.',
        ha='left', va='center', fontsize=9, color=AMBER, linespacing=1.3)

# legenda tracejado
ax.add_patch(FancyBboxPatch((2, 1.2), 5, 2.4, boxstyle='round,pad=0,rounding_size=0.8', fc='#F3F4F6', ec=GRAY, lw=1.4, ls=(0, (4, 3))))
ax.text(8.5, 2.4, 'Tracejado cinza: estado ou transição inexistente no código.', ha='left', va='center', fontsize=8.5, color=GRAY)

fig.savefig('EstadosCotacao.png', dpi=100, facecolor='white')
print('ok')
