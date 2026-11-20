"""Trace the registered Orryx Commodities logo (assets/src/OC Logo - Dark Theme.png)
into exact vector outlines. Nothing is redrawn: the shapes and letters are followed
edge by edge from the supplied file. Run from the project root:  python3 tools/trace_logo.py
Outputs: assets/logo/*.svg, assets/logo/*.png, tools/logo-defs.html (pasted into index.html)."""
from PIL import Image
import numpy as np, json, os

SRC = 'assets/src/OC Logo - Dark Theme.png'
UP = 4                      # trace on a 4x finer grid for sub-pixel accuracy
im = Image.open(SRC).convert('RGB')
W, H = im.size
a = np.asarray(im).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
white = np.clip(b / 255.0, 0, 1)                 # letters: the only pixels with blue in them
orange = np.clip((r - b) / 252.0, 0, 1)          # the mark

m = orange > 0.5
ORANGE = tuple(int(np.median(c[m])) for c in (r, g, b))
print('logo orange', ORANGE, '#%02X%02X%02X' % ORANGE)

def blur(f, sigma):
    if sigma <= 0: return f
    n = int(sigma * 3) + 1
    k = np.exp(-0.5 * (np.arange(-n, n + 1) / sigma) ** 2); k /= k.sum()
    out = np.zeros_like(f)
    p = np.pad(f, ((n, n), (0, 0)), mode='edge')
    for i, w in enumerate(k): out += w * p[i:i + f.shape[0], :]
    f2 = np.zeros_like(f)
    p = np.pad(out, ((0, 0), (n, n)), mode='edge')
    for i, w in enumerate(k): f2 += w * p[:, i:i + f.shape[1]]
    return f2

def upsample(f):
    return np.asarray(Image.fromarray(f.astype(np.float32), 'F').resize((f.shape[1] * UP, f.shape[0] * UP), Image.BICUBIC))

def contours(F):
    """Marching squares at 0.5 with linear interpolation. Returns closed loops in grid units."""
    Bm = F > 0.5
    c0, c1, c2, c3 = Bm[:-1, :-1], Bm[:-1, 1:], Bm[1:, 1:], Bm[1:, :-1]
    case = c0 * 8 + c1 * 4 + c2 * 2 + c3 * 1
    ys, xs = np.nonzero((case > 0) & (case < 15))
    pts = {}
    def P(key):
        if key in pts: return
        kind, i, j = key
        if kind == 'h':
            v0, v1 = F[i, j], F[i, j + 1]; t = (0.5 - v0) / (v1 - v0); pts[key] = (j + t, float(i))
        else:
            v0, v1 = F[i, j], F[i + 1, j]; t = (0.5 - v0) / (v1 - v0); pts[key] = (float(j), i + t)
    adj = {}
    def seg(k1, k2):
        P(k1); P(k2)
        adj.setdefault(k1, []).append(k2); adj.setdefault(k2, []).append(k1)
    for i, j in zip(ys.tolist(), xs.tolist()):
        cs = int(case[i, j])
        T, Bt, L, R = ('h', i, j), ('h', i + 1, j), ('v', i, j), ('v', i, j + 1)
        if cs in (1, 14): seg(L, Bt)
        elif cs in (2, 13): seg(Bt, R)
        elif cs in (3, 12): seg(L, R)
        elif cs in (4, 11): seg(T, R)
        elif cs in (6, 9): seg(T, Bt)
        elif cs in (7, 8): seg(T, L)
        else:
            centre = (F[i, j] + F[i, j + 1] + F[i + 1, j] + F[i + 1, j + 1]) / 4 > 0.5
            if (cs == 5) == centre: seg(T, L); seg(Bt, R)
            else: seg(T, R); seg(L, Bt)
    loops, seen = [], set()
    for start in adj:
        if start in seen: continue
        loop, prev, cur = [], None, start
        while True:
            seen.add(cur); loop.append(pts[cur])
            nb = adj[cur]
            assert len(nb) == 2, 'open contour'
            nxt = nb[0] if nb[0] != prev else nb[1]
            if nb[0] == nb[1]: nxt = nb[0]
            prev, cur = cur, nxt
            if cur == start: break
        loops.append(np.array(loop))
    return loops

def rdp(pts, eps):
    """Ramer-Douglas-Peucker on an open polyline."""
    keep = np.zeros(len(pts), bool); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        s, e = stack.pop()
        if e <= s + 1: continue
        p0, p1 = pts[s], pts[e]; d = p1 - p0; n = np.hypot(*d)
        seg = pts[s + 1:e] - p0
        dist = np.hypot(seg[:, 0], seg[:, 1]) if n == 0 else np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / n
        k = int(dist.argmax())
        if dist[k] > eps:
            keep[s + 1 + k] = True; stack.append((s, s + 1 + k)); stack.append((s + 1 + k, e))
    return pts[keep]

def simplify_closed(loop, eps):
    far = int(np.hypot(*(loop - loop[0]).T).argmax())
    a1 = rdp(loop[:far + 1], eps); a2 = rdp(np.vstack([loop[far:], loop[:1]]), eps)
    return np.vstack([a1[:-1], a2[:-1]])

def trace(field, sigma, eps, pad=24):
    ys, xs = np.nonzero(field > 0.2)
    x0, x1, y0, y1 = xs.min() - pad, xs.max() + pad, ys.min() - pad, ys.max() + pad
    F = upsample(blur(field[y0:y1, x0:x1], sigma))
    out = []
    for lp in contours(F):
        p = np.empty_like(lp)
        p[:, 0] = x0 + (lp[:, 0] + 0.5) / UP - 0.5 + 0.5      # +0.5: pixel centres -> SVG user units
        p[:, 1] = y0 + (lp[:, 1] + 0.5) / UP - 0.5 + 0.5
        if len(p) < 12: continue
        out.append(simplify_closed(p, eps))
    return out

def path_d(loops):
    d = []
    for lp in loops:
        q = np.round(lp, 1); q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
        s = 'M%g %g' % (q[0, 0], q[0, 1])
        for dx, dy in np.round(np.diff(q, axis=0), 1):
            s += 'l%g%s%g' % (dx, '' if dy < 0 else ' ', dy)
        d.append(s + 'z')
    return ''.join(d)

mark = trace(orange, 0.9, 0.05)
word = trace(white, 0.45, 0.04)
print('mark loops', len(mark), [len(l) for l in mark])
print('word loops', len(word))

# group letter outlines with their inner counters, left to right
bb = [(l[:, 0].min(), l[:, 1].min(), l[:, 0].max(), l[:, 1].max()) for l in word]
def inside(i, j): return i != j and bb[i][0] >= bb[j][0] and bb[i][1] >= bb[j][1] and bb[i][2] <= bb[j][2] and bb[i][3] <= bb[j][3]
holes = {i: j for i in range(len(word)) for j in range(len(word)) if inside(i, j)}
outers = sorted([i for i in range(len(word)) if i not in holes], key=lambda i: bb[i][0])
letters = [[word[i]] + [word[h] for h, o in holes.items() if o == i] for i in outers]
print('letters', len(letters), 'counters', len(holes))

mx0 = min(l[:, 0].min() for l in mark); mx1 = max(l[:, 0].max() for l in mark)
my0 = min(l[:, 1].min() for l in mark); my1 = max(l[:, 1].max() for l in mark)
print('mark box', mx0, my0, mx1, my1)
M = 14
VB = '%g %g %g %g' % (round(mx0 - M), round(my0 - M), round(mx1 - mx0 + 2 * M), round(my1 - my0 + 2 * M))
HEX = '#%02X%02X%02X' % ORANGE
BLACK = '#060605'          # the black used for the letters in the supplied light-theme file
BLACK_RGB = (6, 6, 5)
d_mark = path_d(mark); d_letters = [path_d(l) for l in letters]

os.makedirs('assets/logo', exist_ok=True)
def svg(bg, txt, full):
    vb = '0 0 %d %d' % (W, H) if full else VB
    s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">' % vb
    s += '<title>Orryx Commodities</title>'
    if bg: s += '<rect width="%d" height="%d" fill="%s"/>' % (W, H, bg)
    s += '<path fill="%s" fill-rule="evenodd" d="%s"/>' % (HEX, d_mark)
    s += '<path fill="%s" fill-rule="evenodd" d="%s"/>' % (txt, ''.join(d_letters))
    return s + '</svg>\n'
open('assets/logo/orryx-logo-dark.svg', 'w').write(svg('#000000', '#FFFFFF', True))
open('assets/logo/orryx-logo-light.svg', 'w').write(svg('#FFFFFF', BLACK, True))
open('assets/logo/orryx-logo-transparent-white-text.svg', 'w').write(svg(None, '#FFFFFF', False))
open('assets/logo/orryx-logo-transparent-black-text.svg', 'w').write(svg(None, BLACK, False))

defs = '<path id="lm" fill-rule="evenodd" d="%s"/>\n' % d_mark
for i, d in enumerate(d_letters): defs += '<path id="lw%d" fill-rule="evenodd" d="%s"/>\n' % (i, d)
defs += '<symbol id="oc-logo" viewBox="%s"><use href="#lm" fill="%s"/>%s</symbol>\n' % (VB, HEX, ''.join('<use href="#lw%d"/>' % i for i in range(len(d_letters))))
open('tools/logo-defs.html', 'w').write(defs)
json.dump({'viewBox': VB, 'orange': HEX, 'letters': len(d_letters), 'box': [float(mx0), float(my0), float(mx1), float(my1)]}, open('tools/logo-meta.json', 'w'))
print('viewBox', VB, 'defs bytes', len(defs))

# high-resolution PNG set (4x the supplied file), same edges as the vector
Fo = upsample(blur(orange, 0.9)); Fw = upsample(blur(white, 0.45))
def ramp(F): return np.clip((F - 0.5) * 6 + 0.5, 0, 1)
co, cw = ramp(Fo), ramp(Fw)
O = np.array(ORANGE, np.float32)
def flat(bg, txt, name):
    out = np.zeros(co.shape + (3,), np.float32) + np.array(bg, np.float32)
    out = out * (1 - co[..., None]) + O * co[..., None]
    out = out * (1 - cw[..., None]) + np.array(txt, np.float32) * cw[..., None]
    Image.fromarray(out.round().clip(0, 255).astype(np.uint8)).save(name, optimize=True)
def clear(txt, name):
    al = np.clip(co + cw, 0, 1)
    rgb = (O * co[..., None] + np.array(txt, np.float32) * cw[..., None]) / np.maximum(al, 1e-6)[..., None]
    rgb[al == 0] = O
    Image.fromarray(np.dstack([rgb, al * 255]).round().clip(0, 255).astype(np.uint8), 'RGBA').save(name, optimize=True)
px = W * UP
flat((0, 0, 0), (255, 255, 255), 'assets/logo/orryx-logo-dark-%dpx.png' % px)
flat((255, 255, 255), BLACK_RGB, 'assets/logo/orryx-logo-light-%dpx.png' % px)
clear((255, 255, 255), 'assets/logo/orryx-logo-transparent-white-text-%dpx.png' % px)
clear(BLACK_RGB, 'assets/logo/orryx-logo-transparent-black-text-%dpx.png' % px)
print('png width', px)
