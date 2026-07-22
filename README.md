# 🇩🇪 Deutsch Quiz

Aplicación de vocabulario alemán tipo **Kahoot**: aparece la palabra en
**español** y hay que elegir la traducción correcta en **alemán** entre
varias opciones. Construida con [Streamlit](https://streamlit.io).

Organizada por niveles **A1 / A2 / B1**, cada uno con hasta 12 capítulos
de vocabulario en archivos YAML.

---

## 1. Estructura del proyecto

```
german-vocab-quiz/
├── app.py                 # Aplicación Streamlit
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── A1/
    │   └── Kapitel_01.yaml, Kapitel_02.yaml, ...
    ├── A2/
    │   └── Kapitel_01.yaml   ← ya incluido
    └── B1/
        └── Kapitel_01.yaml, ...
```

La app **lee automáticamente todos los `.yaml` que encuentre** dentro de
`data/<NIVEL>/`. No hay que tocar el código para añadir capítulos nuevos:
basta con subir el archivo a la carpeta correspondiente (ver sección 4).

---

## 2. Formato de los archivos YAML

Cada capítulo es un archivo independiente, por ejemplo `data/A2/Kapitel_02.yaml`:

```yaml
capitulo: 2

verbos:
  - aleman: "gehen (geht, ist gegangen)"
    espanol: "ir"
    tipo: "unregelmäßig"

sustantivos:
  - aleman: "Freund"
    espanol: "el amigo"
    genero: "der"
    plural: "-e"

adjetivos:
  - aleman: "groß"
    espanol: "grande"

adverbios:
  - aleman: "immer"
    espanol: "siempre"

preposiciones:
  - aleman: "mit (+ D.)"
    espanol: "con"

expresiones:
  - aleman: "Wie geht's?"
    espanol: "¿Qué tal?"
```

Categorías soportadas: `verbos`, `sustantivos`, `adjetivos`, `adverbios`,
`preposiciones`, `expresiones`. No es obligatorio incluir todas en cada
capítulo.

Para los **sustantivos**, si se indica `genero` (der/die/das), la app lo
muestra junto a la palabra en las opciones de respuesta (p. ej. `die Ausbildung`).

---

## 3. Ejecutar en local

```bash
git clone https://github.com/<tu-usuario>/german-vocab-quiz.git
cd german-vocab-quiz
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

---

## 4. Cómo añadir un capítulo nuevo

1. Crea un archivo YAML siguiendo el formato de la sección 2 (usa
   `data/A2/Kapitel_01.yaml` como plantilla).
2. Guárdalo en `data/<NIVEL>/Kapitel_<NN>.yaml`, por ejemplo:
   `data/A1/Kapitel_03.yaml`. El número de dos dígitos es solo por
   orden/legibilidad; lo que realmente identifica el capítulo dentro de
   la app es el campo `capitulo:` dentro del YAML.
3. Sube el archivo al repositorio (por la web de GitHub con
   "Add file → Upload files", o con git):

   ```bash
   git add data/A1/Kapitel_03.yaml
   git commit -m "Añadir A1 Kapitel 3"
   git push
   ```

4. Si la app ya está desplegada en Streamlit Cloud, se **actualiza sola**
   pocos segundos después del push (o usa "Rerun" en el menú de la app).

No hace falta modificar `app.py` para añadir vocabulario nuevo.

---

## 5. Subir el proyecto a GitHub (primera vez)

```bash
cd german-vocab-quiz
git init
git add .
git commit -m "Primera versión: Deutsch Quiz"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/german-vocab-quiz.git
git push -u origin main
```

Si prefieres no usar la terminal: entra en github.com → **New repository**
→ nómbralo `german-vocab-quiz` → **Create repository** → arrastra ahí
todos los archivos y carpetas de este proyecto con "Add file → Upload files".

---

## 6. Desplegar en Streamlit Community Cloud (gratis)

1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
   con tu cuenta de GitHub.
2. Pulsa **New app**.
3. Selecciona el repositorio `german-vocab-quiz`, la rama `main` y el
   archivo principal `app.py`.
4. Pulsa **Deploy**. En un par de minutos tendrás una URL pública
   (`https://<algo>.streamlit.app`) con tu app funcionando.
5. Cada vez que hagas `git push` con capítulos nuevos, la app se
   actualiza automáticamente.

---

## 7. Cómo funciona el quiz

- En la barra lateral eliges **nivel**, **capítulos** y **categorías**
  de vocabulario, y cuántas preguntas quieres.
- Para cada pregunta aparece la palabra en **español**, y 4 opciones en
  alemán (estilo Kahoot: 🔺🔷🟡🟩), una correcta y tres distractores
  tomados preferentemente de la misma categoría gramatical.
- Al responder se muestra si acertaste, se resalta la respuesta correcta,
  y puedes pasar a la siguiente pregunta.
- Al final se muestra el puntaje total y puedes repetir o cambiar la
  configuración.

---

## 8. Próximos pasos sugeridos

- Añadir más capítulos a `data/A1`, `data/A2`, `data/B1` hasta completar
  los 12 por nivel.
- Si en algún momento quieres también preguntas en la dirección
  Alemán → Español, o modo "escribir la respuesta" en vez de opción
  múltiple, se puede añadir como una opción más en la barra lateral sin
  tocar el formato de los YAML.
