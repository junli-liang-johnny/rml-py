from .triples_map_parser import TriplesMapParser
from .object_map_parser import ObjectMapParser
from .predicate_object_map_parser import PredicateObjectMapParser
from .logical_target_parser import LogicalTargetParser
from .subject_map_parser import SubjectMapParser
from .namespace import rr, rml

class ConfigParser:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.object_map_parser = ObjectMapParser(graph)
        self.predicate_object_map_parser = PredicateObjectMapParser(graph)
        self.logical_target_parser = LogicalTargetParser(graph)
        self.subject_map_parser = SubjectMapParser(graph)

    def parse(self):
        results = []
        triples_maps = TriplesMapParser(self.graph).subjects()

        for trples_map in triples_maps:
            source_file = None
            file_type = None
            template = None
            rdf_class = None
            columns = []
 
            # subject map parser
            subject_map = self.graph.value(trples_map, rr.subjectMap)
            template, rdf_class, subject_logical_target_map = self.subject_map_parser.parse(subject_map)
            print("Template: ", template, ", Class: ", rdf_class)

            # logical source parser
            logical_source = self.graph.value(trples_map, rml.logicalSource)
            source_file = self.graph.value(logical_source, predicate=rml.source)
            file_type = self.graph.value(logical_source, predicate=rml.referenceFormulation)
            print("Source file: ", source_file)
            print("File type: ", file_type)

            predicate_object_maps = list(self.graph.objects(trples_map, rr.predicateObjectMap))
            for predicate_object_map in predicate_object_maps:
                predicate_list, object_map, object_list, logical_target_map = self.predicate_object_map_parser.parse(predicate_object_map)
                column, obj, language, datatype, split_by, _template  = self.object_map_parser.parse(object_map)
                logical_target_tuple = self.logical_target_parser.parse(predicate_object_map)
                print("Predicate: ", predicate_list, ", Object: ", object_list, ", Column: ", column, ", Language: ", language, ", Datatype: ", datatype, ", Split by: ", split_by, ", Template: ", _template)

                for predicate in predicate_list:
                    if len(object_list) > 0:
                        for obj in object_list:
                            columns.append((obj, column, predicate, datatype, language, split_by, _template, logical_target_tuple))
                    elif obj is not None:
                        columns.append((obj, column, predicate, datatype, language, split_by, _template, logical_target_tuple))
                    else:
                        columns.append((None, column, predicate, datatype, language, split_by, _template, logical_target_tuple))

            results.append((source_file, file_type, template, rdf_class, columns))
            print("\n")

        return results


