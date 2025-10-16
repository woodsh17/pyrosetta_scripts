from pyrosetta.rosetta.core import simple_metrics
from pyrosetta.rosetta.core import select
from pyrosetta.rosetta.std import list_utility_tag_XMLSchemaAttribute_t
from pyrosetta.rosetta.std import map_unsigned_long_double

# SimpleMetric subclass for per residue b factor

class PerResidueBfactorBootCampMetric(simple_metrics.PerResidueRealMetric):
    """Python PerResidueBfactorBootCampMetric simple metric"""
    clones_ = list()

    def __init__(self, atom_type: str = "CA"):
        simple_metrics.PerResidueRealMetric.__init__(self)
        self.atom_type_: str = atom_type

    # Name of the class
    def name(self) -> str:
        return self.class_name()

    # Name of the metric
    def metric(self) -> str:
        return "bfactor"

    @staticmethod
    def class_name() -> str:
        return "PerResidueBfactorBootCampMetric"

    def parse_my_tag(self, tag, datamap) -> None:
        self.atom_type_ = tag.get_option_string("atom_type", "CA")

    @classmethod
    def provide_xml_schema(cls, xsd) -> None:
        from pyrosetta.rosetta.utility.tag import XMLSchemaAttribute, XMLSchemaType
        from pyrosetta.rosetta.utility.tag import xs_string

        attrlist = list_utility_tag_XMLSchemaAttribute_t()

        attrlist.append(XMLSchemaAttribute.required_attribute(
            "atom_type",
            XMLSchemaType(xs_string),
            "Which atom type you want to read the bfactor from"))

        description = '''
            PerResidue simple metric to report the b-factor 
            '''
        simple_metrics.xsd_simple_metric_type_definition_w_attributes(
                xsd,
                cls.class_name(),
                description, attrlist)

    def calculate(self, pose) -> map_unsigned_long_double:
       residue_selector = self.get_selector()
       #selection = selection_positions(residue_selector)
       subset = residue_selector.apply(pose)
       selection = select.get_residues_from_subset(subset)

       pdb_info = pose.pdb_info()

       b_fact_map = map_unsigned_long_double()

       for resi in selection:
           rt = pose.residue_type(resi)
           if rt.has(self.atom_type_):

               atom_idx = rt.atom_index(self.atom_type_)
               b_fact_map[ int(resi) ] = float(pdb_info.bfactor(resi, atom_idx))
       return b_fact_map
        

