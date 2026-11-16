import asyncio
import edge_tts

TEXTE = "Alerte ! Le niveau d'eau est bas !"
VOIX = "fr-FR-DeniseNeural"
FICHIER_SORTIE = "alarme_vide.mp3"

async def generer_alarme():
    communicate = edge_tts.Communicate(TEXTE, VOIX)
    await communicate.save(FICHIER_SORTIE)
    print(f"🎯 L'IA a généré votre alarme vocale avec succès sous le nom '{FICHIER_SORTIE}' !")

# Lancement de la génération
if __name__ == "__main__":
    asyncio.run(generer_alarme())