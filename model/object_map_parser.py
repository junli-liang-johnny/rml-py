from .namespace import rr, arkMapping, rml

class ObjectMapParser:
    def __init__(self, graph):
        self.graph = graph

    def parse(self, object_map):
        column = self.graph.value(object_map, rr.column)
        language = self.graph.value(object_map, rr.language)
        datatype = self.graph.value(object_map, rr.datatype)
        split_by = self.graph.value(object_map, arkMapping.splitBy)
        template = self.graph.value(object_map, rml.template)
        return column, language, datatype, split_by, template