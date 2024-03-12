from stable_baselines3.common.callbacks import BaseCallback

from pynguin.reinforcement.mutablebool import MutableBool


class StoppingCallback(BaseCallback):
    """Callback to manually end training"""
    def __init__(self, stop_training: MutableBool, verbose: int = 0):
        super().__init__(verbose)
        self.stop_training = stop_training

    def _on_step(self) -> bool:
        if self.stop_training.get():
            return False
        else:
            return True
