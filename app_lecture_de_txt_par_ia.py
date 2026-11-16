# -*- coding: utf-8 -*-
"""Create MP3 speech with Windows voices or Microsoft Edge's online voices."""

import asyncio
import base64
import json
import queue
import subprocess
import tempfile
import threading
import tkinter as tk
import wave
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import edge_tts
import lameenc
import os
import sys

def resource_path(relative_path):
    """Obtient le chemin absolu vers la ressource, compatible mode dev et PyInstaller"""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class TextToSpeechApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Text to MP3")
        self.window.geometry("760x600")
        self.window.minsize(600, 480)
        self.window.configure(bg="#f3f6f3")
        self.window.iconbitmap(resource_path("v.ico"))

        self.events = queue.Queue()
        self.voice_options = {}
        self.voice_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Chargement des voix disponibles…")

        self._build_ui()
        self.window.after(100, self._process_events)
        self._start_voice_loading()

    def _build_ui(self):
        style = ttk.Style(self.window)
        style.configure("App.TFrame", background="#f3f6f3")
        style.configure(
            "Title.TLabel",
            background="#f3f6f3",
            foreground="#173b2b",
            font=("Arial", 23, "bold"),
        )
        style.configure(
            "Hint.TLabel",
            background="#f3f6f3",
            foreground="#52645a",
            font=("Arial", 10),
        )
        style.configure(
            "App.TLabel",
            background="#f3f6f3",
            foreground="#20342a",
            font=("Arial", 11, "bold"),
        )
        style.configure("Generate.TButton", font=("Arial", 11, "bold"), padding=9)

        content = ttk.Frame(self.window, style="App.TFrame", padding=28)
        content.pack(fill="both", expand=True)

        ttk.Label(content, text="Transformer un texte en MP3", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            content,
            text="Les voix hors ligne fonctionnent sans Internet. Les voix en ligne nécessitent une connexion.",
            style="Hint.TLabel",
            wraplength=680,
        ).pack(anchor="w", pady=(6, 22))

        ttk.Label(content, text="Votre texte", style="App.TLabel").pack(anchor="w")
        self.text_input = tk.Text(
            content,
            height=12,
            wrap="word",
            font=("Arial", 12),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=10,
        )
        self.text_input.pack(fill="both", expand=True, pady=(8, 18))

        ttk.Label(content, text="Voix", style="App.TLabel").pack(anchor="w")
        self.voice_picker = ttk.Combobox(
            content,
            textvariable=self.voice_var,
            state="disabled",
            height=12,
        )
        self.voice_picker.pack(fill="x", pady=(8, 18))

        self.generate_button = ttk.Button(
            content,
            text="Générer le MP3",
            style="Generate.TButton",
            command=self._generate_audio,
            state="disabled",
        )
        self.generate_button.pack(anchor="w")
        ttk.Label(
            content,
            textvariable=self.status_var,
            style="Hint.TLabel",
            wraplength=680,
        ).pack(anchor="w", pady=(14, 0))

    def _start_voice_loading(self):
        threading.Thread(target=self._load_local_voices, daemon=True).start()
        threading.Thread(target=self._load_online_voices, daemon=True).start()

    @staticmethod
    def _run_powershell(script):
        encoded_script = base64.b64encode(script.encode("utf-16le")).decode("ascii")
        return subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-EncodedCommand",
                encoded_script,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def _load_local_voices(self):
        script = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $voices = @($synth.GetInstalledVoices() | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.VoiceInfo.Name
            Culture = $_.VoiceInfo.Culture.Name
            Gender = $_.VoiceInfo.Gender.ToString()
        }
    })
    ConvertTo-Json -InputObject $voices -Compress
} finally {
    $synth.Dispose()
}
"""
        try:
            result = self._run_powershell(script)
            self.events.put(("local_voices", json.loads(result.stdout)))
        except Exception as exc:
            self.events.put(("local_error", f"Impossible de charger les voix Windows : {exc}"))

    def _load_online_voices(self):
        try:
            voices = asyncio.run(edge_tts.list_voices())
            self.events.put(("online_voices", voices))
        except Exception as exc:
            self.events.put(("online_error", f"Voix en ligne indisponibles : {exc}"))

    def _process_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "local_voices":
                    self._show_local_voices(payload)
                elif event == "online_voices":
                    self._show_online_voices(payload)
                elif event in ("local_error", "online_error"):
                    self.status_var.set(payload)
                    if event == "local_error" and not self.voice_options:
                        messagebox.showerror("Erreur", payload)
                elif event == "generated":
                    self.generate_button.configure(state="normal")
                    self.status_var.set(f"MP3 créé : {payload}")
                    messagebox.showinfo("MP3 créé", f"Votre fichier audio a été enregistré :\n{payload}")
                elif event == "error":
                    self.generate_button.configure(state="normal")
                    self.status_var.set(payload)
                    messagebox.showerror("Erreur", payload)
        except queue.Empty:
            pass
        self.window.after(100, self._process_events)

    def _refresh_voice_picker(self):
        current = self.voice_var.get()
        options = list(self.voice_options)
        self.voice_picker.configure(values=options)
        if options:
            self.voice_picker.configure(state="readonly")
            if current in self.voice_options:
                self.voice_var.set(current)
            else:
                preferred = next(
                    (
                        label
                        for label, voice in self.voice_options.items()
                        if voice == ("windows", "Microsoft Hortense Desktop")
                    ),
                    options[0],
                )
                self.voice_var.set(preferred)
            self.generate_button.configure(state="normal")

    def _show_local_voices(self, voices):
        if not voices:
            self.status_var.set("Aucune voix Windows installée.")
            return

        for voice in voices:
            name = voice["Name"]
            label = f'{name} — {voice["Culture"]} ({voice["Gender"]}, hors ligne)'
            self.voice_options[label] = ("windows", name)

        self._refresh_voice_picker()
        self.status_var.set(f"{len(voices)} voix Windows hors ligne disponibles.")

    def _show_online_voices(self, voices):
        for voice in sorted(voices, key=lambda item: (item["Locale"], item["FriendlyName"])):
            name = voice["ShortName"]
            label = f'{voice["FriendlyName"]} — {voice["Locale"]} ({voice["Gender"]}, en ligne)'
            self.voice_options[label] = ("edge", name)

        self._refresh_voice_picker()
        local_count = sum(1 for value in self.voice_options.values() if value[0] == "windows")
        self.status_var.set(f"{local_count} voix hors ligne et {len(voices)} voix en ligne disponibles.")

    def _generate_audio(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Texte manquant", "Écrivez un texte avant de générer le MP3.")
            return

        selected_voice = self.voice_options.get(self.voice_var.get())
        if not selected_voice:
            messagebox.showwarning("Voix manquante", "Sélectionnez une voix.")
            return
        engine, voice = selected_voice

        output_path = filedialog.asksaveasfilename(
            title="Enregistrer le fichier audio",
            defaultextension=".mp3",
            filetypes=[("Fichier audio MP3", "*.mp3")],
            initialfile="audio.mp3",
        )
        if not output_path:
            return

        self.generate_button.configure(state="disabled")
        self.status_var.set("Génération de l’audio en cours…")
        save_method = self._save_local_audio if engine == "windows" else self._save_audio
        threading.Thread(
            target=save_method,
            args=(text, voice, output_path),
            daemon=True,
        ).start()

    def _save_audio(self, text, voice, output_path):
        try:
            asyncio.run(edge_tts.Communicate(text, voice).save(output_path))
            self.events.put(("generated", output_path))
        except Exception as exc:
            self.events.put(("error", f"Échec de la génération du MP3 : {exc}"))

    def _save_local_audio(self, text, voice, output_path):
        wav_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
                wav_path = wav_file.name

            encoded_values = [
                base64.b64encode(value.encode("utf-8")).decode("ascii")
                for value in (voice, text, wav_path)
            ]
            voice_b64, text_b64, path_b64 = encoded_values
            script = f"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$utf8 = [System.Text.Encoding]::UTF8
$voice = $utf8.GetString([Convert]::FromBase64String('{voice_b64}'))
$text = $utf8.GetString([Convert]::FromBase64String('{text_b64}'))
$path = $utf8.GetString([Convert]::FromBase64String('{path_b64}'))
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {{
    $synth.SelectVoice($voice)
    $synth.SetOutputToWaveFile($path)
    $synth.Speak($text)
}} finally {{
    $synth.Dispose()
}}
"""
            self._run_powershell(script)

            with wave.open(wav_path, "rb") as wav_file:
                if wav_file.getsampwidth() != 2:
                    raise ValueError("La voix Windows n’a pas produit un audio PCM 16 bits.")
                channels = wav_file.getnchannels()
                if channels not in (1, 2):
                    raise ValueError(f"Nombre de canaux audio non pris en charge : {channels}.")
                encoder = lameenc.Encoder()
                encoder.set_in_sample_rate(wav_file.getframerate())
                encoder.set_channels(channels)
                encoder.set_bit_rate(128)
                encoder.set_quality(2)
                audio_data = wav_file.readframes(wav_file.getnframes())

            with open(output_path, "wb") as mp3_file:
                mp3_file.write(encoder.encode(audio_data))
                mp3_file.write(encoder.flush())
            self.events.put(("generated", output_path))
        except Exception as exc:
            self.events.put(("error", f"Échec de la génération MP3 hors ligne : {exc}"))
        finally:
            if wav_path and Path(wav_path).exists():
                Path(wav_path).unlink()


if __name__ == "__main__":
    root = tk.Tk()
    TextToSpeechApp(root)
    root.mainloop()
