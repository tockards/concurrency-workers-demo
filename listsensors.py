import re
from redis import StrictRedis
import json
from sys import argv

redis_client = StrictRedis(host='127.0.0.1', port=6379, db=1)
SENSOR_READING_KEYS = ['name', 'time', 'value_ts', 'status', 'value']



def list_sensors(components, name_filter, reading_only):
    try:
        re_pattern = re.compile(name_filter)
        if components == 'all':
            components = []
            for item in redis_client.scan_iter('sensor:*'):
                components.append(item.split('sensor:')[1])
        else:
            components = components.split(',')

        results = {}
        match_pattern = '*:*'
        for component in components:
            component_key = 'sensor:' + component
            for item in redis_client.hscan_iter(
                    component_key, match_pattern):
                key, value = item
                sensor_name = key.split(':')[-1]
                # attr:* keys are stored as attr:<component>_<sensor_name>
                # while read:* keys are stored as read:<sensor_name>
                if key.startswith('attr'):
                    search_sname = sensor_name
                else:
                    search_sname = '{}_{}'.format(component, sensor_name)
                if not name_filter or re_pattern.search(search_sname):
                    loaded_sensor = json.loads(value)
                    if key.startswith('read') and search_sname in results:
                        # update an existing attr key with the reading's value
                        results[search_sname].update(loaded_sensor)
                    elif key.startswith('attr') and search_sname in results:
                        # update an existing read key with the attr
                        loaded_sensor.update(results[search_sname])
                        results[search_sname] = loaded_sensor
                    else:
                        results[search_sname] = loaded_sensor

                    if reading_only:
                        reading_only_dict = {}
                        # repack the cache item as only a reading
                        for reading_key in SENSOR_READING_KEYS:
                            reading_only_dict[reading_key] = results[
                                search_sname][reading_key]
                        results[search_sname] = reading_only_dict

                    results[search_sname]['component'] = component

        return results.values()
    except Exception as exc:
        print(exc)
        #print('Error listing sensors for {}'.format(component))

print (list_sensors("all","^{}*".format(argv[1]), '1'))