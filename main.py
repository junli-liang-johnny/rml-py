import argparse
from rdflib import Graph 
from model.config_parser import ConfigParser
from model.csv2rdf import CSV2RDF
from model.toRDF import ToRDF
from model.format_parser import FormatParser

# Create an argument parser
parser = argparse.ArgumentParser(description='Process a Turtle file.')
parser.add_argument('--config', type=str, help='The path to the config file', required=True)

# Parse the command-line arguments
args = parser.parse_args()

# Parse in an RDF file
input_graph = Graph()
print("Input graph created")
input_graph.parse(args.config, format="turtle")
print("Input graph parsed")
output_graph_dict: dict[str: tuple[Graph, str]] = {}

namespaces = input_graph.namespaces()
format_parser = FormatParser()

for source_file, file_type, template, class_map, columns in ConfigParser(input_graph).parse():
    if source_file is None:
        ToRDF().to_rdf(template, class_map, columns, output_graph_dict)
    else:
        CSV2RDF(source_file).process_csv_to_rdf(template, class_map, columns, output_graph_dict)

# Serialize the graph to a TTL file
for destination in output_graph_dict:
    output_graph, format = output_graph_dict[destination]
    print("Destination: ", destination, ", output_graph: ", output_graph)
    print("\n")
    format_str = format_parser.parse(format)
    for prefix, uri in namespaces:
        output_graph.bind(prefix, uri)
    output_graph.serialize(destination, format_str)