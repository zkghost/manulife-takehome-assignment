# Manulife Take-Home Exercise
## Requirements
Docker **OR** Python3 with pytest installed. 

## To Run
If using Docker, build the image and then run it interactively. 
```
docker build .
docker run -it <image ID>
```
By default this will open a bash shell. 

Now, in either case, run:
```
python3 combine_csvs.py
```
to produce the Combined.csv in `Engineering Test Files`, or

```
pytest .
```
to run unit tests.