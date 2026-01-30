# Built-Ins
from pathlib import Path
from typing import Literal
import re

# Dependencies
import pandas as pd

# Local Imports
from hackathon_package.spectrum_class import FTIRSpectrum, ExperimentMetadata


polarization_translator: dict[str, Literal['Unpolarized', '0', '90']] = {
    "Pol0": "0",
    "Unpol": "Unpolarized",
    "Pol90": "90"
}

acq_type_translator: dict[str, Literal["Spot", "Traverse"]] = {
    "Position": "Spot",
    "Distance": "Traverse"
}

def open_csv(file_path: str | Path):
    df = pd.read_csv(file_path)
    print(df)


if __name__ == "__main__":
    file_name_pattern = re.compile(
        r"^(Position|Distance)\s*\(micrometers\)=\s*((?:-?\d+\s*µm(?:\s*,\s*)"
        r"?){1,3})\s*Number-\s*(\d+).*?"
    )
    base_fp = Path("C:/D stuff/UMD Geol/Research/For experiments/Experiments/")
    spot_set = Path(base_fp, "FMQ900_GS_slab/GSB1.2_normal_b/")
    spectrum_list: list[ExperimentMetadata] = []
    for p, d, file_list in spot_set.walk():
        for file in file_list:
            full_file_name = Path(p, file)
            if full_file_name.suffix == ".CSV":
                parts = full_file_name.parts

                file_name = full_file_name.parts[-1]
                match = file_name_pattern.search(file_name)
                if match is None:
                    continue
                grps = match.groups()
                acq_type = acq_type_translator.get(grps[0])
                position = [int(x) for x in re.findall(r"-?\d+(?=\s*µm)", grps[1])]
                spec_num = grps[2]

                part_length = len(full_file_name.parts)
                if full_file_name.parts[-3].find("Trav") > -1:
                    trav_dir = full_file_name.parts[-3][-2:]
                else:
                    trav_dir = None

                if part_length == 12:
                    sample_name = parts[-6]
                    slab_name = parts[-5]
                    focus_height="Middle"
                    timestep_idx = int(parts[-4][1:])
                elif part_length == 13:
                    sample_name = parts[-7]
                    slab_name = parts[-6]
                    focus_height = parts[-3]
                    timestep_idx = int(parts[-5][1:])
                else:
                    raise ValueError()
                
                time_val = 0.0
                temp = 0.0
                fo2 = 0.0
                pol = polarization_translator.get(parts[-2])

                if len(position) == 1:
                    meta_obj = ExperimentMetadata(
                        spectrum_num=spec_num,
                        wavelength_unit="cm^-1",
                        sample_name=sample_name,
                        slab_name=slab_name,
                        heating_timestep_index=timestep_idx,
                        time_value=time_val,
                        temperautre=temp,
                        fo2=fo2,
                        polarization=pol,
                        acquisition_type=acq_type,
                        traverse_direction = trav_dir,
                        focus_height=focus_height,
                        xpos=position[0]
                    )
                elif len(position) == 2:
                    meta_obj = ExperimentMetadata(
                        spectrum_num=spec_num,
                        wavelength_unit="cm^-1",
                        sample_name=sample_name,
                        slab_name=slab_name,
                        heating_timestep_index=timestep_idx,
                        time_value=time_val,
                        temperautre=temp,
                        fo2=fo2,
                        polarization=pol,
                        acquisition_type=acq_type,
                        traverse_direction = trav_dir,
                        focus_height=focus_height,
                        xpos=position[0],
                        ypos=position[1]
                    )
                elif len(position) == 3:
                    meta_obj = ExperimentMetadata(
                        spectrum_num=spec_num,
                        wavelength_unit="cm^-1",
                        sample_name=sample_name,
                        slab_name=slab_name,
                        heating_timestep_index=timestep_idx,
                        time_value=time_val,
                        temperautre=temp,
                        fo2=fo2,
                        polarization=pol,
                        acquisition_type=acq_type,
                        traverse_direction = trav_dir,
                        focus_height=focus_height,
                        xpos=position[0],
                        ypos=position[1],
                        zpos=position[2]
                    )
                else:
                    raise ValueError()
                spectrum_list.append(meta_obj)


    def get_traverse_group_that_i_want(spec_list: list[ExperimentMetadata]):
        num = 0
        for i in spec_list:
            if (
                i.sample_name == "FMQ900_GS_slab" and
                i.slab_name == "GSB1.2_normal_b" and
                i.polarization == "Unpolarized" and
                i.heating_timestep_index == 4 and
                i.traverse_direction == "NS"
            ):
                print(i.polarization, num)
                num+=1
    get_traverse_group_that_i_want(spectrum_list)