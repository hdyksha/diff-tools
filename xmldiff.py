import sys
import xml.etree.ElementTree as ET

from util import json_util
from util import str_util


def xml_to_json(xml):
    jsonised_xml = {}
    root = ET.fromstring(xml)

    def explore_each(xml_root, key_list):
        # ignore mixed contents
        tag = xml_root.tag
        attr = (' ' + ','.join(['='.join(x) for x in xml_root.attrib.items()])
                if xml_root.attrib else "")

        children = list(xml_root)
        if len(children) != 0:
            for child in children:
                explore_each(child, key_list + [tag+attr])
        else:
            key = '<' + '><'.join(key_list + [tag+attr]) + '>'
            val = xml_root.text or ""
            jsonised_xml[key] = val

    explore_each(root, [])
    return jsonised_xml


def compare_joined_jsonized_xml(joined):
    for key, val in joined.items():
        val_A, val_B = val
        if val_A != val_B:
            diffs = []
            if val_A is None:
                diffs.append(str_util.colorize('+ tag: ' + key, 'green'))
                if val_B:
                    diffs.append(str_util.colorize(
                        '+ data: ' + str(val_B), 'green'))
            elif val_B is None:
                diffs.append(str_util.colorize('- tag: ' + key, 'red'))
                if val_A:
                    diffs.append(str_util.colorize(
                        '- data: ' + str(val_A), 'red'))
            else:
                diffs.append('tag: ' + key)
                diffs.append(str_util.colorize(
                    "- data: " + str(val_A), 'red'))
                diffs.append(str_util.colorize(
                    "+ data: " + str(val_B), 'green'))

            print('\n'.join(diffs))
            print("---")


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 3:
        print("Usage: python {} A.xml B.xml".format(argvs[0]))
        sys.exit(1)

    _, xml_file_A, xml_file_B = argvs
    with open(xml_file_A) as f:
        xml_A = f.read()
    with open(xml_file_B) as f:
        xml_B = f.read()

    jsonised_xml_A = xml_to_json(xml_A)
    jsonised_xml_B = xml_to_json(xml_B)
    joined = json_util.join_json_by_key(jsonised_xml_A, jsonised_xml_B)

    compare_joined_jsonized_xml(joined)
