
    # Añadir todos los Telemundo y ESPN en español
    print("Buscando canales Telemundo y ESPN...")

    todos = analizar(descargar(f"{BASE}index.m3u"))
    espanol = por_idioma["spa"]

    for titulo, url in todos:
        nombre = titulo.lower()

        es_telemundo = "telemundo" in nombre
        es_espn_espanol = "espn" in nombre and url in espanol

        if (es_telemundo or es_espn_espanol) and url not in religiosos:
            if url not in canales:
                grupo = "TELEMUNDO" if es_telemundo else "ESPN EN ESPAÑOL"
                titulo = titulo.replace(
                    ",", f' group-title="{grupo}",', 1
                )
                canales[url] = (titulo, grupo, "spa")
                    salida = ["#EXTM3U"]
