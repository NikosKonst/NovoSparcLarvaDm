# NovoSparcLarvaDm
Single-cell spatial reconstruction of the Drosophila developing visual system.

**"Gene expression cartography of a developing neuronal structure"**  
Leonardo Tadini, Lilia Younsi, Isabel Holguera, Félix Simon, Maximilien Courgeon, Nikos Konstantinides
bioRxiv 2025.03.30.646184; doi: https://doi.org/10.1101/2025.03.30.646184
Contact: nikos.konstantinides@ijm.fr

---

## 🧬 Overview

This repository contains the code used to spatially reconstruct and analyze single-cell gene expression patterns during the development of the **Drosophila optic lobe**. It integrates single-cell transcriptomics with computational spatial inference, allowing users to:

- Reconstruct spatial gene expression maps from scRNA-seq data
- Identify spatial gene modules and regionalized expression
- Visualize developing neuronal structures at cellular resolution

---

## ⚙️ Installation

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
├── configs/              # YAML configuration files for each run
├── data/                 # Sample data (see README in folder)
├── results/              # Example outputs
├── environment.yml       # Conda environment
├── requirements.txt      # Python packages
└── README.md             # This file
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📚 Citation

If you use this code, please cite:

> Nikos X et al. (2025)  
> *Gene expression cartography of a developing neuronal structure*. bioRxiv.  
> [DOI: 10.xxxx/xxxxxx](https://doi.org/xx.xxxx/xxxxxx)

---

## 🙋 Acknowledgements

Developed in the [Your Lab Name], with support from [Funding Body, if applicable].  
Built on top of tools like [novoSpaRc](https://github.com/rajewsky-lab/novosparc), [scanpy](https://github.com/scverse/scanpy), and others.
