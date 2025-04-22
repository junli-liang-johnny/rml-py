import pytest
from rdflib import Graph, URIRef, Literal
from model.csv2rdf import CSV2RDF
from model.namespace import rmlpy, rdf

@pytest.fixture
def sample_csv_file(tmp_path):
	csv_file = tmp_path / "test.csv"
	csv_file.write_text("id,name,age\n1,John,30\n2,Jane,25\n")
	return str(csv_file)

def test_process_csv_to_rdf(sample_csv_file):
	csv2rdf = CSV2RDF(sample_csv_file)
	subject_template = "https://example.com/person/{id}"
	class_map = {
		"rdf_class": [rmlpy.Person],
		"rdf_class_ref": "id",
		"split_by": None
	}
	columns = [
		(None, "name", rmlpy.name, None, None, None, None, (None, None, None, None)),
		(None, "age", rmlpy.age, None, None, None, None, (None, None, None, None))
	]
	output_graph_dict = {}

	result = csv2rdf.process_csv_to_rdf(subject_template, class_map, columns, output_graph_dict)

	# Verify the RDF graph
	output_graph = list(result.values())[0][0]
	assert isinstance(output_graph, Graph)

	# Check if triples are added correctly
	john_uri = URIRef("https://example.com/person/1")
	jane_uri = URIRef("https://example.com/person/2")
	assert (john_uri, rdf.type, rmlpy.Person) in output_graph
	assert (jane_uri, rdf.type, rmlpy.Person) in output_graph
	assert (john_uri, rmlpy.name, Literal("John")) in output_graph
	assert (jane_uri, rmlpy.age, Literal("25")) in output_graph

def test_invalid_csv_file(tmp_path):
	invalid_csv_file = tmp_path / "invalid.csv"
	invalid_csv_file.write_text("id,name\n")  # Missing columns

	csv2rdf = CSV2RDF(str(invalid_csv_file))
	subject_template = "https://example.com/person/{id}"
	class_map = {"rdf_class": [rmlpy.Person], "rdf_class_ref": "id", "split_by": None}
	columns = []

	with pytest.raises(SystemExit):
		csv2rdf.process_csv_to_rdf(subject_template, class_map, columns, {})