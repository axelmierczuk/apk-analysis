import re
from collections import defaultdict

import pandas as pd


class StraceParser:

    def parse_trace(self, file: str) -> pd.DataFrame:
        dataset = []
        pid_pattern = re.compile(r'^\[pid  \d+\] (\d+\.\d+)')  # Pattern to capture the timestamp
        sys_call_pattern = re.compile(r'(\S+)\((.*?)\)')  # Reverting to previous regex
        queues = defaultdict(list)

        with open(file, 'r') as file:
            for line in file:
                pid_match = pid_pattern.match(line)
                if pid_match:
                    timestamp = pid_match.group(1)  # Extracting the timestamp
                    sys_call_with_result = line.split(' ', 4)[4].strip()
                    sys_call_match = sys_call_pattern.search(sys_call_with_result)

                    if sys_call_match:
                        sys_call_command = sys_call_match.group(1)
                        sys_call_arguments = self.parse_sys_call_arguments(sys_call_with_result)
                        sys_call_arguments_count = len(sys_call_arguments)
                        sys_call_arguments_contains_path = any('/' in arg for arg in sys_call_arguments)

                        result_match = re.search(r' = (.*?)(\n|$)', sys_call_with_result)
                        sys_call_result = result_match.group(1) if result_match else None
                        sys_call_result_ok = sys_call_result == '0' if sys_call_result else False
                        sys_call_result_interpreted = False
                        sys_call_return_address = False

                        # Check for interpreted result only if result is not None
                        if sys_call_result:
                            interpreted_match = re.search(r'\((.*?)\)', sys_call_result)
                            if interpreted_match:
                                sys_call_result_interpreted = True

                            # Check for return address
                            if re.match(r'^0x[a-fA-F0-9]{12}$', sys_call_result):
                                sys_call_return_address = True

                        if not sys_call_command.isalnum():
                            continue
                        dataset.append({
                            'timestamp': timestamp,
                            'sys_call': sys_call_command,
                            'sys_call_command': sys_call_with_result,
                            'sys_call_result': sys_call_result,
                            'sys_call_result_ok': sys_call_result_ok,
                            'sys_call_result_interpreted': sys_call_result_interpreted,
                            'sys_call_return_address': sys_call_return_address,
                            'sys_call_arguments': sys_call_arguments,
                            'sys_call_arguments_count': sys_call_arguments_count,
                            'sys_call_arguments_contains_path': sys_call_arguments_contains_path
                        })
                    else:
                        # Handling unfinished system calls
                        call_ = sys_call_with_result.split('(')[0]
                        if "<unfinished ..." in line:
                            queues[call_].append({
                                'timestamp': timestamp,
                                'sys_call_with_result': sys_call_with_result
                            })
        return pd.DataFrame(dataset)

    @staticmethod
    def parse_sys_call_arguments(sys_call_str):
        if '(' not in sys_call_str or ')' not in sys_call_str:
            return []

        args = []

        # Extracting the substring that contains the arguments
        args_str = sys_call_str.split('(', 1)[1].rsplit(')', 1)[0].strip()

        if len(args_str) == 0:
            return []

        args_split = args_str.split(', ')
        array_aggregation = False
        tmp_array = []
        for arg in args_split:
            if arg.startswith('[') or arg.startswith('{'):
                array_aggregation = True
                tmp_array = [arg]
            elif arg.endswith(']') or arg.endswith('}'):
                array_aggregation = False
                tmp_array.append(arg)
                args.append(''.join(tmp_array))
            elif array_aggregation:
                tmp_array.append(arg)
            else:
                args.append(arg)
        return args


if __name__ == '__main__':
    parser = StraceParser()
    res = parser.parse_trace(file="../../dataset/CICMalAnal2017/dynamic-dataset/logs/3-0034344c31f7b8812bc980d67ebd8dfec951d98d5786eb201f3ccfeca427cc54.trace")
    print(res)



