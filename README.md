# Manulife Take-Home Exercise
## Requirements
Docker **OR** Python3 with pytest installed. 

## To Run
*I ran this on Ubuntu 20.04 inside WSL2 running in Windows 11. My guess is that it's fairly close to a vanilla ubuntu install. If you're using Docker to run it, it **should** work on Docker Desktop for Windows/Mac.*

If using Docker, build the image and then run it interactively. 
```
docker build -t manulife.
docker run -it manulife
```
By default this will open a bash shell inside the container at `/app/`. The repo will be copied to the `/app/` directory. 

If not using Docker, just make sure you install `pytest`:
```
# you can also use a virtualenv for this step if necessary
pip3 install pytest
# OR 
pip3 install -r requirements.txt
```
Now, in either case, run:
```
python3 combine_csvs.py
```
to produce the Combined.csv in `Engineering Test Files`, or

```
pytest .
```
to run unit tests.

### Exporting Output
If using Docker and you want to keep the output on disk afterward, you can do something like:
```
# when using docker run, mount a directory for output
docker run -it -v $(pwd)/output:/app/out manulife
# then from within container:
python3 combine_csvs.py
cp Engineering\ Test\ Files/Combined.csv out/
exit
# now the output file should be stored in output/ dir
# NOTE: it will be owned by root by default; there are graceful ways to 
#       have the files be owned by whoever is calling docker run (ie, 
#       pass in user/group IDs at runtime, use them in the dockerfile),
#       but for a single output its fine to just use chown outside dir. 
```
