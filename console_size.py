# Gratefully taken from http://stackoverflow.com/a/6550596, for the question http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python.
# Question author: http://stackoverflow.com/users/26592/umnik700; answer author: http://stackoverflow.com/users/825214/harco-kuppens.
# Provided under the Attribution-ShareAlike 3.0 Unported license - http://creativecommons.org/licenses/by-sa/3.0/legalcode.
# I have modified _getTerminalSize_windows, to always return 79, as this seems to be the maximum (and default) number of columns used by the command prompt.

__all__=['getTerminalSize']


def getTerminalSize():
   import platform
   current_os = platform.system()
   tuple_xy=None
   if current_os == 'Windows':
       tuple_xy = _getTerminalSize_windows()
       if tuple_xy is None:
          tuple_xy = _getTerminalSize_tput()
          # needed for window's python in cygwin's xterm!
   if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
       tuple_xy = _getTerminalSize_linux()
   if tuple_xy is None:
       print("default")
       tuple_xy = (80, 25)      # default value
   return tuple_xy

def getCurrentOS():
   import platform
   current_os = platform.system()
   return current_os
   
def _getTerminalSize_windows():
    return 79

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
       import subprocess
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

if __name__ == "__main__":
    sizex,sizey=getTerminalSize()
    print('width =',sizex,'height =',sizey)
