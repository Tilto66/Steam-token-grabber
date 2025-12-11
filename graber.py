import os
import re

# Chemin absolu vers le fichier de configuration de Steam
config_path = r'C:\Program Files (x86)\steam\config\loginusers.vdf'

# Ouvrir le fichier de sortie
with open('steam_token.txt', 'w', encoding='utf-8') as output_file:
    # Afficher le chemin pour vérification
    output_file.write(f"Chemin du fichier de configuration Steam: {config_path}\n\n")
    print(f"Chemin du fichier de configuration Steam: {config_path}")

    # Vérifier si le fichier existe
    if not os.path.exists(config_path):
        message = f"Erreur: Le fichier {config_path} n'existe pas."
        output_file.write(message + "\n")
        print(message)
    else:
        # Lire le contenu du fichier directement avec Python
        try:
            with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            message = f"Erreur: Impossible de lire le fichier. {e}"
            output_file.write(message + "\n")
            print(message)
            exit(1)

        # Afficher le contenu pour debug
        output_file.write("\n=== CONTENU DU FICHIER ===\n")
        output_file.write(content)
        output_file.write("\n=== FIN DU CONTENU ===\n\n")
        
        print("\n=== CONTENU DU FICHIER ===")
        print(content)
        print("=== FIN DU CONTENU ===\n")

        # Extraire toutes les paires clé-valeur
        all_matches = re.findall(r'"([^"]+)"\s+"([^"]*)"', content)
        
        output_file.write("=== TOUTES LES CLÉS TROUVÉES ===\n")
        print("=== TOUTES LES CLÉS TROUVÉES ===")
        for key, value in all_matches:
            line = f"{key}: {value}\n"
            output_file.write(line)
            print(f"{key}: {value}")
        output_file.write("=== FIN DES CLÉS ===\n\n")
        print("=== FIN DES CLÉS ===\n")

        # Rechercher différentes variantes possibles
        token_match = re.search(r'"(?:AuthTicket|WGToken|RememberPassword)"\s*"(.*?)"', content, re.IGNORECASE)
        username_match = re.search(r'"(?:AccountName|PersonaName)"\s*"(.*?)"', content, re.IGNORECASE)
        steamid_match = re.search(r'"(\d{17})"', content)  # Steam ID est un nombre de 17 chiffres

        output_file.write("=== RÉSULTATS DE LA RECHERCHE ===\n")
        print("=== RÉSULTATS DE LA RECHERCHE ===")
        
        if username_match:
            username = username_match.group(1)
            line = f"✓ Utilisateur trouvé: {username}\n"
            output_file.write(line)
            print(line.strip())
        else:
            line = "✗ Aucun nom d'utilisateur trouvé\n"
            output_file.write(line)
            print(line.strip())
            username = None

        if token_match:
            token = token_match.group(1)
            line = f"✓ Jeton trouvé: {token}\n"
            output_file.write(line)
            print(line.strip())
        else:
            line = "✗ Aucun jeton d'authentification trouvé\n"
            output_file.write(line)
            print(line.strip())
            token = None

        if steamid_match:
            steamid = steamid_match.group(1)
            line = f"✓ Steam ID trouvé: {steamid}\n"
            output_file.write(line)
            print(line.strip())
        else:
            line = "✗ Aucun Steam ID trouvé\n"
            output_file.write(line)
            print(line.strip())
            steamid = None

        output_file.write("=== FIN DES RÉSULTATS ===\n\n")

        # Message final
        if username or token or steamid:
            final_message = "\n✓ Toutes les informations ont été sauvegardées dans steam_token.txt\n"
            output_file.write(final_message)
            print(final_message)
        else:
            final_message = "\n✗ Aucune information exploitable trouvée\n"
            output_file.write(final_message)
            print(final_message)