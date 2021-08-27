# DEEP ESG Data Processing Technical Challenge


## Solutions Architecture
---

The algorithm works in the following manner:
- Get the files and transform to a dataframe;
- Sum all the values related to the same account;
- Relate the values to the chart of accounts;
- Get the number of subdivisions of accounts;
- Order the data to aggregate the data based on the subdivision;
- For each parent subdivision, check if the child subdivision exists and adds the value;
- Reorder the data and save.


## Local Project Setup  
---

### Install Packages  
  
``` pip install -r requirements.txt```
  
### Running
  
```python run.py```

### Run Unit Tests

```python test.py```

## Details of Development
---

The solution took around 7 hours to be developed. I chose to first use concepts of dataframe and dictionary. With the dataframe, I can perform very straightforward manipulations. To perform calculations and organize, I can use dict comprehension, it's also valid in case of using json requests.

The application is set to be scalable, it defines the number of subdivisions and the whole process is based on that. It was also written in a OOP paradigm because it makes easier to manipulate the code and access methods and attributes.