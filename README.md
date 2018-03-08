    ███████╗    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗
    ██╔════╝    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝
    █████╗      ██║  ██║██║███████╗██║     ██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝
    ██╔══╝      ██║  ██║██║╚════██║██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗  ╚██╔╝  
    ███████╗    ██████╔╝██║███████║╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║   ██║   
    ╚══════╝    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝


# Tree Discovery
## Machine Learning Algorithms for E-Discovery

Some background of the project
Discovery in a civil lawsuit is a process where each party turns over documents that are relevant to the case. We improve this process with an utility that helps law professionals classify these documents more efficiently.

We process emails through TF-IDF and LSA and use the output to train our proprietary implementation of random forest.


## Notable Parts of the Directory Structure

* `Documentation`
* `flask_server`
* `data_api.py`: Everything to do with interfacing between our ML backend and the beautiful front end.
* `lib`
* `forest.py`: Entry point into the ML code
* `web_new`
* `src`: All of the front end code is in here
* `email_filter.py`
* `README.md`: This file!
* `makefile`
* `scenario1Full.py`: Run a full scenario using this file.





## How to run
### Web:
1. At project root `make web_dep`
2. Then run `make web`
3. `command+t` to make a new terminal tab and
run `make -B web` in the new tab at project root and
navigate to http://localhost:8080/

### Running Scenario 1 from TREC 2011:
`python3 scenario1Full.py`


## The Data
We used a combination of Kaggle's dataset (https://www.kaggle.com/wcukierski/enron-email-dataset) and Trec's

## Authors
Ju Yun Kim
Dan Mayer
Lazar Zamurovic
Adam Tigar
Micah Nacht
Xingfan Xia    


Advised by Eric Alexander, Carleton College Computer Science Professor
