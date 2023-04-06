import argparse
import sys
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv

from models.common_blocks import CommonBlocks
from models.common_substring import CommonSubstring
from models.mcsp import MCSP
from spreadsheet.google_spreadsheet import GoogleSpreadsheet

load_dotenv()

class TestsCLI:
    CLI_VERSION='0.0.1'

    def __init__(self) -> None:
        self.spreadsheet = GoogleSpreadsheet()
        self.__run()

    def __run(self):

        self.parser = argparse.ArgumentParser(
            prog='TestsCLI',
            description='CLI to run my graduation degree thesis tests',
            epilog='Desenvolvido por srcid'
        )

        self.parser.version = self.CLI_VERSION
        self.parser.add_argument('-v', '--version', action='version')
        
        self.parser.add_argument('--local', action='store_true',
                help='Don\'t send send the results to spreadsheets, just print it to stdout')
        self.parser.add_argument('--dry-run', action='store_true', 
                help='Don\'t run the tests, only log')
        self.parser.add_argument('--limit', type=int, default=1800000,
                help='Time limit in milliseconds')
        
        self.parser.add_argument('-m', '--models', type=str, required=True,
                choices=['cb', 'cs'], nargs='+',
                help='Defines which model should be used for resolve MCSP problem instances')
        self.parser.add_argument('-g', '--group', type=str, required=True,
                choices=['1','2','3','real'],
                help='Defines which group of test cases should be used')
        self.parser.add_argument('-c', '--cases', type=int, nargs='*',
                help='Defines which instances should run for testing')
        self.parser.add_argument('-n', '--num-executions', type=self.__check_num_executions,
                required=True, help='Define how many times a instance should execute')
        self.parser.add_argument('-s','--solvers', type=str, required=True,
                nargs='+', choices=['CPLEX','GUROBI','SCIP','CBC'],
                help='Defines which solvers should be used')

        self.args = self.parser.parse_args()

        if self.args:
            models: str = self.args.models
            group: str = self.args.group
            num_executions: int = int(self.args.num_executions)
            solvers: list = self.args.solvers
            limit: int = int(self.args.limit)
            groupsPath = {
                '1': Path('./instancesMCSP/random/Dataset_Group01'),
                '2': Path('./instancesMCSP/random/Dataset_Group02'),
                '3': Path('./instancesMCSP/random/Dataset_Group03'),
                'real': Path('./instancesMCSP/real')
            }
            results_file = Path('./results.csv').open('a')
            
            for instance in filter(self.__is_in_cases, groupsPath[group].glob('*.dat')):
                print(f'Testando instância {instance.name}')
                with instance.open('r') as file:
                    lines = file.readlines()
                    S1 = lines[4].strip()
                    S2 = lines[5].strip()
                    file.close()

                for model in models:
                    if (model == 'cb'):
                        print('Iniciando modelo Common Blocks')
                        mcsp: MCSP = CommonBlocks(S1, S2)
                    else:
                        print('Iniciando modelo Common Substring')
                        mcsp: MCSP = CommonSubstring(S1,S2)

                    for solverName in solvers:
                        print(f'Usando o solver {solverName}')
                        for i in range(num_executions):
                            print(f'Executando {i} de {num_executions} teste')
                            
                            if self.args.dry_run:
                                val, time, val_status = -1.0, -1, -1
                            else:
                                val, time, val_status = mcsp.solve(solverName, limit)
                            
                            if self.args.local:
                                pprint({"instance": instance.name,
                                        "model": model,
                                        "size": mcsp.N,
                                        "val": val,
                                        "time": time,
                                        "solver": solverName,
                                        'status': val_status})
                            else:
                                self.spreadsheet.appendRow(
                                    groupName = group,
                                    instance=instance.name,
                                    model=model,
                                    size=mcsp.N,
                                    val=val,
                                    time=time,
                                    solver=solverName,
                                    val_status=val_status)
                            
                            results_file.write(f'{instance.name},{model},{mcsp.N},{val},{time},{solverName},{val_status}\n')
            results_file.close()
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