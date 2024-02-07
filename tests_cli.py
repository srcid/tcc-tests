import argparse
import sys
from logging import DEBUG, basicConfig, debug
from pathlib import Path

from dotenv import load_dotenv

from heuristics.chrobak import chrobak
from models.common_blocks import CommonBlocks
from models.common_substring import CommonSubstring
from models.mcsp import MCSP
from spreadsheet.google_spreadsheet import GoogleSpreadsheet

load_dotenv()

class TestsCLI:
    CLI_VERSION='0.0.1'

    def __init__(self) -> None:
        self.spreadsheet = None
        self.__run()

    def __run(self):

        self.parser = argparse.ArgumentParser(
            prog='TestsCLI',
            description='CLI to run my graduation degree thesis tests',
            epilog='Desenvolvido por srcid'
        )

        self.parser.version = self.CLI_VERSION
        self.parser.add_argument('-v', '--version', action='version')
        self.parser.add_argument('--verbose', action='store_true')
        
        self.parser.add_argument('--local', action='store_true',
                help='Don\'t send send the results to spreadsheets, just print it to stdout')
        self.parser.add_argument('--dry-run', action='store_true', 
                help='Don\'t run the tests, only log')
        self.parser.add_argument('--limit', type=int,
                help='Time limit in milliseconds')
        
        self.parser.add_argument('-m', '--models', type=str, required=True,
                choices=['cb', 'cs'], nargs='+',
                help='Defines which model should be used for resolve MCSP problem instances')
        self.parser.add_argument('-g', '--group', type=str, required=True,
                choices=['1','2','3','real', 'myrandom', 
                         *map(lambda x: 'article' + str(x),range(1,9))],
                help='Defines which group of test cases should be used')
        self.parser.add_argument('-c', '--cases', type=int, nargs='*',
                help='Defines which instances should run for testing')
        self.parser.add_argument('-n', '--num-executions', type=self.__check_num_executions,
                required=True, help='Define how many times a instance should execute')
        self.parser.add_argument('-s','--solvers', type=str, required=True,
                nargs='+', choices=['CPLEX','GUROBI','SCIP','CBC'],
                help='Defines which solvers should be used')
        self.parser.add_argument('--heuristic', type=str, choices=['chrobak'],
                help="Set a heuristic to be used as warm start")

        self.args = self.parser.parse_args()

        if self.args:
            groupsPath = {
                '1': Path('./instancesMCSP/random/Dataset_Group01'),
                '2': Path('./instancesMCSP/random/Dataset_Group02'),
                '3': Path('./instancesMCSP/random/Dataset_Group03'),
                'real': Path('./instancesMCSP/real'),
                'myrandom': Path('./instancesMCSP/myrandom'),
                'article1': Path('./instancesMCSP/article1'),
                'article2': Path('./instancesMCSP/article2'),
                'article3': Path('./instancesMCSP/article3'),
                'article4': Path('./instancesMCSP/article4'),
                'article5': Path('./instancesMCSP/article5'),
                'article6': Path('./instancesMCSP/article6'),
                'article7': Path('./instancesMCSP/article7'),
                'article8': Path('./instancesMCSP/article8'),
            }
            heuristics = {
                'chrobak': chrobak
            }

            models: list[str] = self.args.models
            group: str = self.args.group
            num_executions: int = int(self.args.num_executions)
            solvers: list[str] = self.args.solvers
            limit: int = self.args.limit
            heuristic_name: str = self.args.heuristic
            heuristic = heuristics.get(heuristic_name)
            
            if self.args.verbose:
                basicConfig(level=DEBUG)
            
            if not self.args.local:
                self.spreadsheet = GoogleSpreadsheet()
            
            for instance in filter(self.__is_in_cases, groupsPath[group].glob('*.dat')):
                debug(f'Testing instance {instance.name}')
                with instance.open('r') as file:
                    lines = file.readlines()
                    S1 = lines[4].strip()
                    S2 = lines[5].strip()
                    file.close()

                for model in models:
                    if (model == 'cb'):
                        debug('Instantiate Common Blocks model')
                        mcsp: MCSP = CommonBlocks(S1, S2)
                    else:
                        debug('Instantiate Common Substring model')
                        mcsp: MCSP = CommonSubstring(S1,S2)

                    for solverName in solvers:
                        debug(f'Using solver {solverName}')
                        for i in range(num_executions):
                            debug(f'Running {i} of {num_executions} tests')
                            
                            if self.args.dry_run:
                                val, time, val_status = -1.0, -1, -1
                            else:
                                val, time, val_status = mcsp.solve(
                                    solverName, 
                                    limit, 
                                    heuristic
                                )
                            
                            if self.args.local:
                                print(f'{instance.name},{model},{mcsp.N},' + 
                                      f'{val},{time},{solverName},{val_status}')
                            else:
                                groupName = group
                                if heuristic is not None:
                                    groupName += '_' + heuristic_name
                                self.spreadsheet.appendRow(
                                    groupName = groupName,
                                    instance=instance.name,
                                    model=model,
                                    size=mcsp.N,
                                    val=val,
                                    time=time,
                                    solver=solverName,
                                    val_status=val_status)
        else:
            self.parser.print_help()
            sys.exit(1)

    def __is_in_cases(self, instance):
        if self.args.cases == None:
            return True
        for case in self.args.cases:
            if instance.name.find(str(case)) != -1:
                return True
        return False
    
    def __check_num_executions(self, arg):
        n = int(arg)
        if n < 1:
            raise argparse.ArgumentTypeError(
                'Number of executions should be a integer greater then zero'
            )
        return n


if __name__ == '__main__':
    testCLI = TestsCLI()