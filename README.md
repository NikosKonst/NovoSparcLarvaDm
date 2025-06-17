# NovoSparcLarvaDm
Single-cell spatial reconstruction of the Drosophila developing visual system.

**"Gene expression cartography of a developing neuronal structure"**  
Leonardo Tadini, Lilia Younsi, Isabel Holguera, Félix Simon, Maximilien Courgeon, Nikos Konstantinides
bioRxiv 2025.03.30.646184; doi: https://doi.org/10.1101/2025.03.30.646184
Contact: nikos.konstantinides@ijm.fr

---

## Overview

This repository contains the code used to spatially reconstruct and analyze single-cell gene expression patterns during the development of the **Drosophila optic lobe**. It integrates single-cell transcriptomics with computational spatial inference, allowing users to:

- Reconstruct spatial gene expression maps from scRNA-seq data
- Identify spatial gene modules and regionalized expression
- Visualize developing neuronal structures at cellular resolution

---

## Installation

Clone the repository and install the required packages.

### Using pip
```bash
git clone https://github.com/yourusername/gene-expression-cartography.git
cd gene-expression-cartography
pip install -r requirements.txt
```

### Using conda (recommended)
```bash
conda env create -f environment.yml
conda activate cartomap
```

---

## 🧪 Usage

Run the main reconstruction pipeline:

```bash
python run_cartography.py --config configs/optic_lobe.yaml
```

Or explore results interactively via Jupyter:

```bash
jupyter notebook notebooks/optic_lobe_reconstruction.ipynb
```

Example input/output data and config files are provided in the `/examples` directory.

---

## 📂 Repository Structure

```
.
├── src/                  # Core source code
├── notebooks/            # Jupyter notebooks for exploration and figures
├── data/                 # Sample data (see README in folder)
├── scripts/              # Preprocessing steps
└── README.md             # This file
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📚 Citation

If you use this code, please cite:

> Leonardo Tadini, Lilia Younsi, Isabel Holguera, Félix Simon, Maximilien Courgeon, Nikos Konstantinides (2025)
> *Gene expression cartography of a developing neuronal structure*. bioRxiv 2025.03.30.646184; doi: https://doi.org/10.1101/2025.03.30.646184

---

## 🙋 Acknowledgements

Developed in the Konstantinides lab of the Institut Jacques Monod, with support by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No. 949500) and the HORIZON-WIDERA-2023-ACCESS-02 grant no. 101159925 - SCENTINEL..  
Built on top of tools like [novoSpaRc](https://github.com/rajewsky-lab/novosparc), and others.
