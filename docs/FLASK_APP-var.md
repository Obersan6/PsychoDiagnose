# Use this command everytime I activate the environment so Flask can locate the environment

***Because I don't want to install ```python-dotnv```.

### COMANDS TO USE FOR FLASK TO LOCATE THE APPLICATION

I have to do this to set ```FLASK_APP``` environment var correctly.

```
export FLASK_APP=src.main.app:app
export FLASK_ENV=development  # Optional: Enables debug mode
```

- Then run Flask with debug mode
```
flask run --debug
```