# Landing_page_flask
Prototipo de pagina estática usando flask y sus funciones

## base de datos usada

```mermaid
erDiagram
    ALCALDE {
        INTEGER id PK
        VARCHAR nombre
        TEXT descripcion
        VARCHAR imagen
        TEXT vision
        TEXT mision
        TEXT compromisos
        TEXT logros
        DATETIME updated_at
    }

    CONCEJAL {
        INTEGER id PK
        VARCHAR nombre
        VARCHAR cargo
        VARCHAR partido
        TEXT comisiones
        TEXT biografia
        VARCHAR imagen
        BOOLEAN activo
        INTEGER orden
        DATETIME created_at
    }

    NOTICIA {
        INTEGER id PK
        VARCHAR titulo
        TEXT contenido
        VARCHAR imagen
        DATETIME fecha_publicacion
        BOOLEAN activa
        DATETIME created_at
    }

    CONCURSO {
        INTEGER id PK
        VARCHAR titulo
        TEXT descripcion
        VARCHAR fecha
        VARCHAR tipo
        BOOLEAN activo
        DATETIME created_at
    }

    ARCHIVO_CONCURSO {
        INTEGER id PK
        INTEGER concurso_id FK
        VARCHAR nombre_archivo
        VARCHAR ruta_archivo
        VARCHAR tipo
        DATETIME created_at
    }

    CONCURSO ||--o{ ARCHIVO_CONCURSO : "tiene"
