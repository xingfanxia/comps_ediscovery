dep:
	cd data
	wget https://repo.continuum.io/archive/Anaconda3-5.0.0-MacOSX-x86_64.sh
	bash Anaconda3-5.0.0-MacOSX-x86_64.sh
	pip3 install aws-cli
download:
	aws s3 sync s3://comps-ediscovery data/
upload:
	aws s3 sync data/ s3://comps-ediscovery
run:
	jupyter notebook