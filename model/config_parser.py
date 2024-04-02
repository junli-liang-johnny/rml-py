from .triples_map_parser import TriplesMapParser
from .object_map_parser import ObjectMapParser
from .namespace import rr, rml

class ConfigParser:
    def __init__(self, graph) -> None:
        self.graph = graph

    def parse(self):
        results = []
        triples_maps = TriplesMapParser(self.graph).subjects()
        object_map_parser = ObjectMapParser(self.graph)

        for trples_map in triples_maps:
            source_file = None
            file_type = None
            template = None
            class_map = None
            columns = []
 
            subject_map = self.graph.value(trples_map, rr.subjectMap)
            template = self.graph.value(subject_map, rr.template)
            print("Template: ", template)
            class_map = self.graph.value(subject_map, rr["class"])
            print("Class: ", class_map)

            logical_source = self.graph.value(trples_map, rml.logicalSource)
            source_file = self.graph.value(logical_source, predicate=rml.source)
            file_type = self.graph.value(logical_source, predicate=rml.referenceFormulation)
            print("Source file: ", source_file)

            predicate_object_maps = list(self.graph.objects(trples_map, rr.predicateObjectMap))
            for predicate_object_map in predicate_object_maps:
                predicate = self.graph.value(predicate_object_map, predicate=rr.predicate)
                object_map = self.graph.value(predicate_object_map, rr.objectMap)
                column, language, datatype, split_by = object_map_parser.parse(object_map)
                print("Column: ", column, ", Predicate: ", predicate, ", Language: ", language, ", Datatype: ", datatype, ", Split by: ", split_by)
                columns.append((column, predicate, datatype, language, split_by))

            results.append((source_file, file_type, template, class_map, columns))

        return results


