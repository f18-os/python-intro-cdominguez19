## Description

This lab was meant to show us how to make a simple shell using io redirection
and pipes. This lab was centered around the fork, wait, and exec processes. We
needed to know how to fork, when to wait, when to execute, and when to fork
another child as is with the pipe section of this lab.


## Code

The entire code is looped infinately in order to present the user with a
prompt (p>>). I then created different if statements in order to handle input
redirection, one to handle output redirection, and another to handle piping


## How to Run

To run program...

```
`$ python3 shell.py
```
To terminate program, a Ctrl-d is necessary to send EOFException


## Bugs

I was not able to handle the PS1 environment variable. Other than that io
redirection worked properly with the input I gave my prompt. The piping part
of the lab did not work correctly. Everything was piped properly with two
children but it did not print out to the screen (stdout) until the program was
terminated with ctrl-d.

```
p>> cat test.py | wc
```
