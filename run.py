from app import create_app
from threading import Thread

app = create_app()

from app.controllers.signal_controller import SignalController

signal = SignalController()
signal_th = Thread(target=signal.mainloop, args=(app,))
sltp_th = Thread(target=signal.sltp_loop, args=(app,))
signal_th.start()
sltp_th.start()

app.run()

