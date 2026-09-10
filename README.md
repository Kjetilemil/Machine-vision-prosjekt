
Project group 6



# Use the IKT213 enviroment

Tanke på hvordan oppgaven kan bli:
Dekke kravene som er gitt i oppgaven, men også en beauty-loop hvor man kan redigere bilde av ansiktet sitt til å se yngre ut, dermed bruke -
AI Detection til å gjette hvor ung personen er. Dette kan skape en gøy loop hvor man minmaxer beauty standards.


Plan for oppsett:
mv-editor/
├── pyproject.toml
├── main.py                        # 2 linjer: from mv_editor.app import main; main()
├── README.md                      # oppsett, kjøring, modellnedlasting
├── .gitignore                     # .venv/ *.egg-info/ models/ exports/ __pycache__/
│
├── scripts/
│   ├── download_models.py         # Levi-Hassner (Caffe) + checksum. Instansierer også
│   │                              #   FaceAnalysis én gang → henter ~/.insightface
│   └── eval_age.py                # treffsikkerhet mot kjente aldre → tabell til rapport
│
├── src/
│   └── mv_editor/
│       ├── __init__.py
│       ├── app.py                 # main(): QApplication + MainWindow.
│       │                          #   Sjekker ~/.insightface, sier fra hvis tom
│       ├── config.py              # parents[2] for rotmappe, modellnavn, standardverdier
│       │
│       ├── core/                  # ren bildelogikk — INGEN Qt, INGEN modeller
│       │   ├── __init__.py
│       │   ├── document.py        # eier self.image (BGR ndarray), filsti, dirty-flag
│       │   ├── history.py         # undo/redo: stack av hele arrays, maks 20
│       │   ├── fileio.py          # new, open, save, save as, properties
│       │   ├── masking.py         # KONVENSJONEN bor her (modul-docstring):
│       │   │                      #   float32, én kanal, 0.0–1.0, samme H×W.
│       │   │                      #   blend(base, edited, mask)
│       │   ├── selection.py       # rect / lasso / polygon → binær maske
│       │   │                      #   (float32 0/1 — se masking.py)
│       │   ├── transforms.py      # crop, resize, rotate 90 L/R, flip v/h
│       │   ├── filters.py         # gaussian, sobel, binary, histogram-terskling
│       │   ├── retouch.py         # skin smoothing, blur, lysstyrke/kontrast, warp
│       │   ├── drawing.py         # pensel, viskelær, teksturer, tekst
│       │   ├── shapes.py          # figurer, outline/fill
│       │   └── clipboard.py       # copy, cut, paste (jobber mot maske)
│       │
│       ├── vision/                # modell-avhengig — heller ingen Qt
│       │   ├── __init__.py
│       │   ├── face.py            # deteksjon + landmarks → FaceResult
│       │   ├── age.py             # AgeEstimator-protokoll: InsightFaceAge (primær,
│       │   │                      #   regresjon) + LeviHassnerAge (softmax-forventning)
│       │   ├── mask.py            # landmarks → ansiktsmaske, fjæret
│       │   │                      #   (float32 0.0–1.0 — se core/masking.py)
│       │   ├── effects.py         # overlays, bakgrunnsbytte (valgfri)
│       │   └── overlay.py         # tegner bokser/labels på KOPI av framen
│       │
│       ├── experiment/
│       │   ├── __init__.py
│       │   ├── params.py          # RetouchParams: dataclass med alle slider-verdier
│       │   └── loop.py            # params → mål alder → logg Trial → export_trials()
│       │
│       ├── camera/
│       │   ├── __init__.py
│       │   └── stream.py          # QThread, webcam → frames som signal, frame-dropping
│       │
│       └── ui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── menus.py           # de seks menyene fra kravlista
│           ├── canvas.py          # tegning, museinteraksjon
│           ├── viewport.py        # zoom/pan-state + koordinat-mapping skjerm↔bilde
│           ├── toolbar.py
│           ├── camera_window.py   # live-vindu, "Capture" → inn i editoren
│           └── panels/
│               ├── __init__.py
│               ├── color_panel.py     # palett + penselstørrelse
│               ├── tool_panel.py
│               ├── beauty_panel.py    # retusj-slidere, alder-avlesning, kurve, eksport
│               ├── ai_panel.py        # ansiktsinfo, modellvalg
│               └── layer_panel.py     # valgfri
│
├── assets/                        # penselteksturer, ikoner, overlay-PNG-er
├── data/
│   └── faces/                     # testbilder med kjent alder, for eval_age.py
├── models/                        # .caffemodel / .prototxt — i .gitignore
├── exports/                       # CSV fra loopen — i .gitignore
│
├── tests/
│   ├── test_filters.py
│   ├── test_transforms.py
│   ├── test_selection.py
│   ├── test_masking.py            # helt 0 → base, helt 1 → edited, dtype-sjekk
│   ├── test_retouch.py            # ren ndarray-test, ingen modeller nødvendig
│   └── test_age.py                # kun: krasjer ikke, 0–100, deterministisk
│
└── docs/                          # rapport, skjermbilder, arkitekturdiagram
