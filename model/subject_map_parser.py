from .namespace import rr, rml
from rdflib import Graph

class SubjectMapParser:
    def __init__(self, graph: Graph):
        self.graph = graph

    def parse(self, subject_map):
        template = self.graph.value(subject_map, rr.template)
        rdf_class = list(self.graph.objects(subject_map, rr['class']))
        logical_target = self.graph.value(subject_map, predicate=rml.logicalTarget)
        
        return template, rdf_class, logical_target