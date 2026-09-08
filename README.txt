
Project group 6


This project uses the pyQt6 library for gui.
Documentation: https://doc.qt.io/qtforpython-6/


# Use the IKT213 enviroment
# Install in terminal: pip install PyQt6

Plan for oppsett:
mv-editor/
├── main.py                    # starter QApplication, ingenting annet
├── requirements.txt
├── README.md
│
├── src/
│   ├── core/                  # ren bildelogikk — INGEN Qt-import
│   │   ├── document.py        # aktivt bilde, filsti, dirty-flag, undo-stack
│   │   ├── history.py         # undo/redo
│   │   ├── fileio.py          # new, open, save, save as, properties
│   │   ├── selection.py       # rect / lasso / polygon → binær maske
│   │   ├── transforms.py      # crop, resize, rotate, flip
│   │   ├── filters.py         # gaussian, sobel, binary, histogram-terskling
│   │   ├── drawing.py         # pensel, viskelær, teksturer, tekst
│   │   ├── shapes.py          # figurer, outline/fill
│   │   └── clipboard.py       # copy, cut, paste (jobber mot maske)
│   │
│   ├── vision/                # AI-delen — heller ikke Qt
│   │   ├── detector.py        # YOLO: frame → [(label, conf, box)]
│   │   ├── face.py            # ansiktsdeteksjon + landmarks
│   │   ├── age.py             # face crop → aldersbøtte
│   │   ├── effects.py         # overlays, bakgrunnsbytte
│   │   ├── overlay.py         # tegner bokser/labels på en kopi av framen
│   │   └── models/            # .onnx / .caffemodel — i .gitignore
│   │
│   ├── camera/
│   │   └── stream.py          # QThread, leser webcam, sender frames som signal
│   │
│   └── ui/
│       ├── main_window.py     # setter sammen alt
│       ├── menus.py           # de seks menyene fra kravlista
│       ├── canvas.py          # QWidget: tegning, zoom, museinteraksjon
│       ├── toolbar.py
│       ├── camera_window.py   # live-vindu, "Capture"-knapp → inn i editoren
│       └── panels/
│           ├── color_panel.py
│           ├── tool_panel.py
│           ├── ai_panel.py    # deteksjonsliste, alder, filtervalg
│           └── layer_panel.py # valgfri
│
├── assets/                    # penselteksturer, ikoner, overlay-PNG-er
├── tests/                     # test_filters.py, test_transforms.py
└── docs/                      # rapport, skjermbilder, arkitekturdiagram

