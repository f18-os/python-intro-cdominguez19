#! /usr/bin/env python3

import os, sys, time, re, subprocess

while True:

    uIn = input("p>>")

    uIn.strip()
    uIn2 = uIn.split()

    if len(uIn2) < 3:
        print("Invalid command")

    if len(uIn2) == 3:
        rc0 = os.fork()
        if rc0 == 0:#input redirection file with name of another file
            args = [uIn2[0]]#command to execute
            os.close(0)
            sys.stdin = open(uIn2[2],"r")#open file containing name of another file
            rFile = input()
            args.append(rFile)
            fd = sys.stdin.fileno()
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for reading\n"%fd).encode())

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)#try and execute program
                except FileNotFoundError:
                    pass

            os.write(2, ("Error: Could not exec%s\n"%args[0]).encode())
            sys.exit(1)

        else:                           # parent (forked ok)
            childPidCode = os.wait()#wait for  child to execute
    elif len(uIn2) == 4:
        if uIn2[2] == ">":#output redirection into file
            rc1 = os.fork()

            if rc1 == 0:                   # child
                args = [uIn2[0], uIn2[1]]#take command with file
                os.close(1)                 # redirect child's stdout
                sys.stdout = open(uIn2[3], "w")#open file for new output
                fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
                os.set_inheritable(fd, True)
                os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

                for dir in re.split(":", os.environ['PATH']): # try each directory in path

                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass                              # ...fail quietly 

                os.write(2, ("Error: Could not exec %s\n" % args[0]).encode())
                sys.exit(1)                 # terminate with error

            else:
                childPidCode = os.wait()

        elif uIn2[2] == "|":
            pid = os.getpid()               # get and remember pid
            i, o = os.pipe()#pipe on parent
            os.set_inheritable(i,True)#let children inherit new fd
            os.set_inheritable(o,True)
            rc1 = os.fork()#fork first child
            #rc2 = os.fork()
            if rc1 == 0:
                os.dup2(o,1)#switch fd
                os.close(i)#close unused fd
                args = [uIn2[0], uIn2[1]]
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s"%(dir,args[0])
                    try:
                        os.execve(program, args, os.environ)#try to exec prog
                    except FileNotFoundError:
                        pass
                    #returning to parent
                sys.exit(0)
            rc2 = os.fork()#fork second child
            if rc2 == 0:
                os.dup2(i,0)#duplicate fd
                os.close(o)#close unused fd
                fo = input()#get input off of pipe queue &&&&& BUG: ONLY GETTING ONE LINE &&&&&&&&
                fo.strip()
                f = open("temp.txt","w")#putting into a temp file 
                f.write(fo)
                f.close()
                args2 = [uIn2[3]]#piped into new command
                args2.append("temp.txt")
                for dir in re.split(":", os.environ['PATH']):
                    program2 = "%s/%s"%(dir,args2[0])
                    try:
                        os.execve(program2, args2, os.environ)#try to execute the prog
                    except FileNotFoundError:
                        pass
                sys.exit(0)

#else:&&&&&&&&&&& UNUSED CODE &&&&&&&&&&&&&&&
    #at parent about to fork to second child child above ...
    #should have placed input into pipe queue...
    #now must extract it as input for new child.
    #os.wait()
    #rc2 = os.fork()
