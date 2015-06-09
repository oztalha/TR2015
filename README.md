# Turkish General Elections 2015

Collects and analyzes election results.

## Data Collection
  - **scrape.py** : Scrapes province level vote shares from [Yenisafak](http://www.yenisafak.com.tr/secim-2015/secim-sonuclari) website
  - **data/TR2015.csv** : Province level vote shares (output of `scrape.py`)
  - **analyze.py** : Plots 2011 vs 2015 vote shares for each party