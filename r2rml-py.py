import argparse
from rdflib import Graph 
from model.config_parser import ConfigParser
from model.csv2rdf import CSV2RDF

# Create an argument parser
parser = argparse.ArgumentParser(description='Process a Turtle file.')
parser.add_argument('--input', type=str, help='The path to the Turtle file', required=True)
parser.add_argument('--output', type=str, help='The path to the output file', required=True)

# Parse the command-line arguments
args = parser.parse_args()

# Parse in an RDF file
input_graph = Graph()
output_graph = Graph()
input_graph.parse(args.input, format="turtle")

namespaces = input_graph.namespaces()
for prefix, uri in namespaces:
    output_graph.bind(prefix, uri)

config_parser = ConfigParser(input_graph)
triples_maps = config_parser.parse()
for source_file, file_type, template, class_map, columns in triples_maps:
    CSV2RDF(source_file).process_csv_to_rdf(template, class_map, columns, output_graph)

# Serialize the graph to a TTL file
output_graph.serialize(destination=str(args.output), format='turtle')