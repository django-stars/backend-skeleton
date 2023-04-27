# {{ cookiecutter.project_name }}: Commands #

There is multiple commands to run, test, check etc. 
We use `Makefile` to run them, as it is easy to use and understand, 
and it is a standard way to run commands in Unix-like systems.

In `api` directory you can find `Makefile` with all commands related to the `api`. Fill free to add any new 
useful command for you. If you're planing to have client side, you can add `Makefile` to the `client` directory.

On the root directory you can find `Makefile` with all commands related to the project in general and kind of proxy 
commands to the `api` commands with `api` prefix. 
