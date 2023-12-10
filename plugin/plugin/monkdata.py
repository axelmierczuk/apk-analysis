class MonkParser:
    def parse_monk_data(self, file: str):
        print(f'[monk-parser] Evaluating: {file}')
        f = open(file, 'r')
        data = f.readlines()
        f.close()

        if len(data) == 0:
            return {'elapsed': 0, 'mobile': 0, 'wifi': 0, 'not_connected': 0, 'error': True}
        if data[-1] != ('// Monkey finished\n'):
            return {'elapsed': 0, 'mobile': 0, 'wifi': 0, 'not_connected': 0, 'error': True}

        network_data = data[-2].split('## Network stats: elapsed time=')[-1]
        network_data_split = network_data.split('ms (')
        elapsed = int(network_data_split[0])
        network_details = network_data_split[-1]
        mobile_s = network_details.split('ms mobile, ')
        mobile = int(mobile_s[0])
        wifi_s = mobile_s[-1].split('ms wifi, ')
        wifi = int(wifi_s[0])
        not_connected_s = wifi_s[-1].split('ms not connected)')
        not_connected = int(not_connected_s[0])

        return {'elapsed': elapsed, 'mobile': mobile, 'wifi': wifi, 'not_connected': not_connected, 'error': False}






