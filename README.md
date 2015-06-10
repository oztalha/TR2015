# Turkish General Elections 2015

Collects and analyzes election results.

## Data Collection
  - **scrape.py** : Scrapes province level vote shares from [Yenisafak](http://www.yenisafak.com.tr/secim-2015/secim-sonuclari) website
  - **data/TR2015.csv** : Province level vote shares (output of `scrape.py`)
  - **TEPLWeb.csv** : A great [dataset](http://www.luc.edu/faculty/gtezcur/data.html) of past Turkish elections by Gunes Murat Tezcur

## Analysis
  - **analyze.py** : Plots 2011 vs 2015 vote shares for each party
  - **VoteShifts.Rmd** : Simply calls the `multirate` function in `VTR.R` script developed by [Andreadis](http://www.polres.gr/en/vtr) and creates a contingency table of vote transitions: outputs `data/TransitionRates.csv` (note that these values are before they normalized by parties' actual vote shares in '11). Absolute vote share transitions is in `data/TransitionRates.csv`