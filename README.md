# Turkish General Elections 2015

Collects and analyzes election results. Visit my blog [post](http://talhaoz.com/?p=735) to read more about the project.

## Data Collection
  - **scrape.py** :
	  - Scrapes **province level** vote shares from [Yenisafak](http://www.yenisafak.com.tr/secim-2015/secim-sonuclari) website
	  - Scrapes **district level** election results from [secim.haberler.com](http://secim.haberler.com) website
  - **data/TR2015.csv** : Province level vote shares (output of `scrape.py`)
  - **data/TR2015_ILCELER.csv** : District level vote shares (output of `scrape.py`)
  - **data/iller.csv** : Geographical region and other codes data for all the cities
  - **TEPLWeb.csv** : A great [dataset](http://www.luc.edu/faculty/gtezcur/data.html) of past Turkish elections by Gunes Murat Tezcur
  - **TR\_11_15.csv** : 2011 and 2015 **province level** election results merged. (Input to `VoteShifts.Rmd`)
  - **TR\_11\_15_ilce.csv** : 2011 and 2015 **district level** election results merged. (Input to `VoteShifts.Rmd`)

## Analysis
  - **analyze.py** : Plots 2011 vs 2015 vote shares for each party (see `charts/*.PNG` in addition to Plotly plots in the blog [post](http://talhaoz.com/?p=735)) and outputs `data/TR_11_15.csv`
  - **VoteShifts.Rmd** : Simply calls the `multirate` function in `VTR.R` script developed by [Andreadis](http://www.polres.gr/en/vtr) and creates a contingency table of vote transitions: outputs `data/TransitionRates.csv`  for transition results using *province level* data, and `data/TransitionRates_Ilce.csv` for transition results using *district level* data. (note that these values are before they normalized by parties' actual vote shares in '11). Absolute vote share transitions is in `data/Transitions.csv` and in `data/TransitionRates_Ilce.xlsx` files.