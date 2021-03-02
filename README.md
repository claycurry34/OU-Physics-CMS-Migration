# Supporting Documentation for OU Dept of Physics Website CMS Migrations

## Set-Up

The following bash program and options were used to retrieve all website resources.

```bash
wget -r -p -nc --depth 10 --domains https://www.nhn.ou.edu https://www.nhn.ou.edu/
```

Running the `wget` program will, firstly, make a new directory inside `pwd` called https://www.nhn.ou.edu/.  In this directory, the program will add all contents in the entire file system.

## My Work

