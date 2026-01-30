from dataclasses import dataclass
from typing import Literal

import numpy as np

@dataclass(eq=True, frozen=True)
class ExperimentMetadata:
    """
    Stores information about spectrum metadata.

    Attributes
    ----------
    heating_timestep_index: int
        Number of the experimental timestep (0, 1, 2, 3, 4, etc...)
    time_value: float
        Time at the measurement in hours.
    temperature: float
        Temperature of the furnace at the time of measurement (degrees C).
    fo2: float
        Oxygen fugacity of the furnace for the run (in log(delta_FMQ))
    polarization: Literal["Unpolarized", "0", "90"]
        Polarization state.
    acquisition_type: Literal["Spot", "Traverse"]
        If Spot, xpos, ypos and possibly zpos will all be specified.
    xpos: float
        X Position, if Y and Z are None, this represents distance along
        traverse.
    ypos: float
        Y Position
    zpos: float
        Z Position
    """
    spectrum_num: int
    wavelength_unit: str
    sample_name: str
    slab_name: str
    heating_timestep_index: int
    time_value: float
    temperautre: float
    fo2: float
    polarization: Literal['Unpolarized', '0', '90']
    acquisition_type: Literal["Spot", "Traverse"]
    focus_height: Literal["Bottom", "Top", "Middle"]
    xpos: float
    ypos: float | None = None
    zpos: float | None = None
    traverse_direction: Literal["EW", "NS"] | None = None

translator = {
    "Pol0": "0",
    "Unpol": "Unpolarized",
    "Pol90": "90"
}

@dataclass(eq=True, frozen=True)
class FTIRSpectrum:
    wavelength: np.ndarray
    absorbance: np.ndarray
    metadata: ExperimentMetadata
