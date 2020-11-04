#!/usr/bin/env python
from pwn import *

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11664)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript + 'init-gef\ncontext', *a, **kw)
    elif args.QIRA:
        return connect('127.0.0.1', 4000)
    else:
        return process([exe.path] + argv, *a, **kw)

def python_aaaa(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    python_bbb = connect(host, port)
    if args.GDB:
        gdb.attach(python_bbb, gdbscript=gdbscript)
    return python_bbb

def start(argv=[], *a, **kw):
    def start2(argv=[], *a, **kw):
        '''Start the exploit against the target.'''
        if args.LOCAL:
            return local(argv, *a, **kw)
        else:
            return python_aaaa(argv, *a, **kw)
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return python_aaaa(argv, *a, **kw)

