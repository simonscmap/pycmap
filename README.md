[![PyPI version](https://badge.fury.io/py/pycmap.svg)](https://badge.fury.io/py/pycmap)
[![DOI](https://zenodo.org/badge/199070692.svg)](https://zenodo.org/badge/latestdoi/199070692)
![Cover](https://github.com/simonscmap/pycmap/raw/master/docs/figures/CMAP.png)

*Mohammad Dehghani Ashkezari <mdehghan@uw.edu>*


# pycmap
Simons CMAP is an open-source data service to retrieve, visualize, and analyze oceanic datasets such as in-situ observations, multi-decade global satellite remote sensing, and model outputs. Pycmap is the python package of Simons CMAP project providing a simple and unified interface to the hosted datasets at Simons CMAP database. It enables the scientists and general public to dive into the vast, and often underutilized, ocean datasets and retrieve customized subsets of these massive datasets without going through the time-consuming process of data collection and preparation.

## Documentation
See the *table of contents* below for pycmap documentations. 
<br />The docs are written in jupyter notebook format and each notebook contains one or more example codes. Please download the `/docs` directory and run the example codes locally. Alternatively, you may run the examples on google cloud using the *Colab badge* which appears at the top of each page: 
<br /><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory">


<br /><br />More detailed system documentations can be found at [https://cmap.readthedocs.io/en/latest/](https://cmap.readthedocs.io/en/latest/).

## Website
Simons CMAP website is under active development at the moment: [https://simonscmap.com](https://simonscmap.com)

**<br />This project is supported by [Simons Foundation](https://www.simonsfoundation.org/).**




## Table of Contents


### [Installation](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Installation.ipynb)

### [1. Data Retrieval (API)](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/API.ipynb)
- [Query](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Query.ipynb)
- [Catalog](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Catalog.ipynb)
- [Search Catalog](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/SearchCatalog.ipynb)
- [Datasets](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Datasets.ipynb)
- [Datasets With Ancillary](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/DatasetsWithAncillary.ipynb)
- [Dataset MetaData](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/DatasetMetaData.ipynb)
- [Variable MetaData](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/MetaData.ipynb)
- [Dataset Columns](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Columns.ipynb)
- [Dataset Head](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Head.ipynb)
- [Variable Long Name](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/LongName.ipynb)
- [Variable Unit](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Unit.ipynb)
- [Variable Resolution](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Resolution.ipynb)
- [Variable Coverage](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Coverage.ipynb)
- [Variable Stat](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Stat.ipynb)
- [If Column Exists](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/HasField.ipynb)
- [Is Gridded Product](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Grid.ipynb)
- [Is Climatology Product](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/IsClimatology.ipynb)
- [List of Cruises](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Cruises.ipynb)
- [Cruise Details by Name](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/CruiseByName.ipynb)
- [Cruise Spatio-Temporal Bounds](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/CruiseBounds.ipynb)
- [Cruise Trajectory](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/CruiseTrajectory.ipynb)
- [Cruise Variables](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/CruiseVariables.ipynb)
- [Retrieve Dataset](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/RetrieveDataset.ipynb)
- [Retrieve Dataset With Ancillary](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/RetrieveDatasetWithAncillary.ipynb)
- [Data Subset: Generic Space-Time Cut](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/SpaceTime.ipynb)
- [Data Subset: TimeSeries](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/TimeSeries.ipynb)
- [Data Subset: Depth Profile](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/DepthProfile.ipynb)
- [Compute Climatology](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Climatology.ipynb)
- [Sampling](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Sampling.ipynb)
- [Match (colocalize) Cruise Track with Datasets](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/MatchCruise.ipynb)


### [2. Data Visualization](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz.ipynb)
- [Histogram Plot](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_Histogram.ipynb)
- [TimeSeries Plot](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_TimeSeries.ipynb)
- [Regional Map, Contour Plot, 3D Surface Plot](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_RegionalMap.ipynb)
- [Section Map, Section Contour](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_Section.ipynb)
- [Depth Profile](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_DepthProfile.ipynb)
- [Cruise Track Plot](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_CruiseTrack.ipynb)
- [Correlation Matrix](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_CorrelationMatrix.ipynb)
- [Correlation Matrix Along Cruise Track](https://colab.research.google.com/github/simonscmap/pycmap/blob/master/docs/Viz_CruiseCorrelationMatrix.ipynb)

