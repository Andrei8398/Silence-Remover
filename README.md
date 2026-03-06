# ✂️ Silence Remover

A lightweight, portable Python GUI application that effortlessly removes "dead air" (silence) from the beginning and end of your audio files. 

Under the hood, it acts as a graphical wrapper for the powerful FFmpeg engine, allowing users to process audio files without touching the command line.

## ✨ Features
* **Simple GUI:** Easy-to-use interface built with `tkinter`.
* **Smart Format Handling:** Automatically saves the output in the same format as the input.
* **Zero Quality Loss for Lossless:** Perfect 1-to-1 conversion for FLAC and WAV files.
* **Pro-Quality Lossy Output:** Automatically forces a high-quality 320kbps bitrate when processing MP3, OGG, or AAC files to prevent noticeable generation loss.
* **Dynamic Trimming:** Choose to trim the start, the end, or both simultaneously.

## ⚙️ Requirements & Installation
Because FFmpeg is subject to its own open-source licenses, it is not bundled directly in this repository. To use this application, you need to provide the engine:

1. Download **Python 3** if you want to run the script directly.
2. Download the latest `ffmpeg.exe` build from the [official FFmpeg website](https://ffmpeg.org/download.html) (or gyan.dev for Windows).
3. Place `ffmpeg.exe` in the **exact same folder** as `SilenceRemover.pyw`.
4. Run the Python script (or compile it to an `.exe` using PyInstaller).

## 🚀 How to Use
1. Open the application.
2. Click **Browse File** and select your audio file.
3. The destination file will automatically be generated with a `_cleaned` suffix. You can change this by clicking **Save As...**.
4. Check the boxes for where you want the silence removed (Beginning, End, or both).
5. Click **CLEAN AUDIO** and wait for the success message!

---
*Created as a utility tool for fast, reliable audio processing.*
