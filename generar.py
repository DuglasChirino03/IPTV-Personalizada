
import urllib.request
from pathlib import Path

BASE = "https://iptv-org.github.io/iptv/"
IDIOMAS = ["spa", "eng"]
CATEGORIAS = [
    "sports", "movies", "series", "news", "entertainment",
    "kids", "music", "documentary", "culture", "education"
]

def descargar(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

def analizar(texto):
    resultado = []
    titulo = None
    for linea in texto.splitlines():
        linea = linea.strip()
        if linea.startswith("#EXTINF"):
            titulo = linea
        elif linea and not linea.startswith("#") and titulo:
            resultado.append((titulo, linea))
            titulo = None
    return resultado

def main():
    print("Descargando listas de idiomas...")
    por_idioma = {}
    for idioma in IDIOMAS:
        texto = descargar(f"{BASE}languages/{idioma}.m3u")
        por_idioma[idioma] = {url for _, url in analizar(texto)}

    print("Preparando exclusión de canales religiosos...")
    religiosos = {
        url for _, url in analizar(
            descargar(f"{BASE}categories/religious.m3u")
        )
    }

    canales = {}
    for idioma in IDIOMAS:
        print(f"Procesando idioma: {idioma}")
        permitidos = por_idioma[idioma]

        for categoria in CATEGORIAS:
            texto = descargar(f"{BASE}categories/{categoria}.m3u")
            for titulo, url in analizar(texto):
                if url in permitidos and url not in religiosos:
                    if url not in canales:
                        canales[url] = (titulo, categoria, idioma)

    salida = ["#EXTM3U"]
    for idioma in IDIOMAS:
        for url, (titulo, categoria, lang) in canales.items():
            if lang == idioma:
                salida.append(
                    titulo.replace('group-title="', 'group-title="')
                )
                salida.append(url)

    Path("lista.m3u").write_text(
        "\n".join(salida) + "\n", encoding="utf-8"
    )
    print(f"Lista creada: {len(canales)} canales.")

if __name__ == "__main__":
    main()
              
