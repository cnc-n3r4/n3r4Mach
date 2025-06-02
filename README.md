# n3r4Mach

**Modular CNC tooling utilities** — built to support machinists, programmers, and automation teams with a simple local interface that runs entirely on your own machine.

---

## 🎯 Purpose

n3r4Mach is a machinist-focused toolkit that brings together CNC calculators, reference libraries, program analyzers, and G-code tools into a single, easy-to-use desktop app — powered by Python, and presented in a clean, browser-style interface. Giving machinists an easy to use, no CAD/CAM sofware needed, way to modify posted programs and not understand the underlying g-code. You don't need to run a server, install Apache, or know web development. Just open the app and go.

---

## 🔧 Key Tools (in development)

- 🛠️ **Tool Remapper**  
  Remap T/H/D tool numbers in NC files based on a selected tool list — great for cleaning up posted NC files to match existing tool magazine/carosels.

- 🧮 **Trig & Geometry Calculator**  
  Solve right triangles, bolt circles, arc lengths, and other common shop math problems.

- 📐 **Macro Evaluator**  
  Parse and evaluate Fanuc-style macro expressions like `#100 = COS[30] + 2`. Supports variable memory and math functions.

- 📂 **File Drop Support (coming soon)**  
  Drag NC files directly into the interface to run checks, extract tooling info, or apply program modifications and changes.
  

---

## 🧱 Roadmap

- 🕳️ **Tap & Drill Validator**  
  Verify that every tap cycle has a correctly sized drill operation beforehand, with pitch and feed rate analysis.

- ✂️ **Operation Reorderer**  
  Cut/paste entire tool blocks safely. Maintain correct H/D offset logic, spindle conditions, and clearance.

- 🧠 **G-code Intelligence Linter**  
  Warn about missing spindle starts, wrong tool calls, or improper macro math. CNC-aware diagnostics.

- 🧰 **Tool Data Dashboard**  
  Visual overview of all tools used in a file: descriptions, offsets, speeds, feeds, and wear comp settings.

- 🌀 **Backplot Viewer**  
  Basic G-code backplot with 2D move visualization, warnings for unsafe moves, and toolpath summary.

---

## 🖥️ Architecture

- **Frontend**:  
  HTML, CSS, and JavaScript for the interface  

- **Backend**:  
  Python (standalone) — no server required  
  Python modules are exposed to the frontend via [Eel](https://github.com/python-eel/python-eel)

- **Testing and Prototyping**:  
  Jupyter Notebooks may be used for math logic and parsing prototypes, but the final tools run in a desktop GUI

---

## 🧑‍🤝‍🧑 Contributing

We welcome help! Whether you write in Python, HTML, or just want to test tools — there’s room here.

Planned structure includes:

- Modular tools (each in their own folder)
- UI dropdown/tabs to switch modes
- Drag-and-drop NC file support
- Build scripts for generating `.exe` apps for Windows users

---

## 🚧 Status

✅ GitHub Repo Initialized  
✅ Basic HTML UI (Trig / Macro / Geometry)  
✅ Desktop Tool Remapper (Python, needs integration)  
🔄 Eel bridge to connect frontend ↔ backend  
🔄 Logic conversion from JS → Python  
🔄 GUI packaging for local use  

---

## 📫 Contact

Project Lead: [@cnc-n3r4](https://github.com/cnc-n3r4)  
Interested in helping? Submit an issue or pull request!

---

> 🦾 *Built for real-world application.*
