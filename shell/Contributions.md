## Contributions

This lab was done mostly based off the code provided from Professor
Freudenthal. The structure of the redirection was based of his
p4-redirection.py file and the pipe part of the lab was mostly based off of
his p5-pipe-fork.py file.


### Web

The page that I used was for os.pipe()
* https://www.tutorialspoint.com/python/os_pipe.htm
This page helped me understand how it is that os.pipe() returns two ints with
the newly opened file descriptors


### Contribution with classmate

This lab was done in contribution with Michael Baca.

* We helped each other understand what the symbols "<, >, and |" are actually
  doing in the command

* We figured out that input redirection is simply a modification of output
  redirection and asking for input once the file descriptor 0 has been changed

* In the piping part of the lab, we determined that dup2 somehow worked better
  than dup since dup2 duplicates the wanted file descriptor AND closes the
  undesired one at the same time.

* In the piping section of this lab, once the output of one prog has been sent
  to the pipe then the input of the next process is redirected to the output
  of the pipe and the program is executed.
