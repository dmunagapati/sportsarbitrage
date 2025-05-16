
from thread_manager import thread_manager
from accumulator_thread import accumulator
from arb_tracker_thread import ArbTracker
if __name__ == "__main__":
    manager = thread_manager()
    manager.start_threads()

    accumulate = accumulator()
    accumulate.start_accumulator_thread()

    tracker = ArbTracker()
    tracker.update()
     

    