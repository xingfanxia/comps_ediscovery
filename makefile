dep_mac:
	mkdir temp
	wget -O temp/anaconda3.5.sh https://repo.continuum.io/archive/Anaconda3-5.0.0-MacOSX-x86_64.sh
	bash temp/anaconda3.5.sh
	pip3 install aws-cli

dep_linux:
	mkdir temp
	wget -O temp/anaconda3.5.sh https://repo.continuum.io/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh
	bash temp/anaconda3.5.sh
	pip3 install aws-cli

download_all:
	aws s3 sync s3://comps-ediscovery data/

upload_all:
	aws s3 sync data/ s3://comps-ediscovery

download_parsed:
	aws s3 sync s3://comps-ediscovery/parsed data/parsed/

upload_parsed:
	aws s3 sync data/parsed s3://comps-ediscovery/parsed 
	
run:
	jupyter notebook
