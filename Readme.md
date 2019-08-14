# Scrappers para sitios de noticias de Chile

Actualmente, solo está implementado el de la [radio biobio](https://www.biobiochile.cl/), los cuales publican su contenido bajo la licencia Creative Commons (CC-BY-NC).

Projecto hecho usando los paquetes [scrapy](https://scrapy.org/) y [validators](https://pypi.org/project/validators/), sobre [python 3.7.3](https://www.python.org/)

## Configuración

Cada request se hace cada 5 segundos. Esto puede ser cambiado en el archivo `settings.py`, específicamente, en la variable `DOWNLOAD_DELAY`

Por otra parte, el scrapper por defecto solo visitará hasta 2000 páginas de cada categoría. Esto puede ser modificado en el archivo `biobio_spider.py`, en la variable `MAX_PAGES`


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

    scrapy crawl biobio -o biobio.json

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

