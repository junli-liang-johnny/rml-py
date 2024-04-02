import csv
import re
from rdflib import URIRef, Literal
from .namespace import rdf

class CSV2RDF:
    def __init__(self, csv_file) -> None:
        self.csv_file = csv_file
    
    def process_csv_to_rdf(self, subject_template, class_map, columns, output_graph):
        match = self._find_template_match(subject_template)[1]

        if self.csv_file is None or match is None or class_map is None:
            print("No source file found in the configuration file.")
            exit()
        
        with open(str(self.csv_file), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create a URI node with the row ID as the ID
                node = URIRef(subject_template.format(**{match: row['TermID']}))

                output_graph.add((node, URIRef(rdf.type), class_map))

                for column_name, predicate, datatype, language, split_by in columns:
                    column_name = str(column_name)
                    if split_by:
                        # Split the cell value by the specified delimiter
                        values = row[column_name].split(split_by)
                        for value in values:
                            # Add a triple for each value
                            output_graph.add((node, predicate, Literal(value.strip(), datatype=datatype, lang=language)))
                    else:
                        # Add a single triple for the cell value
                        output_graph.add((node, predicate, Literal(row[column_name], datatype=datatype, lang=language)))
    
    def _find_template_match(self, template):
        match = re.match(r"(.*)\{(.*)\}(.*)", template)
        if match:
            return match.group(1), match.group(2), match.group(3)
        return None, None, None
