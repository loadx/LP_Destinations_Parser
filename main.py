import os
import shutil
import sys
import time

from utils import current_dir, make_folder
from destination import Destination
from taxonomy import ListItem, DoubleLinkedList
import xml.etree.cElementTree as ET


def process_destinations(file_name, taxonomies, template_file, output_location):
    """
    Process each <destination> in the xml file into its own file based on `template_file`

    :param: file_name (string/path) - full_path to the destinations.xml
    :param: taxonomies (dict) - double linked list of all the menu items
    :param: template_file (string/path) - full path to the template file
    :param: output_location (string/path) - where each processed destination should be stored
    """
    destination = None

    for event, elem in ET.iterparse(file_name, events=('start','end',)):
        if elem.tag == 'destination':
            if event == 'start':
                location = elem.get('title')
                geo_id = elem.get('atlas_id')

                # build a destination.html
                file_name = os.path.join(output_location, "%s.html" % Destination.sanitize_name(location))
                fp = open(file_name, 'w')
                destination = Destination(location, fp)
            else:
                destination.write_blocks_to_template(taxonomies, geo_id, template_file)
                print "processed: %s" % location

        if destination:
            for text_item in elem.itertext():
                destination.build_block(elem.tag, text_item)


def process_taxonomies(file_name):
    """
    Builds a double linked list of all taxonomy items with hierachy

    e.g
    tree[<geo_id>] = {current: <location_name>, prev: <tree item of previous node>, next: <tree item of next node>}
    """
    depth_list = []
    location_id = None

    # need to track depth
    dllist = DoubleLinkedList()
    for event, elem in ET.iterparse(file_name, events=('start','end',)):
        if event == 'start':
            if elem.tag == 'node':
                location_id = elem.get('geo_id')

            if elem.tag == 'node_name':
                dllist.add(location_id, elem.text)
                if len(depth_list) >= 1:
                    # set the current items previous pointer to the
                    # correct parent for the current depth
                    dllist.set_prev_pointer(dllist[depth_list[-1]])

                depth_list.append(location_id)

        if event == 'end':
            if elem.tag == 'node':
                if len(depth_list) > 0:
                    # moved up one depth
                    depth_list.pop()

    return dllist


def main():
    start_time = time.time()
    template_location = os.path.join(current_dir(), 'output-template')
    css_file = os.path.join(template_location, 'static', 'all.css')
    template_file = os.path.join(template_location, 'example.html')

    args = sys.argv[1:]

    if len(args) < 3:
        raise Exception("This script should be run using. ./run <destination.xml> <taxonomy.xml> /path/to/output_location")

    # create the output folder and move the static files into it
    output_location = args[2]
    static_location = os.path.join(output_location, 'static')
    make_folder(output_location)
    make_folder(static_location)

    shutil.copy2(css_file, static_location)
    print "copied css from %s to %s" % (css_file, static_location)

    try:
        taxonomies = process_taxonomies(args[1])
    except:
        raise Exception("Taxonomies could not be processed :(")

    try:
        process_destinations(args[0], taxonomies, template_file, output_location)
    except:
        raise Exception("Destinations could not be processed :(")

    print "\nexecution took: %0.2f seconds" % (time.time() - start_time)

if __name__ == '__main__':
    main()
