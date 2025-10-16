from pyrosetta.rosetta.core import simple_metrics
from Per_Residue_Bfactor_Metric import PerResidueBfactorBootCampMetric

#global var
_py_metric_creators_ = []

class PerResidueBfactorBootCampMetricCreator(simple_metrics.SimpleMetricCreator):
    instances_ = list()

    def __init__(self):
        simple_metrics.SimpleMetricCreator.__init__(self)

    def create_simple_metric(self):
        metric = PerResidueBfactorBootCampMetric()
        self.instances_.append(metric)
        return metric

    def keyname(self):
        return PerResidueBfactorBootCampMetric.class_name()

    def provide_xml_schema(self, xsd):
        PerResidueBfactorBootCampMetric.provide_xml_schema(xsd)

def register():
    
    factory = simple_metrics.SimpleMetricFactory.get_instance()
    creator = PerResidueBfactorBootCampMetricCreator()
    factory.factory_register(creator)
    
    _py_metric_creators_.append(creator)


