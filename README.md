# Supporting Documentation for OU Dept of Physics Website CMS Migrations

## Set-Up

The following bash program was used to retrieve all website resources.

```bash
wget --recursive \ #follows links
     --depth 10 \ # only follows links 10 levels from root
     --no-clobber \ # does not overwrite or create duplicate files
     --page-requisites \ # gets all JS, CSS, images, sounds
     --domains https://www.nhn.ou.edu \ # only indexes www.nhn.ou.edu files
     https://www.nhn.ou.edu/ \
```

Running the `wget` program will, firstly, make a new directory inside `pwd` called https://www.nhn.ou.edu/.  In this directory, the program will add all contents in the entire file system.

## My Work

