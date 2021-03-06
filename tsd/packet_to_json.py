import json
import struct
from collections import defaultdict

def bin_to_hex(bin_str):
    n = struct.unpack('<' + str(len(bin_str)) + 'B', bin_str)
    return ''.join(['/' + hex(v)[1:] for v in n])

def pkt_to_json(pkt):
    results = defaultdict(dict)
    results['_time_'] = pkt.time * 1000

    raw_pkt = pkt

    try:
        for index in range(50):
            layer = raw_pkt[index]
            layer_len = len(layer)

            # Get layer name
            layer_tmp_name = str(layer.aliastypes[0])
            layer_start_pos = layer_tmp_name.rfind(".") + 1
            layer_name = layer_tmp_name[layer_start_pos:-2].lower()

            # Get the layer info
            # tmp_t = {}
            # for x, y in layer.default_fields.items():
            #     if y and not isinstance(y, (str, int, long, float, list, dict)):
            #         tmp_t[x].update(pkt_to_json(y))
            #     else:
            #         tmp_t[x] = repr(y)
            # results[layer_name] = tmp_t

            try:
                tmp_t = {}
                for x, y in layer.fields.items():
                    if y and not isinstance(y, (unicode, str, int, long, float, list, dict)):
                        tmp_t[x].update(pkt_to_json(y))
                    elif y is None:
                        continue
                    elif x == 'load':
                        if len(y) > 200:
                            continue    # not support big raw load now.
                        else:
                            tmp_t[x] = repr(y)
                    elif isinstance(y, unicode):
                        tmp_t[x] = y
                    elif isinstance(y, str):
                        try:
                            y.decode('utf-8')
                            tmp_t[x] = y
                        except UnicodeDecodeError:
                            tmp_t[x] = repr(y)
                            pass
                    else:
                        tmp_t[x] = repr(y)

                results[layer_name] = tmp_t
            except KeyError:
              # No custom fields
                pass
            results[layer_name]['_len_'] = layer_len
            results[layer_name]['_idx_'] = index
    except IndexError:
        # Package finish -> do nothing
        # raise
        pass

    return json.dumps(results)

def PacketsToJson(pkts):
    json_str = '['
    pkts_len = len(pkts)
    for i in xrange(pkts_len):
        json_str += pkt_to_json(pkts[i])
        if i != pkts_len - 1:
            json_str += ','
    json_str += ']'
    # print json_str
    return json_str







