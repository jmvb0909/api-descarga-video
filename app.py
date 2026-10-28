from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/descargar', methods=['POST'])
def descargar_video():
    # 1. El atajo del iPhone envía el enlace por JSON
    datos = request.get_json()
    url = datos.get('url')
    
    if not url:
        return {"error": "No se proporcionó URL"}, 400

    # 2. Generamos un nombre de archivo temporal único
    nombre_archivo = f"/tmp/{uuid.uuid4()}.mp4"

    # 3. Configuramos yt-dlp para extraer la mejor calidad en mp4
    opciones = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': nombre_archivo,
        'quiet': True,
        'no_warnings': True
    }

    try:
        # 4. Descargamos el video
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
            
        # 5. Se lo enviamos de vuelta al iPhone
        return send_file(nombre_archivo, as_attachment=True)
        
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        # Limpieza de memoria (borramos el video del servidor tras enviarlo)
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
