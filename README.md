(base) devopsx@mahesh:~$ /opt/devopsx/devopsx.sh Starting Devopsx...
Traceback (most recent call last):
File "/opt/devopsx/.venv/bin/devopsx", line 6, in <module>
sys.exit(main())
ΑΑΑΑΑΑ
File "/opt/devopsx/.venv/lib/python3.11/site-packages/click/core.py", line 1157, in __call__ return self.main(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/click/core.py", line 1078, in main rv self.invoke(ctx)
^^^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/click/core.py", line 1434, in invoke return ctx.invoke(self.callback, **ctx.params)
^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/click/core.py", line 783, in invoke return _callback(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/devopsx/devopsx/cli.py", line 168, in main
chat(
File "/opt/devopsx/devopsx/cli.py", line 204, in chat logfile = get_logfile(
^^^^^^^^^^^^File "/opt/devopsx/devopsx/cli.py", line 369, in get_logfile
_, index = pick(options, title) # type: ignore
ΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑ
File "/opt/devopsx/.venv/lib/python3.11/site-packages/pick/__init__.py", line 201, in pick return picker.start()
^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/pick/__init__.py", line 180, in start return curses.wrapper(self._start)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.11/curses/__init__.py", line 94, in wrapper
return func(stdscr, *args, **kwds)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/pick/__init__.py", line 169, in _start return self.run_loop(screen)
^^^^^^^^^^^^^^^^^^^^^
File "/opt/devopsx/.venv/lib/python3.11/site-packages/pick/__init__.py", line 141, in run_loop
self.draw(screen)
File "/opt/devopsx/.venv/lib/python3.11/site-packages/pick/__init__.py", line 132, in draw screen.addnstr(y, x, line, max_x - 2)
Curses.error: addnwstr() returned ERR
