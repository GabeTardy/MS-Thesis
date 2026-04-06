# MS-Thesis
This repository contains the final version of the code used in my MS Thesis, entitled "Finite Element Modeling of Snap-buckling of Shallow Arches with Bimodular Materials."  The text of the thesis explains how the code in the repository works in much more detail.

## Contents
The code in this repository is broken into two folders:
- Code
    - This code was used to run the analyses in the thesis.
- Animations
    - This code was used to create the animations in the defense presentation.

Each folder has its own installation directions and software requirements.

## AI Disclosure
Any code written by AI (ChatGPT or Claude) is minimal. That which does exist is clearly marked in comments in the code. Any truly central code (that of the finite element analysis or postprocessing and plotting work) is written by me. You can tell because it is terribly unoptimized.

## Getting Started
### Installation
Download the repository directly, or clone the repository locally:
```bash
git clone https://github.com/GabeTardy/MS-Thesis.git
```

### Development Requirements
#### MS-Thesis/Code
- [Ansys Mechanical APDL 2025R1+](https://www.ansys.com/products/structures/ansys-mechanical)*
- [Maplesoft Maple 2025.1+](https://www.maplesoft.com/products/maple/new_features/index.aspx)
- [APDL Language Support](https://marketplace.visualstudio.com/items?itemName=ekibun.apdl-language-support) for VS Code
- Recommended: [Modern Fortran](https://marketplace.visualstudio.com/items?itemName=fortran-lang.linter-gfortran) for VS Code

\* An administrator account is required to compile `usermat.F`.

#### MS-Thesis/Animations
- [uv](https://github.com/astral-sh/uv) Package Manager (Or knowledge of how to use another python package manager)
- Python 3.14*
- [Manim (Community) v0.20.1](https://github.com/manimCommunity/manim)*
- [SciPy 1.17.1](https://github.com/scipy/scipy)*
- Recommended: [Microsoft Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (+Pylance, Debugger, etc.) for VS Code

\* Strongly recommended to be installed as follows by running each line in order with a terminal in the MS-Thesis/Animations directory:
```bash
uv python install
uv init
uv add manim
uv run manim checkhealth
uv add scipy
```

### Usage
#### MS-Thesis/Code
This folder should become (or be merged with) the working directory for Ansys Mechanical APDL for all of my scripts to work properly. This can be done by running `install.bat` to set the Usermat path correctly and `apdl.bat` to actually run Mechanical APDL in the current folder. 

Both `apdl.bat` and `Snap2DMaple.mw` must be updated for different versions of Mechanical APDL.

#### MS-Thesis/Animations
`main.py` contains all three animations. Each can be rendered in low detail using the command:
```bash
uv run manim --disable_caching -pql main.py [NAME OF ANIMATION HERE]
```
where `[NAME OF ANIMATION HERE]` is replaced by the name of the class containing the animation. The three classes are:
- Slide 22: `FactorStaticEq`
- Slide 23: `IntroStaticPlot`
- Slide 39: `CriticalLoadPlot`

The final versions of the animations used in the presentation are rendered in 4K60 with the following command:
```bash
uv run manim --disable_caching -pqk main.py [NAME OF ANIMATION HERE]
```

`FactorStaticEq` and `IntroStaticPlot` are compatible with the OpenGL renderer, but `CriticalLoadPlot` uses a hack that was only implemented for Cairo, so keep that in mind. It may be compatible, but I have never tested it.