from collections import namedtuple
import heapq


class Controller:
    def __init__(self):
        self._current_time = 0
        self._total_damage = 0
        self._pending_action_queue = _PendingActionQueue()

    def get_total_damage(self):
        return self._total_damage

    def perform_active_action(self, instance, damage, active_time):
        self._total_damage += damage
        self._pending_action_queue.push(instance, self._current_time + active_time)

    def perform_passive_action(self, damage):
        self._total_damage += damage

    def simulate_total_damage(self, character, total_time):
        self._current_time = 0
        self._total_damage = 0
        self._pending_action_queue = _PendingActionQueue()
        self._pending_action_queue.push(character, 0)

        while self._current_time < total_time:
            if self._current_time > self._pending_action_queue.peek().timestamp:
                raise ValueError('Controller time should never be greater than first action timestamp')

            self._current_time = self._pending_action_queue.peek().timestamp
            while self._current_time == self._pending_action_queue.peek().timestamp:
                self._pending_action_queue.pop().instance.run_iteration(self, self._current_time)

        return self._total_damage


class _PendingActionQueue:
    def __init__(self):
        self._instances_in_queue = set()
        self._queue = []

    def push(self, instance, timestamp):
        if (instance is not None) and (instance in self._instances_in_queue):
            raise ValueError(f'Found instance {instance} in queue already, concurrent active actions are not allowed')
        self._instances_in_queue.add(instance)
        # timestamp comes first because heapq checks tuple[0] for sorting
        heapq.heappush(self._queue, _PendingAction(timestamp, instance))

    def peek(self):
        if len(self._queue) == 0:
            raise ValueError('Tried to peek but queue is empty')

        return self._queue[0]

    def pop(self):
        if len(self._queue) == 0:
            raise ValueError('Tried to pop but queue is empty')

        pending_action = heapq.heappop(self._queue)
        if pending_action.instance is not None:
            self._instances_in_queue.remove(pending_action.instance)
        return pending_action


_PendingAction = namedtuple('_PendingAction', ['timestamp', 'instance'])
