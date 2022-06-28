# SDK Tooling Challenge
A sdk tooling assignment by Dyte to create a CLI tool to check and update the version of a dependency. It should give the current version of that dependency and tell if the version is greater than or equal to the version specified or not. 
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following

```bash
    pip install PyGithub
```
```bash
    pip install pandas
```
## usage

* used a github API: [PyGithub](https://github.com/PyGithub/PyGithub) to access and update the contents of both public and private repositories using their access tokens. 

* access-tokens.json:
store the access token here.
```bash
    {
        "token": "<provide access token hear>"
    }
```
* create a CSV file (Dyte.csv) with columns "name" and "repo".

* Use command:
```bash
    Python myawesometool.py <CSV file path> <dependency_name>@<version> 
```
Eg.
```bash
    Python myawesometool.py Dyte.csv axios@0.23.0 
```

to list out:
1. name of the repo 
2. repo URL
3. current_version
4. current_version satisfies the mentioned version or not (True or False).

* Use command:
```bash
    Python myawesometool.py <CSV file path> <dependency_name>@<version> update
```
Eg.
```bash
    Python myawesometool.py Dyte.csv axios@0.23.0 update
```
to list out:
1. name of the repo 
2. repo URL
3. current_version
4. current_version satisfies the mentioned version or not (True or False).
5. pull request status.

update command updates the dependencies in package.json file, generates updated package-lock.json file for all the repositories that have the version lower than the one specified and creates a pull request.

## Output

```bash
    Python myawesometool.py Dyte.csv axios@0.23.0 
```
![output_1.png](output_1.png?raw=true "result")

```bash
    Python myawesometool.py Dyte.csv axios@0.23.0 update
```
![output_2.png](output_2.png?raw=true "result")