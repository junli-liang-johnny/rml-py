from .namespace import rr, arkMapping

class ObjectMapParser:
    def __init__(self, graph):
        self.graph = graph

    def parse(self, object_map):
        column = self.graph.value(object_map, rr.column)
        obj = self.graph.value(object_map, arkMapping.object)
        language = self.graph.value(object_map, rr.language)
        datatype = self.graph.value(object_map, rr.datatype)
        split_by = self.graph.value(object_map, arkMapping.splitBy)
        template = self.graph.value(object_map, rr.template)

        return column, obj, language, datatype, split_by, template