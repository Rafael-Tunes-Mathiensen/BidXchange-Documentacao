"""Gera Banco/ModeloConceitual.png (Figura 6 da monografia).

Fonte das entidades, relações e cardinalidades: código do BidXchange, revisão 1aa8783
(accounts/models.py, bidxchange/models/*.py), conferido com o modelo físico.
Uso: python gerar_modelo_conceitual.py (requer matplotlib).
"""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BLUE = '#1D4E89'; FILL = '#EAF1F9'; INK = '#1F2933'; GRAY = '#6B7280'; AMBER = '#B45309'
W, H = 140, 134
fig = plt.figure(figsize=(14, 13.4), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

E = {}
BW, BH = 24, 8

def ent(key, cx, cy, text, w=BW, h=BH, assoc=False):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle='square,pad=0', fc=FILL, ec=BLUE, lw=2))
    if assoc:
        ax.add_patch(FancyBboxPatch((cx - w / 2 + 0.9, cy - h / 2 + 0.9), w - 1.8, h - 1.8, boxstyle='square,pad=0', fc='none', ec=BLUE, lw=0.9))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=9.6, color=INK, fontweight='bold', linespacing=1.15)
    E[key] = (cx, cy, w, h)

def anchor(key, side, off=0.0):
    cx, cy, w, h = E[key]
    return {'l': (cx - w / 2, cy + off), 'r': (cx + w / 2, cy + off), 't': (cx + off, cy + h / 2), 'b': (cx + off, cy - h / 2)}[side]

def link(a, sa, b, sb, ca, cb, label=None, offa=0.0, offb=0.0, via=None, lpos=0.5, ldx=0.0, ldy=0.0):
    p1 = anchor(a, sa, offa); p2 = anchor(b, sb, offb)
    pts = [p1] + (via or []) + [p2]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=INK, lw=1.5, solid_capstyle='butt', zorder=1)

    def lab(p, q, txt, side):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dy) or 1
        ux, uy = dx / n, dy / n
        x = p[0] + ux * 3.0 - uy * 1.9 * side
        y = p[1] + uy * 3.0 + ux * 1.9 * side
        ax.text(x, y, txt, ha='center', va='center', fontsize=8.6, color=BLUE, fontweight='bold', zorder=3)
    lab(pts[0], pts[1], ca, 1)
    lab(pts[-1], pts[-2], cb, -1)
    if label:
        segs = list(zip(pts[:-1], pts[1:]))
        lens = [math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in segs]
        target = sum(lens) * lpos
        acc = 0
        mx, my = pts[0]
        for (p, q), L in zip(segs, lens):
            if acc + L >= target:
                t = (target - acc) / L
                mx, my = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
                break
            acc += L
        ax.text(mx + ldx, my + ldy, label, ha='center', va='center', fontsize=8.4, color=GRAY, linespacing=1.15,
                bbox=dict(fc='white', ec='none', pad=0.6), zorder=2)

# ---------------- entidades
ent('usu', 16, 124, 'Usuário')
ent('vin', 52, 124, 'Vínculo\n(papel)', assoc=True)
ent('org', 88, 124, 'Organização\n(instituição ou fornecedor)', w=30, h=9)
ent('fav', 124, 124, 'Fornecedor\nfavorito', assoc=True)
ent('cf', 124, 104, 'Categoria do\nfornecedor', assoc=True)
ent('cat', 124, 84, 'Categoria')
ent('cha', 16, 104, 'Chamado\nde suporte')
ent('not', 16, 84, 'Notificação')
ent('aud', 16, 64, 'Evento de\nauditoria')
ent('par', 52, 104, 'Participante\nda votação', assoc=True)
ent('vot', 52, 84, 'Votação\ninterna')
ent('opc', 52, 64, 'Opção')
ent('voto', 52, 44, 'Voto')
ent('cot', 88, 84, 'Cotação')
ent('pro', 88, 64, 'Proposta')
ent('ava', 88, 44, 'Avaliação do\nfornecedor')
ent('con', 124, 64, 'Conversa')
ent('msg', 124, 44, 'Mensagem')

# ---------------- relações
link('usu', 'r', 'vin', 'l', '1', 'N', 'possui', ldy=3.4)
link('vin', 'r', 'org', 'l', 'N', '1', 'em', ldy=3.4)
link('org', 'r', 'fav', 'l', '1', 'N', 'instituição favorita', offa=2.2, offb=2.2, ldx=3, ldy=3.6)
link('org', 'r', 'fav', 'l', '1', 'N', 'fornecedor favorito', offa=-2.2, offb=-2.2, ldx=3, ldy=-3.6)
link('org', 'b', 'cf', 'l', '1', 'N', 'atua em', offa=8, via=[(96, 104)], lpos=0.84, ldy=3.2)
link('cf', 'b', 'cat', 't', 'N', '1', None)
link('cat', 'l', 'cot', 'r', '1', 'N', 'classifica', ldy=3.4)
link('org', 'b', 'cot', 't', '1', 'N', 'publica\n(instituição)', lpos=0.5, ldx=-9)
link('cot', 'b', 'pro', 't', '1', 'N', 'recebe', offa=-4, offb=-4, lpos=0.5, ldx=-6)
link('cot', 'b', 'pro', 't', '0..1', '0..1', 'vencedora', offa=4, offb=4, lpos=0.5, ldx=7)
link('org', 'b', 'pro', 'r', '1', 'N', 'envia (fornecedor)', offa=14, offb=-2.5, via=[(102.5, 61.5)], lpos=0.4, ldx=0)
link('pro', 'r', 'con', 'l', '0..1', '1', 'abre (só proposta\nselecionada)', offa=1.5, offb=1.5, ldx=6, ldy=5.4)
link('con', 'b', 'msg', 't', '1', 'N', 'contém', ldx=6)
link('cot', 'l', 'ava', 'l', '0..1', '1', 'avaliada em', offa=-3, offb=0, via=[(70, 81), (70, 44)], lpos=0.5, ldx=0)
link('cot', 'l', 'vot', 'r', '1', '0..N', 'tem', offa=3, offb=3, ldy=3.4)
link('vin', 'b', 'par', 't', '1', 'N', 'é o vínculo', ldx=7)
link('vot', 'b', 'opc', 't', '1', 'N', 'oferece', ldx=6)
link('par', 'b', 'vot', 't', 'N', '1', 'convida', ldx=7)
link('opc', 'b', 'voto', 't', '1', 'N', 'recebe', ldx=6)
link('par', 'l', 'voto', 'l', '1', '0..1', 'registra', via=[(36, 104), (36, 44)], lpos=0.5, ldx=0)
link('usu', 'b', 'cha', 't', '1', 'N', 'abre', ldx=5)

# barramento do Usuário (esquerda): notificação e auditoria
ax.plot([3.5, 3.5], [124, 64], color=INK, lw=1.5, zorder=1)
ax.plot([3.5, 16 - BW / 2], [124, 124], color=INK, lw=1.5, zorder=1)
for key in ('not', 'aud'):
    x, y, w, h = E[key]
    ax.plot([3.5, x - w / 2], [y, y], color=INK, lw=1.5, zorder=1)
    ax.text(6.0, y + 1.9, 'N', fontsize=8.6, color=BLUE, fontweight='bold', ha='center', zorder=3)
ax.text(6.3, 121.4, '1', fontsize=8.6, color=BLUE, fontweight='bold', ha='center')
ax.text(1.0, 94, 'recebe', fontsize=8.2, color=GRAY, rotation=90, ha='center', va='center')
ax.text(1.0, 74, 'gera', fontsize=8.2, color=GRAY, rotation=90, ha='center', va='center')

def note(x, y, w, h, text, color=AMBER, size=8.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.2', fc='white', ec=color, lw=1.3, ls=(0, (4, 3))))
    ax.text(x + 1.5, y + h / 2, text, ha='left', va='center', fontsize=size, color=color, linespacing=1.35)

note(2, 24, 66, 12.5, 'Restrições de integridade\n'
     'R1  Só proposta selecionada pode originar conversa.\n'
     'R2  A avaliação só existe para cotação encerrada com escolha, avalia o\n'
     '      fornecedor da proposta vencedora e é única por cotação.\n'
     'R3  O favorito liga uma instituição a um fornecedor, sem repetição.\n'
     'R4  Cada participante vota uma vez por votação.', size=8.3)
note(70, 10, 68, 19.5, 'Notas\n'
     'N1  O usuário também é o autor registrado de cotações, propostas,\n'
     '       votações, avaliações, conversas, mensagens e favoritos; essas\n'
     '       ligações foram omitidas para não poluir o desenho.\n'
     'N2  A proposta pertence a uma cotação e a um fornecedor; a nova\n'
     '       versão aponta para a anterior (relação com ela mesma).\n'
     'N3  O participante da votação é um vínculo (membro) da instituição.\n'
     'N4  O chamado de pedido de categoria pode apontar para a categoria\n'
     '       criada (0..1). A notificação tem usuário e/ou organização como\n'
     '       destino. O evento de auditoria cita a entidade afetada por tipo\n'
     '       e identificador, sem chave estrangeira.', size=8.0, color=GRAY)
ax.text(2, 15.5, 'Cardinalidade (mínima..máxima): 1 = exatamente um; 0..1 = opcional;\nN = um ou mais; 0..N = nenhum ou vários. Moldura dupla = entidade\nassociativa (resolve uma relação N para N entre duas entidades).',
        fontsize=8.0, color=GRAY, ha='left', va='center', linespacing=1.35)
fig.savefig('ModeloConceitual.png', dpi=100, facecolor='white')
print('ok')
