import os
from pathlib import Path


class ExperimentBuilder:
    def __init__(self, script, dataset, defaults, devices):
        """
        @param script: path to script, rooted in home directory (it's automatically inserted as prefix)
        @param dataset: absolute path to dataset folder
        @param defaults: default cmd arguments that usually stay fixed
        @param devices: value to initialize CUDA_VISIBLE_DEVICES env variable
        """
        self.script = os.path.join(str(Path.home()), script)
        os.environ['CUDA_VISIBLE_DEVICES'] = devices
        self.add_param('dataset_path', dataset)
        for k, v in defaults:
            self.add_param(k, v)

    def add_param(self, name, value):
        if isinstance(value, list):
            value = ' '.join(map(str, value))
        setattr(self, f'_{name}', value)

    def run(self, exp_folder, exp_name):
        save_folder = os.path.join(str(Path.home()), exp_folder, exp_name)
        log_file_path = os.path.join(save_folder, f'output_{exp_name}.txt')

        os.makedirs(save_folder, exist_ok=True)

        self.add_param('save', save_folder)
        self.add_param('log_file_path', log_file_path)

        os.system('clear')
        os.system(self._build_command())

    def _build_command(self):
        cvd = 'CUDA_VISIBLE_DEVICES'
        params = ' '.join(
            [f'--{k} {v}'
             for k, v in self.__dict__.items()
             if k.startswith('_')]).replace('--_', '--')
        return f'{cvd}={os.environ[cvd]} python {self.script} {params}'

    def __getattr__(self, item):
        return self.__dict__[f'_{item}']
