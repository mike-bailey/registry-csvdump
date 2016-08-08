# registry-csvdump
Dumps registry hives into CSV dumps to moderately kind of ok degree of accuracy using python-registry.

Steps:

`pip install python-registry`

then


`python registryparse.py -d filename`
**or** 
`python registryparse.py -f filename`

**Exports in UTF8 with the below CSV header**

Header:
```
Path, Timestamp, Key Name, Key Type, Key Data
```
