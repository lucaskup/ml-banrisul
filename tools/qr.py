"""Gera os QR codes SVG em qr/ (índice e uma por página interativa). Requer: pip install segno"""
import segno, pathlib
BASE='https://lucaskup.github.io/ml-banrisul/'
out=pathlib.Path(__file__).parent.parent/'qr'; out.mkdir(exist_ok=True)
pages=['','1-ajuste.html','2-dado-errado.html','3-enviesado.html','4-gradiente.html','c1-passo-a-passo.html','c2-escolher-k.html','c3-limitacoes.html']
for p in pages:
    name=p.removesuffix('.html') or 'index'
    segno.make(BASE+p, error='m').save(str(out/f'{name}.svg'), scale=10, border=2, dark='#000000', light='#ffffff')
    print(name, BASE+p)
