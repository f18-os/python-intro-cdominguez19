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
            pr, pw = os.pipe()
            os.set_inheritable(pr,True)
            os.set_inheritable(pw,True)
            rc1 = os.fork()
            import fileinput
            if rc1 == 0:
                args3 = [uIn2[0],uIn2[1]]
                os.close(1)
                os.dup2(pw,1)
                os.close(pr)
                os.close(pw)
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s"%(dir,args3[0])
                    try:
                        os.execve(program, args3, os.environ)
                    except FileNotFoundError:
                        pass
                    #returning to parent
                sys.exit(0)
            cpid = os.wait()
            rc2 = os.fork()
            if rc2 == 0:
                args4 = [uIn2[3]]
                os.close(0)
                os.dup2(pr,0)
                os.close(pw)
                os.close(pr)
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s"%(dir,args4[0])
                    try:
                        os.execve(program, args4, os.environ)
                    except FileNotFoundError:
                        pass
                #print()
                sys.exit(0)
            #else:
                #cpid2 = os.wait()
                #sys.exit(0)


#else:&&&&&&&&&&& UNUSED CODE &&&&&&&&&&&&&&&
    #at parent about to fork to second child child above ...
    #should have placed input into pipe queue...
    #now must extract it as input for new child.
    #os.wait()
    #rc2 = os.fork()
