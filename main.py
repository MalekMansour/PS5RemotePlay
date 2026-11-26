"""PS5 Remote Play - entry point. Sets up crash protection, then starts the Qt app."""
import faulthandler
import logging
import os
import sys
import threading
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "shim")) 
sys.path.insert(0, HERE)

from ps5rp import settings as cfg 

cfg.setup_logging()
log = logging.getLogger("main")
_crash = open(cfg.CRASH_FILE, "a", encoding="utf-8")
faulthandler.enable(_crash)  

def _hook(exc_type, exc, tb):
    log.error("Unhandled exception", exc_info=(exc_type, exc, tb))


sys.excepthook = _hook
threading.excepthook = lambda a: log.error("Thread exception", exc_info=(a.exc_type, a.exc_value, a.exc_traceback))


def _boost_priority() -> None:
    """Streaming is time-critical: run above normal so Discord/OBS capture can't starve it."""
    try:
        import psutil
        psutil.Process().nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
    except Exception:
        log.info("could not raise priority", exc_info=True)



def _gl_format(QtGui):
    f = QtGui.QSurfaceFormat()
    f.setSwapInterval(1)
    return f


if __name__ == "__main__":
    sys.exit(main())
