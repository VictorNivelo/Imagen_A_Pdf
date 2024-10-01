# Convertidor de Imágenes a PDF

## Descripción

El Convertidor de Imágenes a PDF es una aplicación de escritorio fácil de usar, construida con PyQt5, que permite a los usuarios convertir múltiples imágenes en un solo archivo PDF. Esta herramienta ofrece varias opciones de personalización y una interfaz elegante para un proceso de conversión eficiente.

## Características

- Selección de múltiples imágenes para la conversión
- Elección entre varios tamaños de página (A5, A4, Carta, Legal) o mantener el tamaño original de la imagen
- Nombrado personalizado para los archivos PDF de salida
- Cambio entre modo oscuro y claro
- Barra de progreso para seguimiento de la conversión
- Vista previa de las imágenes seleccionadas antes de la conversión
- Directorios predeterminados configurables para imágenes de entrada y PDF de salida
- Opción para abrir la carpeta que contiene el PDF generado después de la conversión

## Requisitos

- Python 3.x
- PyQt5
- Pillow (PIL)

## Uso

1. Ejecute la aplicación:
2. Utilice el botón "Seleccionar Imágenes" para elegir las imágenes que desea convertir.
3. (Opcional) Seleccione un tamaño de página del menú desplegable.
4. Ingrese un nombre para su archivo PDF de salida.
5. Haga clic en "Convertir a PDF" para generar su PDF.
6. La aplicación le solicitará que elija una ubicación para guardar el PDF.
7. Después de la conversión, tendrá la opción de abrir la carpeta que contiene el nuevo PDF.

## Configuración

La aplicación guarda las preferencias del usuario en un archivo `configuracion.txt`, que incluye:
- Directorio de entrada predeterminado para imágenes
- Directorio de salida predeterminado para PDF
- Preferencia de tema de la interfaz de usuario (Oscuro/Claro)

Estas configuraciones se pueden modificar a través del menú "Opciones" en la aplicación.

## Contribuciones

Las contribuciones, problemas y solicitudes de funciones son bienvenidas. No dude en consultar la página de problemas si desea contribuir.

## Funcionamiento Detallado

1. **Selección de Imágenes**: 
   - Al hacer clic en "Seleccionar Imágenes", se abre un diálogo de selección de archivos.
   - Las imágenes seleccionadas se muestran en una vista previa en la interfaz.

2. **Configuración de Salida**:
   - El usuario puede elegir el tamaño de página del PDF resultante.
   - Se puede especificar un nombre personalizado para el archivo PDF.

3. **Proceso de Conversión**:
   - Al hacer clic en "Convertir a PDF", se inicia el proceso de conversión.
   - Una barra de progreso muestra el avance de la conversión.
   - Las imágenes se procesan y se ajustan según el tamaño de página seleccionado.

4. **Guardado y Finalización**:
   - El usuario elige la ubicación para guardar el PDF.
   - Una vez completado, se muestra un mensaje de éxito.
   - Se ofrece la opción de abrir la carpeta que contiene el PDF generado.

5. **Personalización y Configuración**:
   - El menú "Opciones" permite al usuario:
     - Seleccionar carpetas predeterminadas para imágenes y PDFs.
     - Cambiar entre modo claro y oscuro.
   - Las preferencias se guardan automáticamente en `configuracion.txt`.

## Notas Adicionales

- La aplicación utiliza PyQt5 para la interfaz gráfica, proporcionando una experiencia de usuario moderna y responsive.
- El procesamiento de imágenes se realiza utilizando la biblioteca Pillow (PIL), permitiendo un manejo eficiente de diferentes formatos de imagen.
- La aplicación está diseñada para ser intuitiva y fácil de usar, con mensajes claros y opciones de personalización accesibles.