

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



        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Mingo.PS5RemotePlay")
    except Exception:
        pass
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("PS5RemotePlay by Mingo")
    from ps5rp import theme
    app.setStyleSheet(theme.STYLE)
    app.setWindowIcon(theme.app_icon())
    try:
        from ps5rp.engine import Engine
        from ps5rp.main_window import MainWindow
        settings = cfg.Settings.load()
        engine = Engine(settings)
        win = MainWindow(settings, engine)
        win.show()
    except Exception:
        log.exception("startup failed")
        QtWidgets.QMessageBox.critical(None, "PS5 Remote Play",
                                       "Startup failed:\n\n" + traceback.format_exc()[-1500:] + f"\nLog: {cfg.LOG_FILE}")
        return 1
    return app.exec()

def _gl_format(QtGui):
    f = QtGui.QSurfaceFormat()
    f.setSwapInterval(1)
    return f

if __name__ == "__main__":
    sys.exit(main())
