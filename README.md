# DTU HPC

DTU HPC is a collection of scripts and tools for running jobs on the DTU HPC cluster.
It should help you to get started with running jobs on the cluster, and to make your life easier.

## Installation

To install just run:

```bash
pip install dtuhpc
```

## Getting started

To get started you first need to run:

```bash
dtuhpc auth
```

It will ask you for your username and password for DTU, and it will then
ask you for an encryption password. This password is used to encrypt your
DTU password, so that it can be stored on your computer. You will need to
remember this password, as it is used to decrypt your password when you
run commands.

Afterwards, you should create a configuration file for your project. This
should be named `.dtuhpc.toml` and should be placed in the root of your project.
You can use the following template:

```toml
[ssh]
user = "<username>"
host = "<login-host>"
default_cwd = "<default working directory>"
key_filename = "<path to ssh key>"

[github]
access_token = "<github access token>"

[project]
name = "<project name>"
path = "<path to project on cluster>"
default_deploy_branch = "master"
```

The `ssh` section is used to configure the ssh connection to the cluster.
The GitHub access token can be generated from the following [page](https://github.com/settings/tokens).

### Setup project

To set up a project, you can run:

```bash
dtuhpc init [--poetry] [--custom-job=<path to job script>]
```

This will dispatch a job to the cluster, which will clone your project, create a
virtual environment, and install the dependencies.
You can choose to use either poetry, pip, or a custom job script. How to define jobs
will be explained in the next section.

### Writing jobs

Jobs are defined as toml files. It contains numerous options:

```
name = "<name of job>"
queue = "<queue name>"
single_host = <true/false>
walltime = { hours = <hours>, minutes = <minutes> }
standard_output = "<path to standard output file>"
error_output = "<path to error output file>"
memory = <memory to allocate>
memory_kill_limit = <memory kill limit>
cores = <number of cores to allocate>
email = "<email address>"
notification_start = <true/false>
notification_end = <true/false>
core_block_size = <core block size>
core_p_tile_size = <core p tile size>
use_gpu = { num_of_gpus = <number of gpus>, per_task = <true/false> }

commands = [
    "<bash command 1>",
    "<bash command 2>",
    ...
]
```

An example of a script can be seen here:

```toml
queue = "hpc"
name = "init_${{ project_name }}"
walltime = { hours = 0, minutes = 15 }
single_host = true
cpu = 2
memory = 4
standard_output = "init_${{ project_name }}.out"
error_output = "init_${{ project_name }}.err"

commands = [
    "git clone ${{ git_url }} ${{ project_path }}",
    "module load python3/3.10.7",
    "cd ${{ project_path }}",
    "python3 -m venv ${{ project_path }}/venv",
    "source ${{ project_path }}/venv/bin/activate",
    "pip3 install 'poetry==1.3.2'",
    "poetry install",
]
```

In this script, we can see that we can use variables in the script. These variables
are some default ones that are only available for the `init` job.

### Deploying jobs

To deploy a job you just run the following command:

```bash
dtuhpc deploy <job_path>
```

It will then ask you to pick from branches or PR's. It will then dispatch the job
to the cluster.

### Other commands

Some other commands:

#### Exec commands on cluster

To execute commands on the cluster, you can run:

```bash
dtuhpc exec '<command to run>'
```

It will run in the default working directory, which is defined in the configuration file.

#### SSH into cluster

To ssh into the cluster, you can run:

```bash
dtuhpc ssh
```

It will then open an ssh connection to the cluster. From here you can run commands
as you would normally.

#### Predefined subcommands

There are also some predefined subcommands, which are just wrappers around the
cluster commands. They are all prefixed by `dtuhpc c <command_name>`. To get the
full documentation for the commands, you can run:

```bash
dtuhpc c <command_name> --help
```

##### bkill

Kill a job on the cluster.

```bash
dtuhpc c bkill <job_id>
```

##### bqueues

List all queues on the cluster.

```bash
dtuhpc c bqueues
```

##### bstat

Get the status of a job on the cluster.

```bash
dtuhpc c bstat <optional job_id>
```

##### bsub

Submit a job to the cluster.

```bash
dtuhpc c bsub <path to job script>
```

##### nodestat

Get the status of the nodes on the cluster.

```bash
dtuhpc c nodestat
```

##### showstart

Show the start time of a job on the cluster.

```bash
dtuhpc c showstart <job_id>
```
