# FSO_simulation_v2
Simple FSO propagation library. Propgates a gaussian beam through the turbulent atmoshpere. Can be used to estimate link budget losses due to the atmospheric turbulence for laser propagation. 

**USAGE**

1. Git clone or download the library
2. python -m pip install -r requirements.txt 

**MODIFY**

Parameters in the sim_config.json as needed

List of parameters accepted by *sim_config.json*

| Parameter       | Description   | Units       | Notes |
| -------------   | ------------- |-------------|-------------|
| sim_res         | simulation resolution  | pixels | Too small values can introduce numerical artefacts |  
| sim_size        | simulation size  | meters   | Should be at least 1.5*bigger than the total beam size at the receiver |
| rx_alt          | receiver altitude  | meters |      -       |
| rx_diameter     | receiver aperture diamter | meters        |       -      |
| wvl             | wavelength  | meters      |             |
| w0              | beam waist  | meters      |             |
| power           | beam power  | Watts            |             |
| n_phase_screens | Number of turbulent phase screens  | scalar            |             |
| max_turb_alt    | Maximum height of turbuelnt layers  | meters            |             |
| min_turb_alt    | Minimum height of turbuelnt layers  | meters            |             |
| r0              | Frieds parameter  | meters | Array, should be of size n_phase_screens |
| screen_alt      | Content Cell  |  meters           | Array, should be of size n_phase_screens |
| l0              | Content Cell  |   meters          | Array, should be of size n_phase_screens            |
| L0              | Content Cell  |      meters       | Array, should be of size n_phase_screens            |


**ESTIMATE TURBULENCE LOSSES**



**OUTPUT**

![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/71328fd6-879a-43f7-8ad5-fec775ab6a4f)
![image](https://github.com/MarcnKov/FSO_simulation_v2/assets/46137836/bf415d49-0fd7-4813-9054-15187ec97dfb)
