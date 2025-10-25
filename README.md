# databricks_git_folders_demo

This is the demo of databricks git folders demo

Here we need to do the following:

--  add/integrate git credentials in databricks
--  create a git folder in databricks by providing the remote repository url
--  create a feature_1 branch out of the main branch

We will do the same as we did in databricks asset bundles

go to the directory in databricks
/Users/gmail_id/databricks_git_folders_demo

we will initialize , but this time it is not required to have databrickscgf file as we are in databricks itself, so no need of authentication , databricks will take care of that

Run commands:

databricks bundle init
-- it will prompt some details and initialize the bundle and create a project

Welcome to the default Python template for Databricks Asset Bundles!
Please provide the following details to tailor the template to your preferences.

Unique name for this project [my_project]: databricks_git_folders_proj
Include a stub (sample) notebook in 'databricks_git_folders_proj/src': yes
Include a stub (sample) Lakeflow Declarative Pipeline in 'databricks_git_folders_proj/src': yes
Include a stub (sample) Python package in 'databricks_git_folders_proj/src': yes
Use serverless compute: yes
Workspace to use (auto-detected, edit in 'databricks_git_folders_proj/databricks.yml'): http://127.0.0.1:7073

✨ Your new project has been created in the 'databricks_git_folders_proj' directory!

Please refer to the README.md file for "getting started" instructions.
See also the documentation at https://docs.databricks.com/dev-tools/bundles/index.html.

So, project structre is like :
pwd
/Users/hemantbansal1992@gmail.com/databricks_git_folders_demo/databricks_git_folders_proj

/Users/hemantbansal1992@gmail.com/databricks_git_folders_demo/databricks_git_folders_proj$ ls -alrt
total 38
-rw-r--r-- 1 hemant.agarwal domain users 2287 Oct 22 12:37 README.md
-rw-r--r-- 1 hemant.agarwal domain users  920 Oct 22 12:37 pyproject.toml
-rw-r--r-- 1 hemant.agarwal domain users   87 Oct 22 12:37 .gitignore
-rw-r--r-- 1 hemant.agarwal domain users 1186 Oct 22 12:37 databricks.yml
drwxr-xr-x 2 hemant.agarwal domain users 4096 Oct 22 12:37 .vscode
drwxr-xr-x 2 hemant.agarwal domain users 4096 Oct 22 12:37 resources
drwxr-xr-x 2 hemant.agarwal domain users 4096 Oct 22 12:37 fixtures
drwxr-xr-x 2 hemant.agarwal domain users 4096 Oct 22 12:37 scratch
drwxr-xr-x 2 hemant.agarwal domain users 4096 Oct 22 12:37 tests
drwxr-xr-x 3 hemant.agarwal domain users 4096 Oct 22 12:37 src
drwxr-xr-x 4 hemant.agarwal domain users 4096 Oct 22 12:37 ..
drwxr-xr-x 9 hemant.agarwal domain users 4096 Oct 22 12:38 .

point to note that .databricks is created when we deploy or validate a bundle

we will change the host to include the actual host name for dev and prod environment in databricks.yml file as it is taking host as http://127.0.0.1:7073 right now

so, databricks.yml is the main bundle
fixtures contains the files like .gitkeep
resources contains creation of jobs, pipelines like dab_project_job.yml , dab_project_pipeline.yml etc
scratch contains files like exploration.pynb
src contains actual code such as notebook.ipynb, pipeline.ipynb
tests contains coding related to testing such as pytest, unittest

Here , i have deleted the files present in resources, src, tests folder and make them blank
created a notebooks folder in src and created db_git_folders_ingestion_notebook.ipynb


We will create a job named db_git_folders_ingestion_job in databricks from UI, and copy it's json and create a job.yml file in resources/jobs folder

-- so now in the file , we will modify the Workspace path to a relative path
    from:
        notebook_path: /Workspace/Users/hemantbansal1992@gmail.com/databricks_git_folders_demo/databricks_git_folders_proj/src/notebooks/db_git_folders_ingestion_notebook
    to:
        notebook_path: ../../src/notebooks/db_git_folders_ingestion_notebook

We have catalog_name parameter present in the file.

I want to use these from environment variables instead of hardcoding

for that i can create env variables in 2 ways:
  1)  create variables in databricks.yml file
  2)  create a folder called variables and inside that create a file variables.yml and declare variables inside that

so we will refer the variables created in databricks.yml file as:

  base_parameters:
    catalog_name: ${var.catalog_name}

so, we will create a pipeline from databricks UI

so, pipeline creation involves providing catalog, schema name, then starting in python

Structure is as like:

db_git_folders_ingestion_pipeline
    --  explorations
        --  sample_exploration.ipynb
    --  transformations
        --  xyz.ipynb
        --  abc.ipynb
    --  utilities
        --  utils.ipynb
    README.md

so now, we will delete xyz.ipynb and abc.ipynb and create a file in python named as transformation.py
--  write the code and do a dry run of that

point to note that the pipeline is created outside the bundle, so we need to move the root folder of pipeline inside bundle such that we can refer it, we will move it to src/pipelines folder

We will now create a pipelines folder inside resources folder and paste the yaml code of the db_git_folders_ingestion_pipeline inside the pipeline.yml file


After this we wil change the below things:

    from:
        libraries: 
          - glob:
            include: /Workspace/Users/hemantbansal1992@gmail.com/databricks_git_folders_demo/databricks_git_folders_proj/src/pipelines/db_git_folders_ingestion_pipeline/transformations/**
        root_path: /Workspace/Users/hemantbansal1992@gmail.com/databricks_git_folders_demo/databricks_git_folders_proj/src/pipelines/db_git_folders_ingestion_pipeline
        catalog_name: assetbundles
    to:
      libraries: 
          - glob:
            include: ../../src/pipelines/db_git_folders_ingestion_pipeline/transformations/**
      root_path: ../../src/pipelines/db_git_folders_ingestion_pipeline
      catalog_name: ${var.catalog_name}

By default , the preset is set as '[dev my_user_name]' in databricks.yml file
we can change the default behaviour by setting name_prefix parameter in presets
and also can make source_linked_deployment parameter to false such that it can point to resources in other workspace instead of current Workspace
the job is updated now, not created again with the name

add presets for development and production targets in databricks.yml file, also added root_path to have .bundle file in db_git_folders as this is a demo of git folders
    presets:
      name_prefix:  dev_${workspace.current_user.short_name}_
      source_linked_deployment: false
    root_path: /Workspace/Users/hemantbansal1992@gmail.com/db_git_folders/.bundle/${bundle.name}/${bundle.target}


databricks bundle validate --target dev
--  it creates .databricks folder inside databricks_git_folders_proj directory

databricks bundle deploy --target dev
-- it uses the databricks.yml to deploy to dev environment

Building python_artifact...
Uploading dist/databricks_git_folders_proj-0.0.1-py3-none-any.whl...
Uploading bundle files to /Workspace/Users/hemantbansal1992@gmail.com/db_git_folders/.bundle/databricks_git_folders_proj/dev/files...
Deploying resources...
Deployment complete!

Result:

job is created with the name:
  dev_hemantbansal1992_db_git_folders_ingestion_job

pipeline is created with the name:
  dev_hemantbansal1992_db_git_folders_ingestion_pipeline

so here, it creates a folder having structure

db_git_folders
    --  .bundle
        --  databricks_git_folders_proj
            -- dev
                -- artifacts
                    -- .internal
                        -- databricks_git_folders_proj-0.0.1-py3-none-any.whl
                -- files
                    -- .vscode
                    --  fixtures
                    --  src
                    --  resources
                    --  tests
                    --  .gitignore
                    --  databricks.yml
                    --  pyproject.toml
                    --  README.md
                --  state
                    --  deployment.json
                    --  metadata.json
                    --  terraform.tfstate

also, there is a json file in the folder sync_snapshots in .databricks folder which has details about the last modified timestamp of all files


Production deployment:

--  changed the root_path to include PROD folder as well
--  changed the permissions to group level
--  changed the presets to prod_{user_name}_

if we want to override the variables such as catalog_name during deployment and do it for prod, so lets try that

run the command :
databricks bundle deploy --target prod --var="catalog_name=assetbundles_prod"

Output:
Building python_artifact...
Uploading dist/databricks_git_folders_proj-0.0.1-py3-none-any.whl...
Uploading bundle files to /Workspace/Users/hemantbansal1992@gmail.com/db_git_folders/PROD/.bundle/databricks_git_folders_proj/prod/files...
error: assetbundles_prod does not exist

This is good as it working fine as this catalog does not exist

so we need to create a catalog with name assetbundles_prod

and again if we run the command, we will we able to deploy and also job, pipeline is created


job is created with the name:
  prod_hemantbansal1992_db_git_folders_ingestion_job

pipeline is created with the name:
  prod_hemantbansal1992_db_git_folders_ingestion_pipeline
  


databricks bundle summary --target prod
-- it provides a summary of the changes/resources that are going to be deployed

databricks bundle destroy --target prod
-- it destroys the resources that were deployed

we can push these changes to github and merge into main branch
