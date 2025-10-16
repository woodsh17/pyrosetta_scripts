#!/usr/bin/env python3
from __future__ import annotations
import sys

from pyrosetta import init, pose_from_pdb
from pyrosetta.rosetta.protocols.rosetta_scripts import XmlObjects
from pyrosetta.rosetta import protocols, utility
from pyrosetta.rosetta.utility import vector1_std_string
from register_metric import register  # your MoverCreator registration
from pyrosetta.rosetta.utility.options import OptionCollection
from pyrosetta.rosetta.basic.datacache import DataMap



# Embedded RosettaScripts XML:
EMBEDDED_XML = """<ROSETTASCRIPTS>
  <SCOREFXNS>
    <ScoreFunction name="sfxn" weights="ref2015"/>
  </SCOREFXNS>
  <SIMPLE_METRICS>
    <PerResidueBfactorBootCampMetric name="bfactor" atom_type="CA"/>
  </SIMPLE_METRICS>
  <MOVERS>
    <RunSimpleMetrics name="metrics" metrics="bfactor"/>
  </MOVERS>
  <PROTOCOLS>
    <Add mover="metrics"/>
  </PROTOCOLS>
</ROSETTASCRIPTS>
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_embedded_rs.py <pdb_path>")
        sys.exit(1)
    pdb_path = sys.argv[1]

    # Initialize Rosetta (add flags as needed)

    # Register your mover BEFORE parsing XML so schema/type are known
    register()
    init("-ignore_unrecognized_res")

    pose = pose_from_pdb(pdb_path)

    # Parse XML string and build the overall protocol mover
    xmlobj = XmlObjects.create_from_string(EMBEDDED_XML)
    protocol = xmlobj.get_mover("ParsedProtocol")  # the top-level protocol
    protocol.apply(pose)

    print("Protocol finished. Final score:", pose.energies().total_energy())

    chain, pdb_resi = "A", 42
    resi = pose.pdb_info().pdb2pose(chain, pdb_resi)
    key = f"bfactor_{resi}"
    print(f"CA B-factor for {chain}{pdb_resi} (pose {resi}): {pose.scores.get(key)}")

if __name__ == "__main__":
    main()

