# Scrappers para sitios de noticias de Chile

Actualmente, están implementados los de la [Radio Biobio](https://www.biobiochile.cl/) y de [El Desconcierto](https://www.eldesconcierto.cl/noticias/pais/).

Projecto hecho usando los paquetes [scrapy](https://scrapy.org/) y [validators](https://pypi.org/project/validators/), sobre [python 3.7.3](https://www.python.org/)

## Configuración

Cada request se hace cada 1 segundo. Esto puede ser cambiado en el archivo `settings.py`, específicamente, en la variable `DOWNLOAD_DELAY`

Por otra parte, los scrappers por defecto solo visitarán hasta `N` páginas de cada categoría, lo que puede ser modificado en el los mismos archivos `*_spider.py`, específicamente en la variable `MAX_PAGES`

Adicionalmente, los scrappers pueden ser configurados para que inicien sus rutinas en páginas personalizadas. Dados los recientes hechos (octubre 2019), se dejarán configuradas los scrappers para que recolecten información sobre la crisis que acontece en chile.


## Instalar los paquetes:

Instalar scrapy:

    pip install Scrapy

Instalar validators:

    pip install validators


## Iniciar el scrapper de biobio

En una consola:


Ir al directorio del scrapper de la radio biobio

    cd scrapper_biobio

Opcional. borrar archivo biobio.json para limpiar alguna ejecución anterior: 

    rm biobio.json

Ejecutar:

    # Crawler para la biobio:
    scrapy crawl biobio -o biobio.json

    # Crawler para el desconcierto:
    scrapy crawl el_desconcierto -o el_desconcierto.json

## Formato de las noticias:

Las noticias son guardadas en un archivo formato json. A medida que el crawler trabaja, va almacenando un arreglo con las noticias según la siguiente estructura:


```json
{
    "author": "...",
    "author_link": "/lista/autores/...",
    "category": "...",
    "content": "...",
    "embedded_links": ["https://media.biobiochile.cl/...",
                        "https://media.biobiochile.cl/...", "..."],
    "link": "https://www.biobiochile.cl/.../.../.../AAAA/mm/DD/...",
    "publication_date": " DD/mm/AAAA",
    "publication_hour": "HH:MM",
    "subcategory": "chile",
    "tags": ["#Tag1", "#Tag2", "#Tag3", "..."],
    "title": "... "
}
```

