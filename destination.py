import os

from jinja2 import Environment, FileSystemLoader
from taxonomy import DoubleLinkedList


class Destination(object):
    """
    Helper class for writing a destination file
    title - name of the destination

    optional kwargs:
    tags_to_capture = list or tuple of tags you wish to traverse for data
    """
    tags_to_print = ('history', 'overview', 'weather', 'money', 'getting_there_and_away')

    def __init__(self, title, file_pointer, **kwargs):
        try:
            file_pointer.write('Testing')
            file_pointer.seek(0)
        except:
            raise Exception("file_pointer is invalid or no write permissions")

        # file to dump contents to
        self.fp = file_pointer
        self.title = title
        self.tags_to_capture = kwargs.get('tags_to_capture', self.tags_to_print)
        self.filled_items = []
        self.contents = ''

    @classmethod
    def sanitize_name(self, string_name):
        """
        Returns a clear filename string e.g
        'Example aWEsome File' would become 'example_awesome_file'

        :param: string_name (string) - Name to sanitize
        :return: string
        """
        return string_name.lower().replace(' ', '_')

    @classmethod
    def sanitize_heading(self, heading):
        """
        Returns a clear heading string e.g
        'example_awesome_title' would become 'Example Awesome File'

        :param: heading (string) - Heading to sanitize
        :return: string
        """
        title = heading.title()
        return ' '.join(title.split('_'))

    def build_block(self, heading, content):
        """
        Process an xml block item

        :param: heading (string) - current block's heading
        :param: content (string) - blocks's paragraph content
        :return: string - current contents buffer
        """
        if heading in self.tags_to_capture:
            content = content.strip()

            # if we've already processed this node, drop it
            # likewise if the data is junk
            if heading not in self.filled_items and content != '':

                # normally id make a list and push each block into it but the
                # overhead of creating the list is large, so adding html to
                # the contents buffer is better in this case
                self.contents += "<h2>%s</h2>" % Destination.sanitize_heading(heading)
                self.contents += "<p>%s</p>" % content.encode('ascii', 'ignore')
                self.contents += "\n"
                self.filled_items.append(heading)

        return self.contents

    @classmethod
    def get_nav(self, taxonomy, taxonomy_ref):
        nav = list(reversed(taxonomy.flatten(taxonomy_ref, True, max_items=3)))
        nav += taxonomy.flatten(taxonomy_ref, False, max_items=3)

        # remove the current destination name
        return [n for n in nav if n != taxonomy[taxonomy_ref].current]

    def write_blocks_to_template(self, taxonomy, geo_id, template_file_path):
        """
        write all buffered blocks to the template
        """
        split = os.path.split(template_file_path)
        template_dir = split[0]
        template_file = split[1]

        template = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
        template.globals['sanitize_name'] = Destination.sanitize_name
        template = template.get_template(template_file)

        # using local vars, fill the template and write to disk
        nav = Destination.get_nav(taxonomy, geo_id)
        self.fp.write(template.render(destination_name=self.title, contents=self.contents, nav=nav))
        self.fp.close()

        # just in case this dangles for too long
        del(template)
