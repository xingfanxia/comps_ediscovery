download:
	aws s3 sync s3://comps-ediscovery data/
upload:
	aws s3 sync data/ s3://comps-ediscovery
run:
	jupyter notebook