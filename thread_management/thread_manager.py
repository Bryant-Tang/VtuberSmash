from threading import Thread
from typing import Any, Callable, Iterable, List, Mapping, Union
from decorator import singleton


@singleton
class ThreadManager:
    _running_func: List[Thread]

    def __init__(self) -> None:
        self._running_func = []

    def run_func_as_new_thread(self, target: Union[Callable, None] = None, args: Iterable = (), kargs: Union[Mapping[str, Any], None] = {}):
        if target != None:
            self._running_func.append(target)
            Thread(target=self._start_thread_with_thread_end_record,
                   args=[target, args, kargs]).start()

    def _start_thread_with_thread_end_record(self, target: Callable, args: Iterable = (), kargs: Union[Mapping[str, Any], None] = {}):
        target(*args, **kargs)
        self._running_func.remove(target)

    def is_all_thread_end(self):
        return len(self._running_func) == 0
