# stackexchangeparser

Tooling for parsing data from Cardano Stack Exchange. After gradiation from beta, Area 51 is no longer monitoring the health status of our site.

It is crucial to gather this data to gain insights from the developing community and collective interests of the ecosystem.

# Download

Download StackExchange files as a `7z` file and extract them with

```bash
~/target_directory$ 7z x ~/archive.7z
```


# Parser

See `stackexchangeparser.py` and execute it as `$ ./stackexchangetocsv.py <from-XML-file> <save-to-file>`, for example

```
$./stackexchangeparser/stackexchangetocsv.py data/ data/csv-out
```
