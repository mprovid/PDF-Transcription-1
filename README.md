# PDF Transcription (stage 1)
## What This Is:
This is a simple Python script that will take PDF files from a designated folder and turn them into text transcriptions saved to another designated folder.
## How to Use This Script:
### Applications
1. Install a code editor / integrated development environment like **VS Studio** [https://code.visualstudio.com/]
2. Install **Python** (this was built with Python 3.14) [https://www.python.org/]
3. Install **PyMuPDF** [https://pymupdf.readthedocs.io/en/latest/]
4. Get your own **Google Gemini API key** (the free one works in September 2026) [https://aistudio.google.com/api-keys]
### Configuration
- You should inspect the Python code in **app2.py** before running it on your PC. It should make sense to you and you should know what it's doing.
- the **config.py** file and the **app2.py** file should be in the same folder.
- You will need the edit the **config.py** file. It will contain your **Google Gemini API key** (don't share that) and you will need to set your source and target folders. The folder locations set in the **config.py** file demonstrate python file location syntax but it is unlikely that those file locations exist on your PC.
### Run the Batch
1. Open **VS Studio**.
2. Open **app2.py** in VS Studio.
3. Click the **run button** at the top right.
4. Look for your .txt transcriptions in your target folder.
## Next Steps
As time and help permits, this application can become a more functional tool. Right now, this is just a demo with a very simple prompt and limited functionality.
### Known Issues
- The script needs to be modified with a more robust transcription prompt. The current one merely demonstrates the script produces a result.
- The transcription reports an error if the API does not respond. This leaves gaps in the transcription. The script needs to be modified so tat it pauses when there is an error due to momentary non-response from the API. The script should retry without reporting if a successful retry happens within a certain number of attempts. Errors should be logged only if the system is fully non-responsive over multiple tries. Error gaps in the current transcriptions are, usually, quickly followed by a successful attempt at the next text block.

(9/26/2026)
