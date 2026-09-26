# VoiceAI — Emo Voice Assistant

**Emo** is a desktop voice assistant written in Python. It listens to your microphone, understands what you say, speaks its reply out loud, and can control your PC, fetch live information from the internet, or answer open-ended questions using a locally running **Ollama** LLM.

It runs **100% offline for the AI part** — your questions never leave your machine. Only speech recognition (Google) and the weather/joke APIs need an internet connection.

```
You:  "what is the weather in Kolkata"
Emo:  "The temperature in kolkata is 31 degree Celsius"
      "Weather condition is Partly cloudy"
      "Humadity is 74 percent"
```

> **Platform:** Windows only. Commands like `start`, `winword`, `msedge`, `calc` and window-title matching via `pygetwindow` are Windows-specific.

---

## Features

| Area | What Emo can do |
| --- | --- |
| **Voice I/O** | Text-to-speech via `pyttsx3`, speech-to-text via Google Speech Recognition (`en-IN`) |
| **AI chat** | Any unrecognised question is answered by a local `llama3.2:3b` model through Ollama |
| **Weather** | Live temperature, condition and humidity for any city (wttr.in) |
| **Jokes** | Random setup + punchline (official-joke-api) |
| **System info** | Battery percentage and charging status |
| **Time & date** | Current time, full date, and day of the week |
| **Web search** | "search for …" opens Google results in Chrome |
| **Media** | "play …" opens YouTube search results |
| **App control** | Open Notepad, Calculator, Word, Excel, Paint, Edge, WhatsApp, VS Code |
| **Math** | Spoken arithmetic (plus / minus / multiply / divide) |
| **Close apps** | Closes a running window by matching its title |

---

## Voice Command Reference

### Small talk

| You say | Emo replies |
| --- | --- |
| `hi` / `hello` / `hey` | Hello! Nice to talk to you |
| `how are you` | I am doing great. Thank you for asking! |
| `what is your name` | My name is Emo |

### Information

| You say | Emo does |
| --- | --- |
| `weather in <city>` | Speaks temperature, condition and humidity |
| `check the weather in <city>` | Same as above (many phrasings accepted) |
| `tell me a joke` | Tells a random joke |
| `battery` | Speaks battery percentage + charging status |
| `time` | Speaks current time **and** today's date |
| `what day is it` | Speaks the day of the week |

### Actions

| You say | Emo does |
| --- | --- |
| `search for <query>` | Opens Google search results in Chrome |
| `play <song>` | Opens YouTube search results for the song |
| `open youtube` | Opens youtube.com |
| `open google` | Opens google.com |
| `open notepad` | Launches Notepad |
| `open calculator` | Launches Calculator |
| `open word` / `open microsoft word` | Launches Microsoft Word |
| `open excel` / `open microsoft excel` | Launches Microsoft Excel |
| `open paint` | Launches MS Paint |
| `open edge` / `open microsoft edge` | Launches Microsoft Edge |
| `open whatsapp` | Launches WhatsApp |
| `open code` | Launches VS Code |
| `calculate 5 plus 3` | Speaks "The answer is 8" |
| `calculate 10 divide 2` | Speaks "The answer is 5" |
| `close edge` | Closes the window whose title contains "edge" |
| `stop` / `exit` / `bye` / `goodbye` | Emo says goodbye and the program exits |

### Anything else

Any sentence that does not match the commands above is sent to your local LLM:

```
You:  "explain recursion in one line"
Emo:  "Recursion is a function calling itself until it reaches a base case."
```
---

## Requirements

| Requirement | Notes |
| --- | --- |
| **Windows 10 / 11** | Uses `cmd /c start`, `winword`, `msedge`, `calc`, and `pygetwindow` |
| **Python 3.10+** | Developed and tested on **Python 3.12.10** |
| **A working microphone** | Required — Emo is voice-driven |
| **Speakers / headphones** | Required for the spoken replies |
| **Internet connection** | Needed for speech recognition, weather, and jokes |
| **Ollama** | For the AI fallback (local, free, no API key) |
| **Google Chrome** | The browser is hard-coded to `chrome` for search / YouTube / "play" |

### Python packages

All six direct dependencies are pinned in [`requirements.txt`](requirements.txt):

| Package | Version | Used for |
| --- | --- | --- |
| `pyttsx3` | 2.99 | Offline text-to-speech |
| `SpeechRecognition` | 3.17.0 | Microphone capture + Google STT |
| `PyAudio` | 0.2.14 | Microphone audio stream backend |
| `requests` | 2.34.2 | Ollama / weather / joke HTTP calls |
| `psutil` | 7.2.2 | Battery information |
| `PyGetWindow` | 0.0.9 | Listing and closing windows |

> `pyttsx3` automatically pulls in `pywin32` and `comtypes` on Windows, so no manual install is needed.

---

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/RitamNaskar11/Voice_Assistant.git
cd Voice_Assistant
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, allow it for the current session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

*(Using `cmd.exe` instead? Run `venv\Scripts\activate.bat`.)*

### 3. Install the dependencies

```powershell
pip install -r requirements.txt
```

---

## Set Up Ollama (the AI brain)

Emo's open-ended answers come from a **local** LLM. Without Ollama running, everything else still works — Emo just replies *"Sorry, I cannot connect to my AI brain right now."*

1. Download and install Ollama for Windows: <https://ollama.com/download>
2. Pull the model Emo expects (`llama3.2:3b`):

   ```powershell
   ollama pull llama3.2:3b
   ```

3. Make sure the Ollama server is running. Installing the desktop app normally starts it automatically; otherwise run:

   ```powershell
   ollama serve
   ```

4. Confirm it works before starting Emo:

   ```powershell
   python test_ollama.py
   ```

   You should see a plain-text explanation of Python printed to the console. If you get a `ConnectionError`, the Ollama server is not running on port `11434`.

> **Port note:** `main.py` talks to `http://127.0.0.1:11434/api/generate` and `test_ollama.py` uses `http://localhost:11434/api/generate`. Both point at the same local Ollama server, so the default configuration works out of the box.

---

## Usage

With the virtual environment activated:

```powershell
python main.py
```

Emo greets you with **"Hello!"**, then starts listening. The console shows what it heard and what it is about to say:

```
Emo: Hello!
Listening
Recognizing
You: open notepad
Emo: Opening Notepad
Listening
```

Speak clearly, and allow ~1 second of silence after each command so the recognizer knows you have finished. Exit by saying **"stop"**, **"exit"**, **"bye"**, or **"goodbye"** — or press `Ctrl + C`.


---

## Project Structure

```
VoiceAI/
├── main.py            # The entire assistant — listen loop + every command
├── test_ollama.py     # Standalone check that your local Ollama server responds
├── requirements.txt   # Pinned Python dependencies
├── README.md          # This file
├── .gitignore         # Excludes venv/, __pycache__/ and .env
└── venv/              # Your virtual environment (not committed)
```

`main.py` is a single script. It defines:

| Function | Purpose |
| --- | --- |
| `speak(text)` | Prints and speaks a reply via `pyttsx3` |
| `listen()` | Records from the mic and returns the recognised text (lower-cased) |
| `ask_ai(query)` | Sends the prompt to Ollama and returns the model's answer |
| `tell_joke()` | Fetches a random joke |
| `get_weather(city)` | Fetches current conditions from wttr.in |
| `bettery_check()` | Reports battery level and charging state |
| `close_app(app_name)` | Closes windows whose title matches `app_name` |

Below those, a `while True:` loop routes each recognised phrase to the right handler.

---

## Configuration

Everything is tunable near the top of `main.py`:

| Setting | Line | Current value |
| --- | --- | --- |
| Voice speed | `main.py:13` | `engine.setProperty("rate", 140)` |
| Speech language | `main.py:85` | `"en-IN"` (change to `"en-US"`, `"en-GB"`, etc.) |
| Listen timeout / phrase limit | `main.py:81` | `timeout=5`, `phrase_time_limit=5` seconds |
| Ollama endpoint | `main.py:39` | `http://127.0.0.1:11434/api/generate` |
| AI model | `main.py:41` | `"llama3.2:3b"` |
| Max answer length | `main.py:45` | `"num_predict": 120` tokens |
| Persona / system prompt | `main.py:35-36` | `"You are Emo, a fast voice assistant…"` |

**Example — a faster, more accurate listener:** lower `phrase_time_limit` for snappier commands, or raise it if Emo keeps cutting you off mid-sentence.

**Example — swap the model:** run `ollama pull llama3.1:8b`, then change `main.py:41` to `"llama3.1:8b"`.

---

## Troubleshooting

| Symptom | Cause & fix |
| --- | --- |
| `OSError: [Errno -9996] Invalid input device` or `no default input device` | No usable microphone. Plug one in and set it as the **default recording device** in Windows Sound settings. |
| `Could not find PyAudio; check installation` | Run `pip install PyAudio`. If the build fails, upgrade pip first (`python -m pip install --upgrade pip`) or use `pipwin install pyaudio`. |
| `Sorry, I cannot connect to my AI brain right now.` | Ollama isn't reachable. Start it with `ollama serve` and verify `python test_ollama.py` works. |
| Model errors such as `model "llama3.2:3b" not found` | You haven't downloaded the model: `ollama pull llama3.2:3b`. |
| `No speech detected.` every time | You are speaking too late or too quietly. Speak within ~5 seconds of `Listening`, and raise the `timeout` at `main.py:81`. |
| `Sorry, I did not understand that.` | Background noise, mumbling, or a very strong accent. Wait for the ambient-noise calibration (the short pause after `Listening`) to finish. |
| `Please check your internet connection.` | Google Speech Recognition is online-only — check your network. |
| Chrome never opens | Chrome is hard-coded. Install Chrome, or replace `"chrome"` with `"msedge"` in the `subprocess.Popen` calls. |
| `Sorry I didn't find it <app>` | Apps must exist in the `apps` dictionary (`main.py:328-338`). Add your own entry there. |
| Weather says it can't fetch data | Use a plain city name, e.g. `weather in London`, and check your internet connection. |
| Emo speaks but you hear nothing | `pyttsx3` uses the Windows default output device — check your volume/output device. |


---

## Known Limitations

- **Windows only.** The app-launching and window-closing logic relies on Windows commands and `pygetwindow`.
- **Internet required for speech recognition.** Google's Web Speech API is used, so there is no offline STT. The AI part, however, is fully local.
- **Chrome is hard-coded.** "search for", "open youtube/google" and "play" all launch `chrome`.
- **No wake word.** Emo listens continuously in a loop; it does not wait for a keyword such as "Hey Emo".
- **Limited app list.** Only Notepad, Calculator, Word, Excel, Paint, Edge, WhatsApp and VS Code are mapped. Unknown names produce *"Sorry I didn't find it `<name>`"*.
- **Basic speech-error correction.** Only a few recognition mistakes are aliased (e.g. `age` / `this` → `edge`). Other mis-hearings fall through to the AI.
- **Exact small-talk matching.** `hi`, `hello`, `hey` and `how are you` must be said on their own; extra words route the phrase to the LLM instead.
- **Battery value is spoken verbatim.** `psutil` returns a float, so you may hear *"85.0 percent"* instead of *"85 percent"*.
- **No microphone error guard.** If the microphone is unavailable, `listen()` has no catch-all handler and the script can exit with a traceback.
- **Answers are capped** at roughly 120 tokens (`num_predict`) to keep replies short.

---

## Credits

| Component | Provider |
| --- | --- |
| Large language model | [Ollama](https://ollama.com) + Meta `llama3.2:3b` |
| Speech recognition | Google Web Speech API via [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) |
| Text-to-speech | [pyttsx3](https://pypi.org/project/pyttsx3/) (SAPI5 on Windows) |
| Weather data | [wttr.in](https://wttr.in) |
| Jokes | [official-joke-api](https://official-joke-api.appspot.com) |

---

## License

This is a personal learning project by **Ritam Naskar** — no license file is currently included, so all rights are reserved by the author. Feel free to open an issue or pull request on the [repository](https://github.com/RitamNaskar11/Voice_Assistant).

---

<p align="center">Built with Python and a lot of talking to a computer.</p>

