# 💻 Yuuruii Technical Support (YTS)

## 🌟 Resumen del Proyecto

Yuuruii Technical Support (YTS) es una **herramienta de soporte técnico de escritorio compacta y eficiente**, diseñada para facilitar la comunicación del estado y las acciones realizadas por el técnico al cliente. Su función principal es mostrar el registro de cambios (**Changelog**) de las tareas de reparación y optimización realizadas, utilizando un sistema de resaltado de color intuitivo para clasificar las acciones.

La aplicación está construida con **Python** y la librería **CustomTkinter**, asegurando una interfaz moderna, limpia y compacta, optimizada para **laptops** y pantallas de baja resolución (480x500px).

| Característica | Detalle |
| :--- | :--- |
| **Plataformas** | Windows, macOS, Linux (compilado vía PyInstaller). |
| **Tecnología** | Python, CustomTkinter (interfaz moderna y oscura). |
| **Función Principal** | Visualización y edición segura de un archivo `changelog.md` centralizado. |
| **Optimización** | Interfaz ajustada a dimensiones **compactas** para evitar el desborde en laptops. |

---

## 🚀 Características Principales

* **Resaltado Inteligente del Changelog:** Utiliza un sistema de *tags* de color para identificar rápidamente el tipo de trabajo realizado (p. ej., optimización, reparación, reemplazo, menciones al S.O.).
* **Diseño Compacto y Oscuro:** Interfaz moderna (tema Drácula) optimizada para resoluciones limitadas (480x500px).
* **Ubicación Centralizada:** El archivo de registro se almacena en `[Su_Usuario]/Documentos/YTS/changelog.md` para un acceso rápido y predecible.
* **Modo de Desarrollo Oculto (TS Tools):**
    * Permite a los técnicos autorizados (vía clave secreta) editar y guardar el `changelog.md`.
    * Ofrece la opción de aplicar automáticamente un fondo de pantalla de soporte post-servicio (función activa en Windows).
* **Sistema de Carga (Splash Screen):** Ofrece una experiencia de carga profesional antes de iniciar la aplicación principal.

---

## 🛠️ Instalación y Uso

### Ejecución

1. Descargue el archivo ejecutable (`app.exe` o `app` binario) desde el directorio de distribución (`dist/`).
2. Ejecute el archivo.

### Acceso al Changelog

El archivo de registro de cambios del servicio se encuentra en la ruta centralizada del sistema:
  [Su_Usuario]/Documentos/YTS/changelog.md

### Modo de Desarrollo (TS Tools)

El acceso a las herramientas del técnico está oculto en la interfaz principal.

1. Haga clic discretamente en la etiqueta **`YRZ OPTIONS`** en la parte inferior de la ventana principal.
2. Ingrese la clave de desarrollador (Developer Key): **`Yuuruii-TS-D3v_K3y-2025`**.

---

## 🎨 Paleta de Colores y Resaltado

El código utiliza la paleta de colores de **Drácula** para el resaltado visual del texto en el Changelog:

| Tipo de Acción | Color | Código |
| :--- | :--- | :--- |
| **Optimización/Actualización** | Verde | `#50fa7b` |
| **Reemplazo/Formateo** | Rojo | `#ff5555` |
| **Reparación** | Naranja | `#ffb86c` |
| **S.O. (Palabra clave)** | Cyan | `#8be9fd` |
| **Flechas (`->`)** | Púrpura | `#DA9CFF` |

---

## 🤖 Asistencia de Inteligencia Artificial

Este proyecto, incluyendo su arquitectura, soluciones para bugs de interfaz (como el problema de los iconos y la optimización de tamaño para laptops) y la generación de este archivo `README.md`, fue desarrollado con la asistencia de **Gemini, un modelo de lenguaje de gran tamaño entrenado por Google**.

---

## 📝 Licencia

Este proyecto es de código abierto y distribuido bajo la licencia **MIT**.

---

<p align="center">
  Hecho con ❤️ por Yuuruii.
</p>
