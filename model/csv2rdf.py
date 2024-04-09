import csv
import re
from rdflib import URIRef, Literal
from .namespace import rdf
from sys import exit

class CSV2RDF:
    def __init__(self, csv_file) -> None:
        self.csv_file = csv_file
    
    def process_csv_to_rdf(self, subject_template, class_map, columns, output_graph):
        match = self._find_template_match(subject_template)[1]

        if self.csv_file is None:
            print("No source file found in the configuration file.")
            exit(1)

        if match is None:
            print("No match found in the subject template.")
            exit(1)
        
        if class_map is None:
            print("No class map found in the configuration file.")
            exit(1)

        if columns is None:
            print("No columns found in the configuration file.")
            exit(1)

        if not isinstance(columns, list):
            print("Columns must be a list.")
            exit(1)
        
        if not isinstance(class_map, URIRef):
            print("Class map must be a URIRef.")
            exit(1)

        if output_graph is None:
            print("No output graph found.")
            exit(1)
        
        with open(str(self.csv_file), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create a URI node with the row ID as the ID
                node = URIRef(subject_template.format(**{match: row['TermID']}))

                output_graph.add((node, URIRef(rdf.type), class_map))

                for column_name, predicate, datatype, language, split_by, template in columns:
                    self._add_triple(node, predicate, row[str(column_name)], datatype, language, split_by, template, output_graph)

    def _add_triple(self, subject, predicate, obj, datatype, language, split_by, template, output_graph):
        match = self._find_template_match(template)[1]
        # add url
        if match and split_by is not None:
            values = obj.replace('\n', '').split(split_by)
            for value in values:
                objectNode = URIRef(template.format(**{match: value}))
                output_graph.add((subject, predicate, objectNode))
            return

        if match:
            # Create a URI node with the row ID as the ID
            objectNode = URIRef(template.format(**{match: obj}))
            output_graph.add((subject, predicate, objectNode))
            return

        # add literal
        if split_by:
            # Split the cell value by the specified delimiter
            values = obj.replace('\n', '').split(split_by)
            for value in values:
                # Add a triple for each value
                cell_value = self._format_cell_value(value, datatype, language)
                output_graph.add((subject, predicate, Literal(cell_value, datatype=datatype, lang=language)))
        else:
            # Add a single triple for the cell value
            cell_value = self._format_cell_value(obj, datatype, language)
            output_graph.add((subject, predicate, Literal(cell_value, datatype=datatype, lang=language)))
    
    def _format_cell_value(self, value, datatype, language):
        return Literal(value.replace("\n", " ").strip(), datatype=datatype, lang=language)
    
    def _find_template_match(self, template):
        if template is None:
            return None, None, None

        match = re.match(r"(.*)\{(.*)\}(.*)", template)
        if match:
            return match.group(1), match.group(2), match.group(3)
        return None, None, None
