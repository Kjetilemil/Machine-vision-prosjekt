
Project group 6


This project uses the pyQt6 library for gui.
Documentation: https://doc.qt.io/qtforpython-6/


# Use the IKT213 enviroment
# Install in terminal: pip install PyQt6

Tanke på hvordan oppgaven kan bli:
Dekke kravene som er gitt i oppgaven, men også en beauty-loop hvor man kan redigere bilde av ansiktet sitt til å se yngre ut, dermed bruke -
AI Detection til å gjette hvor ung personen er. Dette kan skape en gøy loop hvor man minmaxer beauty standards.


Plan for oppsett:
mv-editor/
├── main.py                        # kun: sys.path-oppsett, QApplication, MainWindow
├── requirements.txt
├── README.md                      # oppsett, kjøring, modellnedlasting
├── config.py                      # stier, modellnavn, standardverdier
├── .gitignore                     # models/, __pycache__/, exports/
│
├── scripts/
│   ├── download_models.py         # henter modellfiler, verifiserer checksum
│   └── eval_age.py                # eksperiment: treffsikkerhet mot kjente aldre → tabell
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                      # ren bildelogikk — INGEN Qt, INGEN modeller
│   │   ├── __init__.py
│   │   ├── document.py            # eier self.image (BGR ndarray), filsti, dirty-flag
│   │   ├── history.py             # undo/redo: stack av hele arrays, maks 20
│   │   ├── fileio.py              # new, open, save, save as, properties
│   │   ├── selection.py           # rect / lasso / polygon → binær maske
│   │   ├── transforms.py          # crop, resize, rotate 90 L/R, flip v/h
│   │   ├── filters.py             # gaussian, sobel, binary, histogram-terskling
│   │   ├── retouch.py             # skin smoothing, blur, lysstyrke/kontrast, warp
│   │   ├── drawing.py             # pensel, viskelær, teksturer, tekst
│   │   ├── shapes.py              # figurer, outline/fill
│   │   └── clipboard.py           # copy, cut, paste (jobber mot maske)
│   │
│   ├── vision/                    # modell-avhengig — heller ingen Qt
│   │   ├── __init__.py
│   │   ├── face.py                # deteksjon + landmarks → FaceResult
│   │   ├── age.py                 # face crop → float alder + konfidens
│   │   ├── mask.py                # landmarks → ansiktsmaske (hud, øyne, munn)
│   │   ├── detector.py            # YOLO: frame → [(label, conf, box)]
│   │   ├── effects.py             # overlays, bakgrunnsbytte (valgfri)
│   │   └── overlay.py             # tegner bokser/labels på KOPI av framen
│   │
│   ├── experiment/
│   │   ├── __init__.py
│   │   ├── params.py              # RetouchParams: dataclass med alle slider-verdier
│   │   └── loop.py                # kjør params → mål alder → logg Trial → export_trials()
│   │
│   ├── camera/
│   │   ├── __init__.py
│   │   └── stream.py              # QThread, webcam → frames som signal, frame-dropping
│   │
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py
│       ├── menus.py               # de seks menyene fra kravlista
│       ├── canvas.py              # tegning, museinteraksjon
│       ├── viewport.py            # zoom/pan-state + koordinat-mapping skjerm↔bilde
│       ├── toolbar.py
│       ├── camera_window.py       # live-vindu, "Capture" → inn i editoren
│       └── panels/
│           ├── __init__.py
│           ├── color_panel.py     # palett + penselstørrelse
│           ├── tool_panel.py
│           ├── beauty_panel.py    # retusj-slidere, alder-avlesning, kurve, eksport
│           ├── ai_panel.py        # ansiktsinfo, modellvalg (Levi-Hassner / InsightFace)
│           └── layer_panel.py     # valgfri
│
├── assets/                        # penselteksturer, ikoner, overlay-PNG-er
├── data/
│   └── faces/                     # testbilder med kjent alder, for eval_age.py
├── exports/                       # CSV fra loopen — i .gitignore
│
├── tests/
│   ├── test_filters.py
│   ├── test_transforms.py
│   ├── test_selection.py
│   ├── test_retouch.py            # ren ndarray-test, ingen modeller nødvendig
│   └── test_age.py                # kun: krasjer ikke, 0–100, deterministisk
│
└── docs/                          # rapport, skjermbilder, arkitekturdiagram
