🛡️ Phishing HTML JavaScript Desbfuscator

<img width="493" height="416" alt="imagen" src="https://github.com/user-attachments/assets/cb566688-9dfa-4830-9455-b14114d9e42f" />


Este repositorio contiene un script en Python para desofuscar código JavaScript malicioso ofuscado, comúnmente utilizado en ataques de phishing. Está diseñado para campañas que usan archivos HTML con objetos de mapeo numérico (como el objeto dpsh).
🔍 Descripción

En un análisis reciente de phishing distribuido vía WhatsApp, se detectó un archivo HTML altamente ofuscado que generaba contenido fraudulento simulando una actualización oficial de Adobe Acrobat Reader. Este contenido soporta múltiples idiomas, realiza redirecciones maliciosas y utiliza plataformas legítimas como Google Drive para alojar documentos falsos.

El script permite interpretar y recuperar el código original, convirtiendo valores codificados en Unicode a texto legible, facilitando análisis forense y detección.
⚙️ Uso

   Clonar este repositorio.

   Colocar el archivo HTML ofuscado en la carpeta raíz (o especificar la ruta en el comando).

   Ejecutar el script:

    python desofusk.py archivo_ofuscado.html

  Revisar el archivo desofuscado generado para análisis.

✨ Beneficios

  Simplifica análisis manual complejo.

  Mejora la efectividad en detección y respuesta ante phishing.

  Facilita la generación de indicadores de compromiso (IoCs).

⚠️ Disclaimer

Este código es para fines educativos y de análisis únicamente. El autor no se responsabiliza por usos indebidos.

📁 Ejemplo Visual

Ejecuccion del Script: 

<img width="446" height="158" alt="imagen" src="https://github.com/user-attachments/assets/5bc42f00-06b5-4883-96fa-22aa3c621cca" />


HTML ofuscado:

<img width="750" height="789" alt="imagen" src="https://github.com/user-attachments/assets/a0840b86-bd26-4ad0-96d0-adfeb01c61ad" />

HTML deobfuscado:

<img width="1176" height="711" alt="imagen" src="https://github.com/user-attachments/assets/0dc1756c-c1f1-4340-8b3d-197e132cd8f3" />
