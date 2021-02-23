# Supporting Documentation for OU Dept of Physics Website CMS Migrations

The following bash program was used to retrieve all website resources.

```bash
wget https://www.nhn.ou.edu/ \
     --recursive \ #follows links
     --depth 10 \ # only follows links 10 levels from root
     --no-clobber \ # does not overwrite or create duplicate files
     --page-requisites \ # gets all JS, CSS, images, sounds
     --domains https://www.nhn.ou.edu \ # only indexes www.nhn.ou.edu files
```
