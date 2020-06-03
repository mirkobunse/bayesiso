# Bayes-Iso

This repository contains a [Python implementation of the Non-parametric Bayesian Isotonic Calibration](newcal.py) (Bayes-Iso) algorithm. The rest of the code is the experiment conducted to compare Bayes-Iso to other calibration methods like Isotonic calibration, Logistic calibration, Beta calibration and ENIR. Descriptions and results can be found in the corresponding article published in ECML2019. 

## Usage

**1)** Install the R package *OpenML*, its dependencies, and the local R packages in this repository. To do so, type the following commands into your terminal:

    R -e 'update.packages(checkBuilt=TRUE, ask=FALSE)'
    R -e 'install.packages(c("OpenML", "farff", "RWeka"))'
    R -e 'install.packages("ENIR/enir/", repos=NULL, type="source")'
    R -e 'install.packages("ENIR/neariso 3/", repos=NULL, type="source")'

**2)** Download the data. You need to create an API key by registering at [OpenML.org](https://www.openml.org). Replace the placeholder in line 3 of `download_data.R` with your own key. Then, type the following into your terminal:

    Rscript download_data.R

**3)** Create a virtual environment for Python and install the dependencies:

    python3.6 -m venv venv
    venv/bin/pip install -r requirements.txt

**4)** Run the experiments:

    venv/bin/python -W ignore::FutureWarning run.py --size <NUMBER> --dataset <NUMBER>

For example,

    venv/bin/python -W ignore::FutureWarning run.py --size 100 --dataset 1
