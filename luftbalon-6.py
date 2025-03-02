import os
import base64
import zlib

# /by Alan
# created for/by Fragment-6


# Unterstützte Dateiarten
COVER_FILE_TYPES = [".png", ".jpg", ".pdf", ".docx"]
HIDDEN_FILE_TYPES = [".txt", ".jpg", ".png"]

# ASCII-Logo für den Startbildschirm
def print_ascii_art():
    ascii_art = """
  █████▒██▓ ███▄    █   ▄████   ████▄    █ 
▓██   ▒▓██▒ ██ ▀█   █  ██▒ ▀█▒  ██ ▀█   █ 
▒████ ░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░ ▓██  ▀█ ██▒
░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█  ██▓ ▓██▒  ▐▌██▒
░▒█░   ░██░▒██░   ▓██░░▒▓███▀▒ ▒██░   ▓██░
 ▒ ░   ░▓  ░ ▒░   ▒ ▒  ░▒   ▒  ░ ▒░   ▒ ▒ 
 ░      ▒ ░░ ░░   ░ ▒░  ░   ░  ░ ░░   ░ ▒░
 ░ ░    ▒ ░   ░   ░ ░ ░ ░   ░     ░   ░ ░ 
        ░           ░       ░           ░ 
    """
    print(ascii_art)

# Hauptmenü
def main_menu():
    print("Willkommen zu Fragment-6!")
    print("1: Daten in Datei einbetten")
    print("2: Daten aus Datei extrahieren")
    choice = input("Wähle eine Option (1/2): ").strip()
    return choice

# Funktion zur Auswahl der Trägerdatei (wo die Daten versteckt werden)
def choose_cover_file():
    print("\nWähle eine Dateiart für die Trägerdatei:")
    for i, ext in enumerate(COVER_FILE_TYPES, 1):
        print(f"{i}: {ext}")

    while True:
        choice = input("Gib die Zahl ein: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(COVER_FILE_TYPES):
            cover_ext = COVER_FILE_TYPES[int(choice) - 1]
            break
        print("Ungültige Eingabe. Bitte eine Zahl aus der Liste wählen.")

    # Dateien dieses Typs im aktuellen Verzeichnis suchen
    available_files = [f for f in os.listdir() if f.endswith(cover_ext)]

    if not available_files:
        print(f"Keine {cover_ext}-Dateien gefunden. Bitte manuell eingeben.")
        file_path = input("Pfad zur Trägerdatei: ").strip()
    else:
        print("\nVerfügbare Dateien:")
        for i, filename in enumerate(available_files, 1):
            print(f"{i}: {filename}")

        while True:
            file_choice = input("Datei wählen oder eigenen Pfad eingeben: ").strip()
            if file_choice.isdigit() and 1 <= int(file_choice) <= len(available_files):
                file_path = available_files[int(file_choice) - 1]
                break
            elif os.path.exists(file_choice):
                file_path = file_choice
                break
            print("Ungültige Eingabe. Wähle eine Zahl oder gib einen gültigen Pfad an.")

    print(f"Trägerdatei gewählt: {file_path}")
    return file_path

# Funktion zur Auswahl der versteckten Datei
def choose_hidden_file():
    print("\nWähle eine Dateiart für die zu schmuggelnde Datei:")
    for i, ext in enumerate(HIDDEN_FILE_TYPES, 1):
        print(f"{i}: {ext}")

    while True:
        choice = input("Gib die Zahl ein: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(HIDDEN_FILE_TYPES):
            hidden_ext = HIDDEN_FILE_TYPES[int(choice) - 1]
            break
        print("Ungültige Eingabe. Bitte eine Zahl aus der Liste wählen.")

    # Dateien dieses Typs im aktuellen Verzeichnis suchen
    available_files = [f for f in os.listdir() if f.endswith(hidden_ext)]

    if not available_files:
        print(f"Keine {hidden_ext}-Dateien gefunden. Bitte manuell eingeben.")
        file_path = input("Pfad zur zu versteckenden Datei: ").strip()
    else:
        print("\nVerfügbare Dateien:")
        for i, filename in enumerate(available_files, 1):
            print(f"{i}: {filename}")

        while True:
            file_choice = input("Datei wählen oder eigenen Pfad eingeben: ").strip()
            if file_choice.isdigit() and 1 <= int(file_choice) <= len(available_files):
                file_path = available_files[int(file_choice) - 1]
                break
            elif os.path.exists(file_choice):
                file_path = file_choice
                break
            print("Ungültige Eingabe. Wähle eine Zahl oder gib einen gültigen Pfad an.")

    print(f"Zu versteckende Datei gewählt: {file_path}")
    return file_path

# Funktion zum Einbetten der Daten
def embed_data(cover_file, hidden_file):
    with open(hidden_file, "rb") as f:
        hidden_data = f.read()

    compressed_data = zlib.compress(hidden_data)  # Komprimieren
    encoded_data = base64.b64encode(compressed_data).decode()  # Base64-Codieren
    marker = "###HIDDEN_DATA###"  # Erkennungsmarkierung

    with open(cover_file, "rb") as f:
        cover_data = f.read()

    new_file = f"hidden_{cover_file}"
    with open(new_file, "wb") as f:
        f.write(cover_data + marker.encode() + encoded_data.encode())

    print(f"Daten erfolgreich in {new_file} versteckt!")

# Funktion zum Extrahieren der Daten
def extract_data(cover_file):
    marker = "###HIDDEN_DATA###"

    with open(cover_file, "rb") as f:
        content = f.read().decode(errors="ignore")

    if marker in content:
        encoded_data = content.split(marker)[-1]
        compressed_data = base64.b64decode(encoded_data)
        hidden_data = zlib.decompress(compressed_data)

        output_file = "extracted_data"
        with open(output_file, "wb") as f:
            f.write(hidden_data)

        print(f"Versteckte Daten extrahiert und in {output_file} gespeichert!")
    else:
        print("Keine versteckten Daten gefunden.")

# Hauptprogramm
if __name__ == "__main__":
    print_ascii_art()
    choice = main_menu()
    
    if choice == "1":
        print("Option 1 gewählt: Daten einbetten")
        cover_file = choose_cover_file()
        hidden_file = choose_hidden_file()
        embed_data(cover_file, hidden_file)

    elif choice == "2":
        print("Option 2 gewählt: Daten extrahieren")
        cover_file = input("Pfad zur Datei mit versteckten Daten: ").strip()
        extract_data(cover_file)
    
    else:
        print("Ungültige Auswahl. Bitte starte das Programm neu.")