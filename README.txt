
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
├── main.py
├── requirements.txt
├── README.md                      # inkl. hvor modellfiler lastes ned fra
├── config.py                      # stier, modellnavn, standardverdier
│
├── scripts/
│   └── download_models.py         # henter .onnx-filene så alle i gruppa får samme oppsett
│
├── src/
│   ├── core/                      # ren bildelogikk — INGEN Qt-import
│   │   ├── document.py            # aktivt bilde, filsti, dirty-flag, (lag-liste)
│   │   ├── history.py             # undo/redo
│   │   ├── fileio.py              # new, open, save, save as, properties
│   │   ├── selection.py           # rect / lasso / polygon → binær maske
│   │   ├── transforms.py          # crop, resize, rotate 90 L/R, flip v/h
│   │   ├── filters.py             # gaussian, sobel, binary, histogram-terskling
│   │   ├── drawing.py             # pensel, viskelær, teksturer, tekst
│   │   ├── shapes.py              # figurer, outline/fill
│   │   └── clipboard.py           # copy, cut, paste (jobber mot maske)
│   │
│   ├── vision/                    # AI-delen — heller ikke Qt
│   │   ├── face.py                # ansiktsdeteksjon + landmarks → FaceResult
│   │   ├── age.py                 # face crop → alder (+ konfidens)
│   │   ├── beauty.py              # retusj-operasjoner: skin smoothing, blur,
│   │   │                          #   lysstyrke/kontrast, warp — kjøres på ansiktsmaske
│   │   ├── loop.py                # beauty-loopen: mål alder før/etter, hold historikk
│   │   ├── effects.py             # overlays, bakgrunnsbytte (valgfri)
│   │   ├── overlay.py             # tegner bokser/labels på KOPI av framen
│   │   └── models/                # .onnx — i .gitignore
│   │
│   ├── camera/
│   │   └── stream.py              # QThread, webcam → frames som signal
│   │
│   └── ui/
│       ├── main_window.py
│       ├── menus.py               # de seks menyene fra kravlista
│       ├── canvas.py              # tegning, museinteraksjon
│       ├── viewport.py            # zoom/pan-state + koordinat-mapping skjerm↔bilde
│       ├── toolbar.py
│       ├── camera_window.py       # live-vindu, "Capture" → inn i editoren
│       └── panels/
│           ├── color_panel.py     # palett + penselstørrelse
│           ├── tool_panel.py
│           ├── beauty_panel.py    # slidere for retusj + alder-avlesning
│           ├── ai_panel.py        # ansiktsinfo, modellvalg
│           └── layer_panel.py     # valgfri
│
├── assets/
├── tests/
│   ├── test_filters.py
│   ├── test_transforms.py
│   ├── test_selection.py
│   └── test_age.py                # kjører mot 2–3 testbilder
└── docs/
├── assets/                    # penselteksturer, ikoner, overlay-PNG-er
├── tests/                     # test_filters.py, test_transforms.py
└── docs/                      # rapport, skjermbilder, arkitekturdiagram

